"""
Servicio centralizado de notificaciones por correo electronico institucional para ACADEMIX.
Envia credenciales, alertas de asistencia, nuevas tareas por curso, comunicados de rectoria/secretaria y observador.
"""
import logging
import threading
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = logging.getLogger(__name__)


def is_valid_recipient(email):
    """Filtra correos nulos o ficticios de prueba."""
    if not email or '@' not in email:
        return False
    email = email.strip().lower()
    domain = email.split('@')[-1]
    if domain in ['ejemplo.com', 'example.com', 'test.com', 'correo.com']:
        return False
    return True


def _send_async_mail(subject, text_content, html_content, recipient_list):
    """Despacha correos en un hilo secundario para no bloquear la navegacion del usuario."""
    valid_recipients = [r.strip() for r in recipient_list if is_valid_recipient(r)]
    if not valid_recipients:
        logger.info(f"Omitiendo envio para {recipient_list}: ningun correo real valido.")
        return

    def _worker():
        try:
            from_email = f"ACADEMIX <{settings.EMAIL_HOST_USER}>" if settings.EMAIL_HOST_USER else settings.DEFAULT_FROM_EMAIL
            for recipient in valid_recipients:
                try:
                    msg = EmailMultiAlternatives(
                        subject=subject,
                        body=text_content,
                        from_email=from_email,
                        to=[recipient]
                    )
                    msg.attach_alternative(html_content, "text/html")
                    msg.send(fail_silently=False)
                    logger.info(f"[NOTIFICACION_ENVIADA] Correo enviado a {recipient}: {subject}")
                    print(f"[NOTIFICACION_ENVIADA] Correo enviado a {recipient}: {subject}")
                except Exception as ex_single:
                    logger.error(f"Error enviando correo individual a {recipient}: {ex_single}")
                    print(f"[EMAIL_ERROR_INDIVIDUAL] {recipient}: {ex_single}")
        except Exception as e:
            logger.error(f"Fallo general en hilo de envio: {e}")
            print(f"[EMAIL_WORKER_ERROR] {e}")

    thread = threading.Thread(target=_worker, daemon=True)
    thread.start()


# ══════════════════════════════════════════════════════════════════════
# 1. BIENVENIDA Y CREDENCIALES
# ══════════════════════════════════════════════════════════════════════
def send_registration_email(user, password, student_code=None, role_label=None):
    """Envia credenciales de acceso al crear alumno o docente."""
    if not is_valid_recipient(user.email):
        return False

    nombre_completo = user.get_full_name() or user.username
    rol = role_label or user.get_role_display()
    usuario = user.username
    id_registro = student_code if student_code else usuario

    asunto = f"📋 Credenciales de Acceso al Sistema - ACADEMIX ({nombre_completo})"

    texto_plano = f"""Bienvenido(a) {nombre_completo} a ACADEMIX.

Rol asignado: {rol}
📋 Su número de registro / ID único: {id_registro}
👤 Su nombre de usuario: {usuario}
🔐 Su contraseña inicial: {password}

Acceso al sistema: http://localhost:8000/
"""

    texto_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 560px; margin: 0 auto; padding: 25px; border: 1px solid #e2e8f0; border-radius: 12px; background: #ffffff;">
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="display: inline-block; background: #1e3a8a; color: #ffffff; font-weight: 900; font-size: 20px; width: 44px; height: 44px; line-height: 44px; border-radius: 8px;">A</div>
            <h2 style="color: #1e3a8a; margin: 8px 0 0 0;">ACADEMIX</h2>
            <p style="color: #64748b; font-size: 13px; margin: 4px 0 0 0;">Sistema Integral de Gestión y Control Escolar</p>
        </div>
        <div style="background: #f8fafc; border-left: 4px solid #2563eb; padding: 14px 18px; border-radius: 6px; margin-bottom: 20px;">
            <h3 style="color: #0f172a; margin: 0 0 6px 0; font-size: 15px;">¡Bienvenido(a), {nombre_completo}!</h3>
            <p style="color: #475569; font-size: 13.5px; margin: 0;">Tu cuenta ha sido creada como <strong>{rol}</strong>. A continuación tus credenciales de ingreso:</p>
        </div>
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13.5px;">
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: 700; color: #334155;">📋 Su número de registro / ID único:</td>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-family: monospace; font-size: 14px; font-weight: 700; color: #2563eb;">{id_registro}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: 700; color: #334155;">👤 Su nombre de usuario:</td>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-family: monospace; font-size: 14px; font-weight: 700; color: #0f172a;">{usuario}</td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: 700; color: #334155;">🔐 Su contraseña inicial:</td>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-family: monospace; font-size: 14px; font-weight: 700; color: #0f172a;">{password}</td>
            </tr>
        </table>
        <div style="text-align: center; margin: 25px 0;">
            <a href="http://localhost:8000/" style="background: #2563eb; color: #ffffff; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 14px; display: inline-block;">Ingresar a ACADEMIX</a>
        </div>
    </div>
    """

    _send_async_mail(asunto, texto_plano, texto_html, [user.email])
    return True


# ══════════════════════════════════════════════════════════════════════
# 2. INASISTENCIAS / FALTAS DE ALUMNOS
# ══════════════════════════════════════════════════════════════════════
def send_absence_notification_email(student_profile, subject, session_date, status_display, justification=None):
    """Notifica al estudiante y su acudiente sobre una inasistencia o tardanza."""
    recipients = []
    if student_profile and student_profile.user and student_profile.user.email:
        recipients.append(student_profile.user.email)
    if student_profile and student_profile.parent and student_profile.parent.email:
        recipients.append(student_profile.parent.email)

    if not recipients:
        return

    student_name = student_profile.user.get_full_name()
    subject_name = getattr(subject, 'name', 'Asignatura')
    fecha_str = session_date.strftime('%d/%m/%Y') if hasattr(session_date, 'strftime') else str(session_date)

    asunto = f"⚠️ Notificación de Inasistencia - ACADEMIX ({student_name})"

    texto_plano = f"""Estimado(a) estudiante / Acudiente:

Se ha registrado una novedad de asistencia en el sistema ACADEMIX para el estudiante {student_name}:

• Asignatura: {subject_name}
• Fecha: {fecha_str}
• Novedad: {status_display}
{f'• Observación/Justificación: {justification}' if justification else ''}

Por favor verifique en la plataforma o contacte al docente para gestionar la justificación correspondiente.
http://localhost:8000/
"""

    texto_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 560px; margin: 0 auto; padding: 25px; border: 1px solid #fee2e2; border-radius: 12px; background: #ffffff;">
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="display: inline-block; background: #dc2626; color: #ffffff; font-weight: 900; font-size: 20px; width: 44px; height: 44px; line-height: 44px; border-radius: 8px;">⚠️</div>
            <h2 style="color: #991b1b; margin: 8px 0 0 0;">Reporte de Asistencia</h2>
            <p style="color: #64748b; font-size: 13px; margin: 4px 0 0 0;">Sistema de Control Escolar ACADEMIX</p>
        </div>
        <div style="background: #fef2f2; border-left: 4px solid #ef4444; padding: 14px 18px; border-radius: 6px; margin-bottom: 20px;">
            <p style="color: #991b1b; font-size: 14px; margin: 0; font-weight: 600;">
                Se ha registrado una inasistencia/tardanza para el estudiante <u>{student_name}</u>.
            </p>
        </div>
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13.5px;">
            <tr>
                <td style="padding: 9px; border-bottom: 1px solid #fecaca; font-weight: 700; color: #475569;">Estudiante:</td>
                <td style="padding: 9px; border-bottom: 1px solid #fecaca; font-weight: 700; color: #0f172a;">{student_name}</td>
            </tr>
            <tr>
                <td style="padding: 9px; border-bottom: 1px solid #fecaca; font-weight: 700; color: #475569;">Asignatura:</td>
                <td style="padding: 9px; border-bottom: 1px solid #fecaca; color: #1e3a8a; font-weight: 700;">{subject_name}</td>
            </tr>
            <tr>
                <td style="padding: 9px; border-bottom: 1px solid #fecaca; font-weight: 700; color: #475569;">Fecha:</td>
                <td style="padding: 9px; border-bottom: 1px solid #fecaca; color: #0f172a;">{fecha_str}</td>
            </tr>
            <tr>
                <td style="padding: 9px; border-bottom: 1px solid #fecaca; font-weight: 700; color: #475569;">Estado:</td>
                <td style="padding: 9px; border-bottom: 1px solid #fecaca; font-weight: 800; color: #dc2626;">{status_display}</td>
            </tr>
            {f'<tr><td style="padding: 9px; border-bottom: 1px solid #fecaca; font-weight: 700; color: #475569;">Observación:</td><td style="padding: 9px; border-bottom: 1px solid #fecaca; color: #475569;">{justification}</td></tr>' if justification else ''}
        </table>
        <div style="text-align: center; margin: 20px 0;">
            <a href="http://localhost:8000/" style="background: #dc2626; color: #ffffff; padding: 10px 24px; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 13px; display: inline-block;">Consultar Asistencias</a>
        </div>
    </div>
    """

    _send_async_mail(asunto, texto_plano, texto_html, recipients)


# ══════════════════════════════════════════════════════════════════════
# 3. TAREAS Y ACTIVIDADES ESCOLARES (SOLO ALUMNOS DEL CURSO)
# ══════════════════════════════════════════════════════════════════════
def send_homework_notification_email(homework):
    """
    Notifica la publicacion de una nueva tarea escolar.
    IMPORTANTE: Solo se envia a los estudiantes matriculados en el curso de la tarea.
    """
    from apps.students.models import Enrollment

    section = homework.course_section
    enrollments = Enrollment.objects.filter(
        course_section=section,
        status=Enrollment.Status.ACTIVE
    ).select_related('student__user', 'student__parent')

    recipients = []
    for enr in enrollments:
        if enr.student and enr.student.user and enr.student.user.email:
            recipients.append(enr.student.user.email)
        if enr.student and enr.student.parent and enr.student.parent.email:
            recipients.append(enr.student.parent.email)

    if not recipients:
        logger.info(f"Tarea {homework.title}: no hay alumnos con correo en el curso {section.name}")
        return

    subject_name = homework.subject.name
    teacher_name = homework.teacher.user.get_full_name() if homework.teacher else "Docente Titular"
    due_str = homework.due_date.strftime('%d/%m/%Y') if hasattr(homework.due_date, 'strftime') else str(homework.due_date)

    asunto = f"📚 Nueva Tarea: {homework.title} - {subject_name} ({section.name})"

    texto_plano = f"""Hola estudiante de {section.name}:

Se ha publicado una nueva actividad escolar en ACADEMIX:

• Curso: {section.name}
• Asignatura: {subject_name}
• Tarea: {homework.title}
• Docente: {teacher_name}
• Fecha límite de entrega: {due_str}

Instrucciones:
{homework.description}

Ingresa al sistema para ver los archivos adjuntos y subir tu entrega:
http://localhost:8000/homework/{homework.id}/submit/
"""

    texto_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 580px; margin: 0 auto; padding: 25px; border: 1px solid #e0e7ff; border-radius: 12px; background: #ffffff;">
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="display: inline-block; background: #4f46e5; color: #ffffff; font-weight: 900; font-size: 20px; width: 44px; height: 44px; line-height: 44px; border-radius: 8px;">📚</div>
            <h2 style="color: #3730a3; margin: 8px 0 0 0;">Nueva Tarea Escolar</h2>
            <p style="color: #64748b; font-size: 13px; margin: 4px 0 0 0;">Curso {section.name} • {subject_name}</p>
        </div>
        <div style="background: #eef2ff; border-left: 4px solid #6366f1; padding: 14px 18px; border-radius: 6px; margin-bottom: 20px;">
            <h3 style="color: #1e1b4b; margin: 0 0 6px 0; font-size: 16px;">{homework.title}</h3>
            <p style="color: #4338ca; font-size: 13px; margin: 0;">Asignada por el docente <strong>{teacher_name}</strong>.</p>
        </div>
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13.5px;">
            <tr>
                <td style="padding: 9px; border-bottom: 1px solid #e0e7ff; font-weight: 700; color: #475569;">Curso:</td>
                <td style="padding: 9px; border-bottom: 1px solid #e0e7ff; font-weight: 700; color: #1e293b;">{section.name}</td>
            </tr>
            <tr>
                <td style="padding: 9px; border-bottom: 1px solid #e0e7ff; font-weight: 700; color: #475569;">Asignatura:</td>
                <td style="padding: 9px; border-bottom: 1px solid #e0e7ff; font-weight: 700; color: #4338ca;">{subject_name}</td>
            </tr>
            <tr>
                <td style="padding: 9px; border-bottom: 1px solid #e0e7ff; font-weight: 700; color: #475569;">Fecha de Entrega:</td>
                <td style="padding: 9px; border-bottom: 1px solid #e0e7ff; font-weight: 800; color: #b91c1c;">📅 {due_str}</td>
            </tr>
        </table>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px; margin-bottom: 20px; font-size: 13px; color: #334155; line-height: 1.5;">
            <strong>Indicaciones:</strong><br>
            {homework.description}
        </div>
        <div style="text-align: center; margin: 25px 0;">
            <a href="http://localhost:8000/homework/{homework.id}/submit/" style="background: #4f46e5; color: #ffffff; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 14px; display: inline-block;">Ver Tarea y Subir Entrega</a>
        </div>
    </div>
    """

    _send_async_mail(asunto, texto_plano, texto_html, recipients)


# ══════════════════════════════════════════════════════════════════════
# 4. COMUNICADOS DE RECTORÍA Y SECRETARÍA (ESTUDIANTES Y/O DOCENTES)
# ══════════════════════════════════════════════════════════════════════
def send_institutional_activity_email(activity):
    """
    Notifica comunicados y actividades institucionales programadas por el Rector o Secretaria.
    Filtra segun el destinatario elegido (Estudiantes, Docentes o Toda la Comunidad).
    """
    from apps.accounts.models import CustomUser
    from apps.alerts.models import InstitutionalActivity

    recipients = []
    aud = activity.target_audience

    if aud in [InstitutionalActivity.TargetAudience.STUDENTS, InstitutionalActivity.TargetAudience.ALL]:
        students = CustomUser.objects.filter(role=CustomUser.Role.STUDENT, is_active=True).values_list('email', flat=True)
        recipients.extend(students)

    if aud in [InstitutionalActivity.TargetAudience.TEACHERS, InstitutionalActivity.TargetAudience.ALL]:
        teachers = CustomUser.objects.filter(role=CustomUser.Role.TEACHER, is_active=True).values_list('email', flat=True)
        recipients.extend(teachers)

    if aud in [InstitutionalActivity.TargetAudience.PARENTS, InstitutionalActivity.TargetAudience.ALL]:
        parents = CustomUser.objects.filter(role=CustomUser.Role.PARENT, is_active=True).values_list('email', flat=True)
        recipients.extend(parents)

    if not recipients:
        logger.info(f"Actividad {activity.title}: no hay usuarios con correo para la audiencia {aud}")
        return

    author_name = activity.created_by.get_full_name() if activity.created_by else "Rectoría / Secretaría"
    date_str = activity.event_date.strftime('%d/%m/%Y') if hasattr(activity.event_date, 'strftime') else str(activity.event_date)
    time_str = f" a las {activity.event_time.strftime('%H:%M')}" if activity.event_time else ""

    asunto = f"📢 Comunicado Institucional: {activity.title} - ACADEMIX"

    texto_plano = f"""Comunicado Oficial ACADEMIX:

{activity.title}
Publicado por: {author_name}
Dirigido a: {activity.get_target_audience_display()}

Fecha del Evento: {date_str}{time_str}
Lugar: {activity.location}

Detalles:
{activity.description}

Más información en la plataforma:
http://localhost:8000/alerts/activities/
"""

    texto_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 580px; margin: 0 auto; padding: 25px; border: 1px solid #bae6fd; border-radius: 12px; background: #ffffff;">
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="display: inline-block; background: #0284c7; color: #ffffff; font-weight: 900; font-size: 20px; width: 44px; height: 44px; line-height: 44px; border-radius: 8px;">📢</div>
            <h2 style="color: #0369a1; margin: 8px 0 0 0;">Comunicado Institucional</h2>
            <p style="color: #64748b; font-size: 13px; margin: 4px 0 0 0;">Rectoría y Dirección Escolar ACADEMIX</p>
        </div>
        <div style="background: #f0f9ff; border-left: 4px solid #0284c7; padding: 14px 18px; border-radius: 6px; margin-bottom: 20px;">
            <h3 style="color: #0c4a6e; margin: 0 0 6px 0; font-size: 16px;">{activity.title}</h3>
            <p style="color: #0369a1; font-size: 13px; margin: 0;">Publicado por: <strong>{author_name}</strong> • Dirigido a: <strong>{activity.get_target_audience_display()}</strong></p>
        </div>
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13.5px;">
            <tr>
                <td style="padding: 9px; border-bottom: 1px solid #e0f2fe; font-weight: 700; color: #475569;">Fecha:</td>
                <td style="padding: 9px; border-bottom: 1px solid #e0f2fe; font-weight: 700; color: #0284c7;">📅 {date_str}{time_str}</td>
            </tr>
            <tr>
                <td style="padding: 9px; border-bottom: 1px solid #e0f2fe; font-weight: 700; color: #475569;">Lugar:</td>
                <td style="padding: 9px; border-bottom: 1px solid #e0f2fe; color: #0f172a;">📍 {activity.location}</td>
            </tr>
        </table>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px; margin-bottom: 20px; font-size: 13.5px; color: #334155; line-height: 1.5;">
            {activity.description}
        </div>
        <div style="text-align: center; margin: 25px 0;">
            <a href="http://localhost:8000/alerts/activities/" style="background: #0284c7; color: #ffffff; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 14px; display: inline-block;">Ver Actividades en ACADEMIX</a>
        </div>
    </div>
    """

    _send_async_mail(asunto, texto_plano, texto_html, recipients)


# ══════════════════════════════════════════════════════════════════════
# 5. OBSERVADOR DISCIPLINARIO Y CITACIONES
# ══════════════════════════════════════════════════════════════════════
def send_discipline_annotation_email(anotacion):
    """Notifica al estudiante y su acudiente de una anotacion o situacion en el observador."""
    student_profile = anotacion.student_profile
    recipients = []
    if student_profile and student_profile.user and student_profile.user.email:
        recipients.append(student_profile.user.email)
    if student_profile and student_profile.parent and student_profile.parent.email:
        recipients.append(student_profile.parent.email)

    if not recipients:
        return

    student_name = student_profile.user.get_full_name()
    author_name = anotacion.author_user.get_full_name() if anotacion.author_user else "Docente / Directivo"

    asunto = f"📋 Notificación de Observador del Estudiante - ACADEMIX ({student_name})"

    texto_plano = f"""Estimado(a) estudiante / Acudiente:

Se ha registrado una situación en el Observador Estudiantil de {student_name}:

• Clasificación: {anotacion.get_fault_type_display()}
• Situación: {anotacion.title}
• Registrado por: {author_name}
• Compromiso: {anotacion.pedagogical_commitment or 'Seguimiento institucional'}

Detalles:
{anotacion.description}

Consulte el observador completo en:
http://localhost:8000/discipline/student/{student_profile.id}/
"""

    texto_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 560px; margin: 0 auto; padding: 25px; border: 1px solid #fef08a; border-radius: 12px; background: #ffffff;">
        <div style="text-align: center; margin-bottom: 20px;">
            <div style="display: inline-block; background: #ca8a04; color: #ffffff; font-weight: 900; font-size: 20px; width: 44px; height: 44px; line-height: 44px; border-radius: 8px;">📋</div>
            <h2 style="color: #854d0e; margin: 8px 0 0 0;">Observador del Estudiante</h2>
            <p style="color: #64748b; font-size: 13px; margin: 4px 0 0 0;">Registro de Convivencia y Seguimiento Pedagógico</p>
        </div>
        <div style="background: #fefce8; border-left: 4px solid #eab308; padding: 14px 18px; border-radius: 6px; margin-bottom: 20px;">
            <p style="color: #854d0e; font-size: 14px; margin: 0; font-weight: 600;">
                Se ha generado un registro para el estudiante <u>{student_name}</u> ({anotacion.get_fault_type_display()}).
            </p>
        </div>
        <table style="width: 100%; border-collapse: collapse; margin-bottom: 20px; font-size: 13.5px;">
            <tr>
                <td style="padding: 9px; border-bottom: 1px solid #fef08a; font-weight: 700; color: #475569;">Situación:</td>
                <td style="padding: 9px; border-bottom: 1px solid #fef08a; font-weight: 700; color: #0f172a;">{anotacion.title}</td>
            </tr>
            <tr>
                <td style="padding: 9px; border-bottom: 1px solid #fef08a; font-weight: 700; color: #475569;">Registrado por:</td>
                <td style="padding: 9px; border-bottom: 1px solid #fef08a; color: #475569;">{author_name}</td>
            </tr>
            {f'<tr><td style="padding: 9px; border-bottom: 1px solid #fef08a; font-weight: 700; color: #475569;">Compromiso:</td><td style="padding: 9px; border-bottom: 1px solid #fef08a; color: #0284c7; font-weight: 600;">{anotacion.pedagogical_commitment}</td></tr>' if anotacion.pedagogical_commitment else ''}
        </table>
        <div style="background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px; padding: 14px; margin-bottom: 20px; font-size: 13px; color: #334155; line-height: 1.5;">
            {anotacion.description}
        </div>
        <div style="text-align: center; margin: 20px 0;">
            <a href="http://localhost:8000/discipline/student/{student_profile.id}/" style="background: #ca8a04; color: #ffffff; padding: 10px 24px; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 13px; display: inline-block;">Consultar Observador</a>
        </div>
    </div>
    """

    _send_async_mail(asunto, texto_plano, texto_html, recipients)
