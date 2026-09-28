from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from django.core.exceptions import ValidationError, PermissionDenied
from .models import AttendanceSession, AttendanceRecord
from apps.periods.models import AcademicPeriod
from apps.periods.services import get_current_active_period
from apps.courses.models import CourseSection
from apps.subjects.models import Subject
from apps.students.models import StudentProfile, Enrollment
from apps.alerts.models import SystemAlert
from apps.alerts.services import create_system_alert
from apps.audit.services import log_audit

def calculate_student_absence_stats(student_profile, subject, academic_period):
    """
    Calcula el ausentismo exacto con precisión Decimal para un estudiante, asignatura y periodo.
    Retorna el porcentaje y el nivel del semáforo institucional:
    - 🟢 Normal: < 10%
    - 🟡 Advertencia: 10% a 19.99%
    - 🔴 Bloqueo / Riesgo de Reprobación: >= 20%
    """
    records = AttendanceRecord.objects.filter(
        student=student_profile,
        session__subject=subject,
        session__academic_period=academic_period
    ).select_related('session')

    total_sessions = records.count()
    if total_sessions == 0:
        return {
            'total_sessions': 0,
            'total_hours': 0,
            'present_count': 0,
            'unjustified_hours': 0,
            'justified_hours': 0,
            'late_count': 0,
            'absence_percentage': Decimal('0.00'),
            'semaphore': 'GREEN',
            'semaphore_badge': 'bg-success text-white',
            'semaphore_label': 'Normal',
            'is_blocked': False,
        }

    total_hours = sum(r.session.hours_count for r in records)
    unjustified_hours = sum(r.session.hours_count for r in records if r.status == AttendanceRecord.Status.UNJUSTIFIED)
    justified_hours = sum(r.session.hours_count for r in records if r.status == AttendanceRecord.Status.JUSTIFIED)
    late_count = sum(1 for r in records if r.status == AttendanceRecord.Status.LATE)

    # Fórmula institucional:
    # Ausentismo equivalente = Faltas injustificadas + (0.33 * Tardanzas) + (0.5 * Justificadas)
    equivalent_absent_hours = Decimal(str(unjustified_hours)) + (Decimal(str(late_count)) * Decimal('0.33')) + (Decimal(str(justified_hours)) * Decimal('0.50'))
    
    if total_hours > 0:
        pct = (equivalent_absent_hours / Decimal(str(total_hours))) * Decimal('100.00')
        percentage = pct.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    else:
        percentage = Decimal('0.00')

    # Semáforo
    if percentage >= Decimal('20.00'):
        semaphore = 'RED'
        badge = 'bg-danger text-white'
        label = '🔴 Riesgo Pérdida (≥20%)'
        is_blocked = True
    elif percentage >= Decimal('10.00'):
        semaphore = 'YELLOW'
        badge = 'bg-warning text-dark'
        label = '🟡 Advertencia (≥10%)'
        is_blocked = False
    else:
        semaphore = 'GREEN'
        badge = 'bg-success text-white'
        label = '🟢 Normal'
        is_blocked = False

    present_count = sum(1 for r in records if r.status == AttendanceRecord.Status.PRESENT)

    return {
        'total_sessions': total_sessions,
        'total_hours': total_hours,
        'present_count': present_count,
        'unjustified_hours': unjustified_hours,
        'justified_hours': justified_hours,
        'late_count': late_count,
        'absence_percentage': percentage,
        'semaphore': semaphore,
        'semaphore_badge': badge,
        'semaphore_label': label,
        'is_blocked': is_blocked,
    }

@transaction.atomic
def get_or_create_attendance_session(course_section, subject, session_date, recorded_by=None, hours_count=1):
    """
    Obtiene o crea una sesión de clase y asegura que todos los alumnos matriculados
    tengan su registro individual inicializado.
    """
    session = AttendanceSession.objects.filter(
        course_section=course_section,
        subject=subject,
        date=session_date
    ).select_related('academic_period').first()

    if not session:
        academic_period = get_current_active_period(course_section.academic_year)
        if not academic_period:
            raise ValidationError("No existe ningún periodo académico activo para registrar asistencia.")

        if not academic_period.is_editable:
            raise PermissionDenied(f"El periodo {academic_period.name} se encuentra cerrado o bloqueado.")

        session, created = AttendanceSession.objects.get_or_create(
            course_section=course_section,
            subject=subject,
            date=session_date,
            academic_period=academic_period,
            defaults={
                'hours_count': hours_count,
                'recorded_by': recorded_by,
            }
        )

    # Poblar registros para todos los alumnos matriculados que falten
    enrolled_students = StudentProfile.objects.filter(
        enrollments__course_section=course_section,
        enrollments__academic_year=course_section.academic_year,
        enrollments__status=Enrollment.Status.ACTIVE
    ).distinct()

    for student in enrolled_students:
        AttendanceRecord.objects.get_or_create(
            session=session,
            student=student,
            defaults={'status': AttendanceRecord.Status.UNJUSTIFIED}
        )

    return session

@transaction.atomic
def update_student_attendance(session, student, new_status, justification=None, user=None):
    """
    Actualiza el registro individual de asistencia de un estudiante con autoguardado en línea,
    auditoría inmutable y evaluación del semáforo de faltas.
    """
    if not session.academic_period.is_editable:
        raise PermissionDenied(f"No se pueden alterar asistencias: el periodo {session.academic_period.name} está cerrado.")

    record, _ = AttendanceRecord.objects.select_for_update().get_or_create(
        session=session,
        student=student
    )
    old_status = record.status
    record.status = new_status
    if justification:
        record.justification = justification
    record.save()

    # Auditoría inmutable
    log_audit(
        action='UPDATE',
        table_name='AttendanceRecord',
        record_id=record.id,
        old_values={'status': old_status},
        new_values={'status': new_status, 'justification': justification},
        reason=f'Asistencia actualizada para {student.user.username}: {new_status}',
        user=user
    )

    # Evaluar ausentismo y semáforo
    stats = calculate_student_absence_stats(student, session.subject, session.academic_period)

    # Emitir alerta si superó umbrales
    if stats['semaphore'] == 'RED':
        create_system_alert(
            title=f'🔴 ALERTA DE REPROBACIÓN POR INASISTENCIA: {student.user.get_full_name()}',
            message=f'El estudiante ha acumulado un {stats["absence_percentage"]}% de inasistencias en {session.subject.name} (Periodo {session.academic_period.number}). Se encuentra en causal de reprobación.',
            level=SystemAlert.Level.BLOCK,
            recipient_user=student.parent or student.user,
            target_role=None,
            is_dismissible=False
        )
    elif stats['semaphore'] == 'YELLOW':
        create_system_alert(
            title=f'🟡 AVISO DE AUSENTISMO: {student.user.get_full_name()}',
            message=f'El estudiante registra un {stats["absence_percentage"]}% de inasistencias en {session.subject.name}. Se recomienda contactar a acudiente.',
            level=SystemAlert.Level.WARNING,
            recipient_user=student.parent or student.user,
            target_role=None,
            is_dismissible=True
        )

    return record, stats

@transaction.atomic
def mark_all_session_present(session, user=None):
    """
    Marca masivamente a todos los estudiantes de la sesión como PRESENTES de manera atómica.
    """
    if not session.academic_period.is_editable:
        raise PermissionDenied("El periodo se encuentra cerrado.")

    session.records.update(status=AttendanceRecord.Status.PRESENT, is_justified=False)

    log_audit(
        action='UPDATE',
        table_name='AttendanceSession',
        record_id=session.id,
        new_values={'bulk_action': 'ALL_PRESENT'},
        reason=f'Marcado masivo de presentes en grupo {session.course_section.name} para {session.subject.name}',
        user=user
    )
    return session
