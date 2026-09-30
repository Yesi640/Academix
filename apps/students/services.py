from django.db import transaction
from .models import StudentProfile, Enrollment
from apps.courses.models import CourseSection, AcademicYear
from apps.audit.services import log_audit

def get_or_create_student_profile(user, student_code=None, parent=None, blood_type='O+'):
    """Recupera o crea el expediente para un usuario con rol STUDENT."""
    if not student_code:
        student_code = f"EST-{user.id:05d}"

    profile, _ = StudentProfile.objects.get_or_create(
        user=user,
        defaults={
            'student_code': student_code,
            'parent': parent,
            'blood_type': blood_type,
        }
    )
    return profile

@transaction.atomic
def enroll_student_in_section(student_profile, course_section, academic_year, user=None):
    """
    Matricula formalmente a un estudiante en un grupo para un año lectivo determinado.
    Garantiza integridad referencial y audita la acción.
    """
    enrollment, created = Enrollment.objects.update_or_create(
        student=student_profile,
        academic_year=academic_year,
        defaults={
            'course_section': course_section,
            'status': Enrollment.Status.ACTIVE,
        }
    )

    action = 'INSERT' if created else 'UPDATE'
    log_audit(
        action=action,
        table_name='Enrollment',
        record_id=enrollment.id,
        new_values={
            'student': student_profile.user.get_full_name() or student_profile.user.username,
            'code': student_profile.student_code,
            'section': course_section.name,
            'year': academic_year.year,
            'status': enrollment.status,
        },
        reason=f'Matrícula de estudiante {student_profile.user.username} en curso {course_section.name} ({academic_year.year})',
        user=user
    )

    return enrollment


def send_student_credentials_email(
    user,
    raw_password,
    student_code='',
    section_name='',
    academic_year='',
    login_url='',
    fail_silently=True
):
    """
    Envía un correo electrónico institucional al estudiante con sus credenciales
    y el enlace con instrucciones para cambiar la contraseña en su primer acceso.
    """
    import logging
    from django.core.mail import EmailMultiAlternatives
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    from django.conf import settings

    logger = logging.getLogger(__name__)

    recipient_email = user.email
    if not recipient_email or '@' not in recipient_email:
        return False, "Correo no válido o ausente."

    try:
        subject = f"ACADEMIX - Tus Credenciales de Acceso Institucional ({user.get_full_name() or user.username})"
        context = {
            'user': user,
            'student_name': user.get_full_name() or user.username,
            'username': user.username,
            'password': raw_password,
            'student_code': student_code,
            'document_number': user.document_number or '',
            'document_type': user.get_document_type_display(),
            'section_name': section_name,
            'academic_year': academic_year,
            'login_url': login_url,
        }

        html_content = render_to_string('emails/student_credentials.html', context)
        text_content = strip_tags(html_content)

        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'notificaciones@academix.edu.co'),
            to=[recipient_email],
        )
        email.attach_alternative(html_content, "text/html")
        email.send(fail_silently=False)
        return True, "Enviado exitosamente."
    except Exception as exc:
        logger.warning(f"Error al enviar correo a {recipient_email}: {exc}")
        if not fail_silently:
            raise
        return False, str(exc)


def send_bulk_student_credentials(credentials_list, login_url=''):
    """
    Envía credenciales de acceso en lote para estudiantes matriculados.
    Reutiliza conexión SMTP y gestiona errores individualmente sin detener el lote.
    Retorna un diccionario con estadísticas:
    {'sent': int, 'failed': int, 'skipped': int, 'errors': list}
    """
    import logging
    from django.core.mail import EmailMultiAlternatives, get_connection
    from django.template.loader import render_to_string
    from django.utils.html import strip_tags
    from django.conf import settings

    logger = logging.getLogger(__name__)
    results = {'sent': 0, 'failed': 0, 'skipped': 0, 'errors': []}

    if not credentials_list:
        return results

    connection = None
    try:
        connection = get_connection()
        connection.open()
    except Exception as conn_err:
        logger.warning(f"No se pudo inicializar conexión de correo: {conn_err}")
        connection = None

    from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'notificaciones@academix.edu.co')

    for item in credentials_list:
        user = item.get('user')
        raw_password = item.get('password')
        student_code = item.get('student_code', '')
        section_name = item.get('section_name', '')
        academic_year = item.get('academic_year', '')
        custom_email = item.get('email')

        email_to_use = custom_email or (user.email if user else None)
        if not email_to_use or '@' not in email_to_use:
            results['skipped'] += 1
            continue

        try:
            student_display_name = user.get_full_name() or user.username
            subject = f"ACADEMIX - Credenciales de Acceso y Activacion de Cuenta ({student_display_name})"
            context = {
                'user': user,
                'student_name': student_display_name,
                'username': user.username,
                'password': raw_password,
                'student_code': student_code,
                'document_number': user.document_number or '',
                'document_type': user.get_document_type_display(),
                'section_name': section_name,
                'academic_year': academic_year,
                'login_url': login_url,
            }
            html_content = render_to_string('emails/student_credentials.html', context)
            text_content = strip_tags(html_content)

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_content,
                from_email=from_email,
                to=[email_to_use],
                connection=connection
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send(fail_silently=False)
            results['sent'] += 1
        except Exception as err:
            results['failed'] += 1
            results['errors'].append(f"{user.username if user else 'desconocido'}: {str(err)}")
            logger.warning(f"Fallo al enviar correo a {email_to_use}: {err}")

    if connection:
        try:
            connection.close()
        except Exception:
            pass

    return results


# ══════════════════════════════════════════════════════════════════════════════
# MÓDULO 2: CARPETA PERPETUA Y EXPEDIENTE DIGITAL DEL ESTUDIANTE (CON RBAC)
# ══════════════════════════════════════════════════════════════════════════════

def can_user_access_student_expediente(user, student_profile):
    """
    Control de acceso granular (RBAC) para el Expediente Digital Perpetuo:
    - Secretaría Académica / Administrador / Rector: Lectura y verificación total.
    - Docente / Director de Grupo: Exclusivamente sobre estudiantes de su curso asignado.
    - Padre de Familia / Acudiente: Exclusivamente sobre sus hijos/acudidos vinculados.
    - Estudiante: Exclusivamente sobre su propio expediente personal.
    Retorna True si tiene autorización; False en caso contrario.
    """
    if not user or not user.is_authenticated:
        return False

    # 1. Directivos y Secretaría tienen acceso institucional universal
    if user.is_admin_role or user.is_rector or user.is_secretary:
        return True

    # 2. Estudiante consultando su propio expediente
    if user.is_student:
        return hasattr(user, 'student_profile') and user.student_profile.id == student_profile.id

    # 3. Padre de familia consultando a su hijo dependiente
    if user.is_parent:
        return student_profile.parent_id == user.id

    # 4. Docente: Validar si es el Director de Grupo del curso donde el estudiante está activo
    if user.is_teacher and hasattr(user, 'teacher_profile'):
        from apps.teachers.models import TeachingAssignment
        from apps.courses.services import get_current_academic_year
        
        current_year = get_current_academic_year()
        current_enrollment = student_profile.enrollments.filter(
            status=Enrollment.Status.ACTIVE,
            academic_year=current_year
        ).first()

        if current_enrollment:
            return TeachingAssignment.objects.filter(
                teacher=user.teacher_profile,
                course_section=current_enrollment.course_section,
                is_group_director=True,
                is_active=True
            ).exists()

    return False


def can_user_manage_student_expediente(user, student_profile):
    """
    Evalúa si el usuario tiene privilegios de gestión (subir soportes oficiales,
    verificar o anular documentos) en el expediente del estudiante.
    """
    if not user or not user.is_authenticated:
        return False
    return user.is_admin_role or user.is_rector or user.is_secretary


def validate_admission_checklist(student_profile):
    """
    Verifica el cumplimiento de requisitos obligatorios del expediente de matrícula:
    1. Documento de Identidad (Registro Civil o Tarjeta de Identidad)
    2. Certificado de Afiliación a EPS
    3. Carnet de Vacunación o Ficha Médica
    4. Contrato de Matrícula (colegios privados) o Certificado de Estudios Anteriores
    """
    from .models import ExpedienteDocumento
    from apps.courses.services import get_institution_settings

    inst = get_institution_settings()

    # Requisitos base
    required_defs = [
        {
            'id': 'identidad',
            'label': 'Documento de Identidad (Registro Civil / TI / Cédula)',
            'types': [
                ExpedienteDocumento.DocumentType.REGISTRO_CIVIL,
                ExpedienteDocumento.DocumentType.TARJETA_IDENTIDAD
            ],
            'category': ExpedienteDocumento.Category.ADMISSION
        },
        {
            'id': 'eps',
            'label': 'Certificado de Afiliación a Salud (EPS / SISBEN)',
            'types': [ExpedienteDocumento.DocumentType.CERTIFICADO_EPS],
            'category': ExpedienteDocumento.Category.ADMISSION
        },
        {
            'id': 'vacunas',
            'label': 'Carnet de Vacunación o Certificado Médico',
            'types': [ExpedienteDocumento.DocumentType.CARNET_VACUNAS],
            'category': ExpedienteDocumento.Category.ADMISSION
        },
    ]

    # Requisito adicional para colegios privados: Contrato de matrícula
    if inst.is_private_institution:
        required_defs.append({
            'id': 'contrato',
            'label': 'Contrato de Matrícula y Prestación de Servicios',
            'types': [ExpedienteDocumento.DocumentType.CONTRATO_MATRICULA],
            'category': ExpedienteDocumento.Category.ADMINISTRATIVE
        })
    else:
        # Colegio oficial: Certificado de estudios anteriores
        required_defs.append({
            'id': 'estudios_ant',
            'label': 'Certificado de Estudios de Años Anteriores',
            'types': [ExpedienteDocumento.DocumentType.CERTIFICADO_ESTUDIO_ANT],
            'category': ExpedienteDocumento.Category.ADMISSION
        })

    docs = list(student_profile.expediente_documentos.all())

    checklist_items = []
    completed_count = 0
    verified_count = 0

    for req in required_defs:
        matched_doc = next((d for d in docs if d.document_type in req['types']), None)
        is_present = matched_doc is not None
        is_verified = matched_doc.is_verified if matched_doc else False

        if is_present:
            completed_count += 1
        if is_verified:
            verified_count += 1

        checklist_items.append({
            'id': req['id'],
            'label': req['label'],
            'is_present': is_present,
            'is_verified': is_verified,
            'document': matched_doc,
        })

    total_req = len(required_defs)
    percentage = int((completed_count / total_req) * 100) if total_req > 0 else 100
    is_complete = (completed_count == total_req)

    return {
        'is_complete': is_complete,
        'percentage': percentage,
        'completed_count': completed_count,
        'total_required': total_req,
        'missing_count': total_req - completed_count,
        'verified_count': verified_count,
        'items': checklist_items,
    }


@transaction.atomic
def attach_bulletin_to_expediente(student_profile, period, pdf_content=None, filename=None, user=None):
    """
    Automatización: Archiva de forma perpetua e inmutable el boletín oficial
    en el expediente digital del estudiante bajo la categoría ACADEMIC.
    """
    from django.core.files.base import ContentFile
    from .models import ExpedienteDocumento

    doc_title = f"Boletín Oficial — {period.name} ({period.academic_year.year})"
    
    # Buscar si ya existe un documento archivado para este periodo y año
    doc = ExpedienteDocumento.objects.filter(
        student=student_profile,
        category=ExpedienteDocumento.Category.ACADEMIC,
        document_type=ExpedienteDocumento.DocumentType.BOLETIN_OFICIAL,
        academic_year=period.academic_year,
        title=doc_title
    ).first()

    if not doc:
        doc = ExpedienteDocumento(
            student=student_profile,
            category=ExpedienteDocumento.Category.ACADEMIC,
            document_type=ExpedienteDocumento.DocumentType.BOLETIN_OFICIAL,
            academic_year=period.academic_year,
            title=doc_title,
            is_verified=True,
            verified_by=user,
            uploaded_by=user,
            notes=f"Boletín oficial generado automáticamente por el motor ACADEMIX para el periodo {period.number}."
        )

    if pdf_content:
        fname = filename or f"boletin_P{period.number}_{student_profile.student_code}.pdf"
        doc.file.save(fname, ContentFile(pdf_content), save=False)

    doc.save()

    log_audit(
        action='INSERT',
        table_name='ExpedienteDocumento',
        record_id=doc.id,
        new_values={'title': doc.title, 'student': student_profile.user.get_full_name()},
        reason=f"Inyección automática de boletín oficial al expediente perpetuo de {student_profile.user.get_full_name()}",
        user=user
    )

    return doc


@transaction.atomic
def verify_expediente_document(document_id, user):
    """
    Marca oficialmente un soporte del expediente como verificado con trazabilidad de auditoría.
    """
    from .models import ExpedienteDocumento
    from django.utils import timezone

    doc = ExpedienteDocumento.objects.select_for_update().get(id=document_id)
    doc.is_verified = True
    doc.verified_by = user
    doc.verified_at = timezone.now()
    doc.save(update_fields=['is_verified', 'verified_by', 'verified_at'])

    log_audit(
        action='UPDATE',
        table_name='ExpedienteDocumento',
        record_id=doc.id,
        new_values={'is_verified': True, 'verified_by': user.username},
        reason=f"Verificación oficial de documento '{doc.title}' en expediente de {doc.student.user.get_full_name()}",
        user=user
    )

    return doc


