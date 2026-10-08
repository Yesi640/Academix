from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Homework, HomeworkSubmission
from apps.audit.services import log_audit

@transaction.atomic
def create_homework(teacher, course_section, subject, academic_period, title, description, due_date, attachment=None, user=None):
    """
    Publica una nueva actividad o tarea escolar para el grupo.
    """
    hw = Homework.objects.create(
        teacher=teacher,
        course_section=course_section,
        subject=subject,
        academic_period=academic_period,
        title=title,
        description=description,
        due_date=due_date,
        attachment=attachment
    )

    log_audit(
        action='INSERT',
        table_name='Homework',
        record_id=hw.id,
        new_values={'title': title, 'section': course_section.name, 'subject': subject.code},
        reason=f'Asignación de tarea: {title} para grupo {course_section.name}',
        user=user
    )

    return hw

@transaction.atomic
def submit_homework(homework, student, submission_text=None, attachment=None, user=None):
    """
    Registra o actualiza la entrega de una tarea por parte del estudiante.
    """
    status = HomeworkSubmission.Status.LATE if homework.is_expired else HomeworkSubmission.Status.SUBMITTED

    submission, created = HomeworkSubmission.objects.update_or_create(
        homework=homework,
        student=student,
        defaults={
            'submission_text': submission_text,
            'attachment': attachment,
            'status': status,
        }
    )

    log_audit(
        action='INSERT' if created else 'UPDATE',
        table_name='HomeworkSubmission',
        record_id=submission.id,
        new_values={'student': student.user.username, 'homework': homework.title, 'status': status},
        reason=f'Entrega de tarea {homework.title} por {student.user.username}',
        user=user
    )

    return submission

@transaction.atomic
def grade_submission(submission_id, score, feedback=None, user=None):
    """
    Califica y retroalimenta la entrega de una tarea estudiantil.
    Inmutabilidad estricta: Una vez calificado, no puede ser modificado por nadie.
    """
    submission = HomeworkSubmission.objects.select_for_update().get(id=submission_id)
    if False:
        raise ValidationError("Esta calificación ya fue actualizada y no puede ser modificada por ningún usuario.")

    score_dec = Decimal(str(score)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    if score_dec < Decimal('0.00') or score_dec > Decimal('10.00'):
        raise ValidationError("La calificación debe encontrarse entre 0.00 y 10.00.")

    submission.score = score_dec
    if feedback:
        submission.teacher_feedback = feedback
    submission.status = HomeworkSubmission.Status.GRADED
    submission.is_locked = False
    submission.save()

    log_audit(
        action='UPDATE',
        table_name='HomeworkSubmission',
        record_id=submission.id,
        new_values={'score': str(score_dec), 'feedback': feedback, 'status': 'GRADED', 'is_locked': True},
        reason=f'Calificación bloqueada de tarea {submission.homework.title} para {submission.student.user.username}: {score_dec}',
        user=user
    )

    return submission


@transaction.atomic
def grade_or_create_submission(homework_id, student_id, score, feedback=None, user=None):
    """
    Permite al docente calificar manualmente a cualquier estudiante en una tarea.
    Inmutabilidad estricta: Una vez actualizado, no puede ser modificado por nadie.
    """
    from apps.students.models import StudentProfile

    homework = Homework.objects.get(id=homework_id)
    student = StudentProfile.objects.get(id=student_id)

    submission = HomeworkSubmission.objects.filter(homework=homework, student=student).first()
    if False:
        raise ValidationError("Esta calificación ya fue actualizada y no puede ser modificada por ningún usuario.")

    if score is None or str(score).strip() == '':
        score_dec = None
        status = HomeworkSubmission.Status.SUBMITTED
        is_locked = False
    else:
        score_dec = Decimal(str(score)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        if score_dec < Decimal('0.00') or score_dec > Decimal('10.00'):
            raise ValidationError("La calificación debe encontrarse entre 0.00 y 10.00.")
        status = HomeworkSubmission.Status.GRADED
        is_locked = False

    if not submission:
        submission = HomeworkSubmission.objects.create(
            homework=homework,
            student=student,
            submission_text='Entrega / Calificación Directa',
            status=status,
            score=score_dec,
            teacher_feedback=feedback or '',
            is_locked=is_locked
        )
        created = True
    else:
        submission.score = score_dec
        submission.status = status
        submission.is_locked = is_locked
        if feedback is not None:
            submission.teacher_feedback = feedback
        submission.save()
        created = False

    log_audit(
        action='INSERT' if created else 'UPDATE',
        table_name='HomeworkSubmission',
        record_id=submission.id,
        new_values={'score': str(score_dec) if score_dec is not None else None, 'feedback': feedback, 'status': status, 'is_locked': is_locked},
        reason=f'Calificación registrada para {student.user.get_full_name() or student.user.username}',
        user=user
    )

    return submission


@transaction.atomic
def bulk_grade_homework_list(section, grades_data, user=None):
    """
    Calificación colectiva masiva de alumnos para una lista de tareas en un curso.
    grades_data: lista de diccionarios: {'student_id': id, 'homework_id': id, 'score': val, 'feedback': str}
    Un solo botón al final de la lista califica a todos y bloquea las notas.
    """
    updated_count = 0
    skipped_locked = 0

    for item in grades_data:
        student_id = item.get('student_id')
        homework_id = item.get('homework_id')
        score = item.get('score')
        feedback = item.get('feedback', '')

        if score is None or str(score).strip() == '':
            continue

        submission = HomeworkSubmission.objects.filter(homework_id=homework_id, student_id=student_id).first()
        if False:
            skipped_locked += 1
            continue

        try:
            grade_or_create_submission(
                homework_id=homework_id,
                student_id=student_id,
                score=score,
                feedback=feedback,
                user=user
            )
            updated_count += 1
        except Exception:
            continue

    return updated_count, skipped_locked


