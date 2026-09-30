from django.utils import timezone
from django.core.exceptions import PermissionDenied, ValidationError
from .models import AnotacionDisciplinaria
from apps.audit.services import log_audit
from apps.audit.models import AuditLog


def create_anotacion(
    student_profile,
    author_user,
    academic_year,
    title,
    description,
    fault_type=AnotacionDisciplinaria.FaultType.TIPO_I,
    period=None,
    date=None,
    time=None,
    location='Aula de Clase',
    student_disclaimer=None,
    pedagogical_commitment=None,
    parent_notified=False
):
    """
    Crea un nuevo registro en el Observador del Estudiante garantizando auditoría inmutable.
    """
    if not title or not description:
        raise ValidationError("El título y la descripción son obligatorios.")

    record = AnotacionDisciplinaria.objects.create(
        student=student_profile,
        author=author_user,
        academic_year=academic_year,
        period=period,
        fault_type=fault_type,
        date=date or timezone.now().date(),
        time=time,
        location=location or 'Aula de Clase',
        title=title.strip(),
        description=description.strip(),
        student_disclaimer=(student_disclaimer or '').strip() or None,
        pedagogical_commitment=(pedagogical_commitment or '').strip() or None,
        parent_notified=parent_notified,
        status=AnotacionDisciplinaria.Status.ABIERTA
    )

    log_audit(
        action=AuditLog.Action.CREATE,
        table_name='discipline_anotaciondisciplinaria',
        record_id=str(record.id),
        new_values={
            'student_id': student_profile.id,
            'student_name': student_profile.user.get_full_name(),
            'fault_type': fault_type,
            'title': title
        },
        user=author_user
    )
    return record


def add_student_disclaimer(record_id, disclaimer_text, user):
    """
    Permite consignar la versión o descargos del estudiante en respeto al debido proceso (Ley 1620).
    """
    record = AnotacionDisciplinaria.objects.get(id=record_id)
    if record.status in [AnotacionDisciplinaria.Status.CERRADA, AnotacionDisciplinaria.Status.ANULADA]:
        raise ValidationError("No se pueden agregar descargos a una anotación cerrada o anulada.")

    old_status = record.status
    record.student_disclaimer = disclaimer_text.strip()
    if record.status == AnotacionDisciplinaria.Status.ABIERTA and record.pedagogical_commitment:
        record.status = AnotacionDisciplinaria.Status.SEGUIMIENTO
    record.save(update_fields=['student_disclaimer', 'status', 'updated_at'])

    log_audit(
        action=AuditLog.Action.UPDATE,
        table_name='discipline_anotaciondisciplinaria',
        record_id=str(record.id),
        old_values={'status': old_status},
        new_values={'status': record.status, 'student_disclaimer': record.student_disclaimer},
        user=user
    )
    return record


def sign_parent_anotacion(record_id, parent_user, comments=None):
    """
    Registra la firma y enterado formal del acudiente/familia.
    """
    record = AnotacionDisciplinaria.objects.get(id=record_id)
    
    # Validar que sea el padre asignado o un directivo
    is_parent = (record.student.parent == parent_user)
    is_admin_directivo = (parent_user.is_superuser or parent_user.is_admin_role or parent_user.is_rector or parent_user.is_secretary)
    
    if not (is_parent or is_admin_directivo):
        raise PermissionDenied("Solo el acudiente registrado o la directiva puede firmar este llamado de atención.")

    record.parent_notified = True
    record.parent_acknowledged_at = timezone.now()
    record.parent_signature_name = parent_user.get_full_name() or parent_user.username
    if comments:
        record.parent_comments = comments.strip()
    record.save(update_fields=['parent_notified', 'parent_acknowledged_at', 'parent_signature_name', 'parent_comments', 'updated_at'])

    log_audit(
        action=AuditLog.Action.UPDATE,
        table_name='discipline_anotaciondisciplinaria',
        record_id=str(record.id),
        new_values={'parent_signature_name': record.parent_signature_name, 'signed_at': str(record.parent_acknowledged_at)},
        user=parent_user
    )
    return record


def close_anotacion(record_id, directivo_user, closing_notes=None):
    """
    Cierra formalmente la situación una vez verificado el cumplimiento de compromisos.
    """
    record = AnotacionDisciplinaria.objects.get(id=record_id)
    if not (directivo_user.is_superuser or directivo_user.is_admin_role or directivo_user.is_rector or directivo_user.is_secretary or directivo_user.is_teacher):
        raise PermissionDenied("No tiene permisos para cerrar anotaciones disciplinarias.")

    old_status = record.status
    record.status = AnotacionDisciplinaria.Status.CERRADA
    record.closed_at = timezone.now()
    record.closed_by = directivo_user
    if closing_notes:
        record.pedagogical_commitment = f"{record.pedagogical_commitment or ''}\n[Cierre por {directivo_user.get_full_name()}]: {closing_notes}".strip()
    record.save(update_fields=['status', 'closed_at', 'closed_by', 'pedagogical_commitment', 'updated_at'])

    log_audit(
        action=AuditLog.Action.UPDATE,
        table_name='discipline_anotaciondisciplinaria',
        record_id=str(record.id),
        old_values={'status': old_status},
        new_values={'status': record.status, 'closed_by': directivo_user.username},
        user=directivo_user
    )
    return record


def get_student_discipline_summary(student_profile, academic_year=None):
    """
    Obtiene el resumen y conteo estadístico de convivencia del alumno.
    """
    qs = student_profile.anotaciones_disciplinarias.all()
    if academic_year:
        qs = qs.filter(academic_year=academic_year)

    total = qs.count()
    tipo_1 = qs.filter(fault_type=AnotacionDisciplinaria.FaultType.TIPO_I).count()
    tipo_2 = qs.filter(fault_type=AnotacionDisciplinaria.FaultType.TIPO_II).count()
    tipo_3 = qs.filter(fault_type=AnotacionDisciplinaria.FaultType.TIPO_III).count()
    positivas = qs.filter(fault_type=AnotacionDisciplinaria.FaultType.POSITIVA).count()
    pendientes_firma = qs.filter(parent_acknowledged_at__isnull=True).exclude(fault_type=AnotacionDisciplinaria.FaultType.POSITIVA).count()

    return {
        'total': total,
        'tipo_1': tipo_1,
        'tipo_2': tipo_2,
        'tipo_3': tipo_3,
        'positivas': positivas,
        'pendientes_firma': pendientes_firma,
        'records': qs
    }
