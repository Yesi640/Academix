from django.db.models import Q
from .models import SystemAlert

def get_active_alerts_for_user(user):
    """
    Recupera las alertas activas pertinentes para el usuario y su rol.
    """
    if not user.is_authenticated:
        return SystemAlert.objects.none()

    return SystemAlert.objects.filter(
        is_active=True
    ).filter(
        Q(recipient_user=user) |
        Q(target_role=user.role) |
        Q(recipient_user__isnull=True, target_role__isnull=True)
    ).order_by('-created_at')

def create_system_alert(title, message, level=SystemAlert.Level.INFO, recipient_user=None, target_role=None, is_dismissible=True):
    """
    Crea y despacha una nueva alerta en el sistema.
    """
    # Si es bloqueo, por regla no puede ser descartable
    if level == SystemAlert.Level.BLOCK:
        is_dismissible = False

    return SystemAlert.objects.create(
        title=title,
        message=message,
        level=level,
        recipient_user=recipient_user,
        target_role=target_role,
        is_dismissible=is_dismissible
    )

def schedule_institutional_activity(title, description, event_date, event_time=None, location='Instalaciones del Colegio', target_audience='ALL', created_by=None):
    """
    Registra una actividad institucional y despacha notificaciones automáticas inmediatas a los estudiantes y la comunidad.
    """
    from .models import InstitutionalActivity
    activity = InstitutionalActivity.objects.create(
        title=title,
        description=description,
        event_date=event_date,
        event_time=event_time,
        location=location,
        target_audience=target_audience,
        created_by=created_by,
        is_active=True
    )

    # Determinar rol destinatario para la notificación
    time_str = f" a las {event_time.strftime('%H:%M')}" if event_time else ""
    alert_msg = f"Fecha: {event_date}{time_str} | Lugar: {location}. {description}"

    if target_audience == InstitutionalActivity.TargetAudience.STUDENTS:
        roles_to_notify = ['STUDENT']
    elif target_audience == InstitutionalActivity.TargetAudience.TEACHERS:
        roles_to_notify = ['TEACHER']
    elif target_audience == InstitutionalActivity.TargetAudience.PARENTS:
        roles_to_notify = ['PARENT']
    else:
        # Toda la comunidad
        roles_to_notify = ['STUDENT', 'TEACHER', 'PARENT', 'SECRETARIA']

    for role in roles_to_notify:
        create_system_alert(
            title=f"📅 Actividad Institucional: {title}",
            message=alert_msg,
            level=SystemAlert.Level.INFO,
            target_role=role,
            is_dismissible=True
        )

    # Enviar notificaciones por correo institucional a la audiencia objetivo
    try:
        from apps.accounts.email_service import send_institutional_activity_email
        send_institutional_activity_email(activity)
    except Exception as _mail_err:
        pass

    return activity

