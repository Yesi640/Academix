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

