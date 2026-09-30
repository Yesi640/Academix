from django.db.models import Q
from .models import AuditLog

def get_audit_trail_for_entity(table_name, record_id=None, limit=50):
    """
    Recupera el historial de auditoría cronológico para una tabla o registro específico.
    """
    qs = AuditLog.objects.filter(table_name=table_name)
    if record_id is not None:
        qs = qs.filter(record_id=str(record_id))
    return qs.select_related('user').order_by('-timestamp')[:limit]

def get_audit_trail_for_user(user, limit=50):
    """
    Recupera todas las acciones de auditoría registradas por un usuario específico.
    """
    return AuditLog.objects.filter(user=user).order_by('-timestamp')[:limit]

def get_critical_audit_logs(limit=100):
    """
    Retorna logs de alta criticidad: Modificaciones de notas, borrado de observaciones,
    cierres de periodos y alertas de seguridad.
    """
    critical_actions = [
        AuditLog.Action.GRADE_OVERRIDE,
        AuditLog.Action.OBSERVATION_DELETED,
        AuditLog.Action.PERIOD_CLOSE,
        AuditLog.Action.SECURITY_ALERT,
        AuditLog.Action.ENROLLMENT_ALTERED,
        AuditLog.Action.CONFIG_CHANGE,
    ]
    return AuditLog.objects.filter(action__in=critical_actions).select_related('user').order_by('-timestamp')[:limit]

def get_audit_trail_by_action(action, start_date=None, end_date=None, limit=100):
    """
    Filtra eventos de auditoría por tipo de acción y rango de fechas opcional.
    """
    qs = AuditLog.objects.filter(action=action)
    if start_date:
        qs = qs.filter(timestamp__gte=start_date)
    if end_date:
        qs = qs.filter(timestamp__lte=end_date)
    return qs.select_related('user').order_by('-timestamp')[:limit]
