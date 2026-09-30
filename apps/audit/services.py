import json
from decimal import Decimal
from .models import AuditLog
from .middleware import get_current_user, get_current_ip, get_current_user_agent

def serialize_for_audit(data):
    """
    Serializa estructuras de datos u objetos a formato amigable JSON para auditoría.
    Protege información confidencial (passwords, tokens).
    """
    if data is None:
        return None
    if isinstance(data, dict):
        cleaned = {}
        for k, v in data.items():
            if any(secret_term in k.lower() for secret_term in ['password', 'secret', 'token', 'key']):
                cleaned[k] = '***PROTEGIDO***'
            elif isinstance(v, Decimal):
                cleaned[k] = str(v)
            elif not isinstance(v, (int, float, bool, str, type(None), list, dict)):
                cleaned[k] = str(v)
            else:
                cleaned[k] = v
        return cleaned
    return {'detail': str(data)}

def calculate_dict_diff(old_dict, new_dict):
    """
    Calcula los campos que cambiaron entre dos estados de un modelo.
    Retorna (diff_old, diff_new) con solo los valores modificados.
    """
    if not isinstance(old_dict, dict) or not isinstance(new_dict, dict):
        return old_dict, new_dict

    diff_old = {}
    diff_new = {}
    all_keys = set(old_dict.keys()).union(set(new_dict.keys()))

    for key in all_keys:
        val_old = old_dict.get(key)
        val_new = new_dict.get(key)
        if str(val_old) != str(val_new):
            diff_old[key] = val_old
            diff_new[key] = val_new

    return diff_old, diff_new

def log_audit(
    action,
    table_name,
    record_id=None,
    old_values=None,
    new_values=None,
    reason=None,
    user=None,
    ip=None,
    user_agent=None,
    request=None
):
    """
    Función de servicio centralizada para registrar eventos en la auditoría inmutable de ACADEMIX.
    Garantiza captura de usuario, IP, User Agent y valores previos/nuevos en formato JSON.
    """
    if user is None:
        user = get_current_user()

    if ip is None:
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
        else:
            ip = get_current_ip()

    if user_agent is None:
        if request:
            user_agent = request.META.get('HTTP_USER_AGENT', '')[:255]
        else:
            user_agent = get_current_user_agent()

    serialized_old = serialize_for_audit(old_values)
    serialized_new = serialize_for_audit(new_values)

    return AuditLog.objects.create(
        user=user if (user and user.is_authenticated) else None,
        action=action,
        table_name=table_name,
        record_id=str(record_id) if record_id is not None else None,
        old_values=serialized_old,
        new_values=serialized_new,
        ip_address=ip,
        user_agent=user_agent,
        reason=reason
    )

# Alias de nomenclatura de arquitectura
record_audit_event = log_audit

def audit_grade_change(grade_record_id, old_score, new_score, student_name, subject_code, criterion_name, reason=None, user=None):
    """
    Auditoría especializada de misión crítica para alteraciones en calificaciones de estudiantes.
    Registra quién, cuándo, nota anterior, nueva y motivo obligatorio o contextual.
    """
    return log_audit(
        action=AuditLog.Action.GRADE_OVERRIDE if old_score is not None else AuditLog.Action.INSERT,
        table_name='GradeRecord',
        record_id=grade_record_id,
        old_values={'score': str(old_score) if old_score is not None else None},
        new_values={'score': str(new_score), 'criterion': criterion_name, 'subject': subject_code},
        reason=reason or f'Calificación registrada/modificada para {student_name} en {criterion_name} ({subject_code}): {old_score} -> {new_score}',
        user=user
    )

def audit_observation_deletion(observation_id, student_name, author_name, content_snippet, reason, user=None):
    """
    Auditoría crítica para borrado de faltas disciplinarias u observaciones en el observador del alumno.
    """
    return log_audit(
        action=AuditLog.Action.OBSERVATION_DELETED,
        table_name='DisciplineRecord',
        record_id=observation_id,
        old_values={'student': student_name, 'author': author_name, 'snippet': content_snippet[:150]},
        new_values=None,
        reason=reason or 'Eliminación de anotación en el observador escolar',
        user=user
    )

def audit_official_export(report_type, filter_params, filename, user=None):
    """
    Auditoría de generación o exportación de archivos oficiales (SIMAT, Certificados, Sábanas).
    """
    return log_audit(
        action=AuditLog.Action.OFFICIAL_REPORT_EXPORT,
        table_name='OfficialReports',
        record_id=report_type,
        old_values=None,
        new_values={'filename': filename, 'filters': filter_params},
        reason=f'Exportación de documento oficial: {report_type} ({filename})',
        user=user
    )

def audit_security_event(event_description, details=None, user=None):
    """
    Auditoría de eventos de seguridad, accesos bloqueados o infracciones de reglas institucionales.
    """
    return log_audit(
        action=AuditLog.Action.SECURITY_ALERT,
        table_name='SecurityGateway',
        record_id=None,
        old_values=None,
        new_values=details,
        reason=event_description,
        user=user
    )
