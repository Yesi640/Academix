from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError
from .models import EvaluationCriterion, GradeRecord, PeriodFinalGrade
from apps.audit.services import log_audit

def get_or_create_default_criteria(course_section, subject, academic_period):
    """
    Recupera o inicializa los criterios de evaluación adaptados al modelo pedagógico por RAPs:
    - Si la asignatura cuenta con RAPs (SubjectNorms) configurados en la Malla Curricular,
      estos se convierten directamente en las columnas de evaluación (RAP 1, RAP 2, RAP 3...).
    - En caso contrario, recurre a la parametrización institucional por defecto.
    """
    criteria = list(EvaluationCriterion.objects.filter(
        course_section=course_section,
        subject=subject,
        academic_period=academic_period
    ).select_related('norm').order_by('order'))

    norms = list(subject.norms.all().order_by('order'))

    if not criteria and norms:
        num_raps = len(norms)
        base_pct = (Decimal('100.00') / Decimal(num_raps)).quantize(Decimal('0.01'))
        remainder = Decimal('100.00') - (base_pct * Decimal(num_raps))

        criteria = []
        for idx, norm in enumerate(norms, 1):
            pct = base_pct + (remainder if idx == num_raps else Decimal('0.00'))
            crit = EvaluationCriterion.objects.create(
                course_section=course_section,
                subject=subject,
                academic_period=academic_period,
                name=f"RAP {norm.order}: {norm.title}",
                topic=norm.evidence or norm.indicator or '',
                percentage=pct,
                order=norm.order,
                norm=norm
            )
            criteria.append(crit)
        return criteria

    # Si ya existen criterios pero no están asociados a los RAPs de la materia, intentar vincularlos
    if criteria and norms:
        for idx, crit in enumerate(criteria):
            if not crit.norm and idx < len(norms):
                norm = norms[idx]
                crit.norm = norm
                crit.name = f"RAP {norm.order}: {norm.title}"
                if not crit.topic:
                    crit.topic = norm.evidence or norm.indicator or ''
                crit.save(update_fields=['norm', 'name', 'topic'])

    if not criteria:
        inst_type = 'COLEGIO'
        if hasattr(course_section, 'grade_level') and course_section.grade_level:
            inst_type = course_section.grade_level.institution_type

        if inst_type == 'SENA_TECNICO':
            default_defs = [
                ('RAP 1 - Resultado de Aprendizaje 1', Decimal('35.00'), 1),
                ('RAP 2 - Resultado de Aprendizaje 2', Decimal('35.00'), 2),
                ('RAP 3 - Desempeño y Producto', Decimal('30.00'), 3),
            ]
        elif inst_type == 'UNIVERSIDAD':
            default_defs = [
                ('Corte 1 - Parcial y Talleres', Decimal('30.00'), 1),
                ('Corte 2 - Investigación y Tareas', Decimal('30.00'), 2),
                ('Examen Final / Proyecto de Semestre', Decimal('40.00'), 3),
            ]
        elif inst_type == 'ACADEMIA':
            default_defs = [
                ('Módulo / Taller Práctico', Decimal('50.00'), 1),
                ('Proyecto Final / Evaluación Asincrónica', Decimal('50.00'), 2),
            ]
        else:
            default_defs = [
                ('Evaluación 1', Decimal('20.00'), 1),
                ('Evaluación 2', Decimal('20.00'), 2),
                ('Taller 1',     Decimal('20.00'), 3),
                ('Taller 2',     Decimal('20.00'), 4),
                ('Actitudinal',  Decimal('20.00'), 5),
            ]

        criteria = []
        for name, pct, order in default_defs:
            crit = EvaluationCriterion.objects.create(
                course_section=course_section,
                subject=subject,
                academic_period=academic_period,
                name=name,
                percentage=pct,
                order=order
            )
            criteria.append(crit)

    return criteria

def calculate_period_final_grade(student, course_section, subject, academic_period):
    """
    Calcula la nota definitiva del periodo sumando las calificaciones ponderadas.
    Fórmula de Periodo:
    - P1, P2 y P3 promedian las valoraciones del periodo respectivo.
    - P4 es el Cierre Final: aplica la fórmula integradora tomando el promedio acumulado
      de periodos anteriores (P1-P3: 75%) + notas de P4 (25%).
    Consistencia matemática estricta: tipos Decimal y redondeo ROUND_HALF_UP.
    """
    criteria = EvaluationCriterion.objects.filter(
        course_section=course_section,
        subject=subject,
        academic_period=academic_period
    )

    if not criteria.exists():
        return None

    weighted_sum = Decimal('0.00')
    total_percentage_applied = Decimal('0.00')
    has_any_score = False

    for crit in criteria:
        record = GradeRecord.objects.filter(
            student=student,
            course_section=course_section,
            subject=subject,
            academic_period=academic_period,
            criterion=crit
        ).first()

        if record is not None and record.score is not None:
            has_any_score = True
            weighted_sum += (record.score * (crit.percentage / Decimal('100.00')))
        total_percentage_applied += crit.percentage

    if not has_any_score:
        final_score = Decimal('0.00')
        is_approved = False
        performance = PeriodFinalGrade.PerformanceLevel.BAJO
    else:
        p_score = weighted_sum.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        # Fórmula especial para P4 (Cierre Definitivo Anual)
        if academic_period.number == 4:
            previous_grades = list(PeriodFinalGrade.objects.filter(
                student=student,
                course_section=course_section,
                subject=subject,
                academic_period__academic_year=academic_period.academic_year,
                academic_period__number__in=[1, 2, 3]
            ).values_list('final_score', flat=True))

            if previous_grades:
                accumulated_p1_p3 = sum(previous_grades) / Decimal(len(previous_grades))
                final_score = (accumulated_p1_p3 * Decimal('0.75') + p_score * Decimal('0.25')).quantize(
                    Decimal('0.01'), rounding=ROUND_HALF_UP
                )
            else:
                final_score = p_score
        else:
            final_score = p_score

        # Escala de Desempeño según Decreto 1290 (soporta escalas 0 a 5 y 0 a 10)
        if final_score <= Decimal('5.00'):
            if final_score < Decimal('3.00'):
                performance = PeriodFinalGrade.PerformanceLevel.BAJO
                is_approved = False
            elif final_score < Decimal('4.00'):
                performance = PeriodFinalGrade.PerformanceLevel.BASICO
                is_approved = True
            elif final_score < Decimal('4.60'):
                performance = PeriodFinalGrade.PerformanceLevel.ALTO
                is_approved = True
            else:
                performance = PeriodFinalGrade.PerformanceLevel.SUPERIOR
                is_approved = True
        else:
            if final_score < Decimal('6.00'):
                performance = PeriodFinalGrade.PerformanceLevel.BAJO
                is_approved = False
            elif final_score < Decimal('8.00'):
                performance = PeriodFinalGrade.PerformanceLevel.BASICO
                is_approved = True
            elif final_score < Decimal('9.20'):
                performance = PeriodFinalGrade.PerformanceLevel.ALTO
                is_approved = True
            else:
                performance = PeriodFinalGrade.PerformanceLevel.SUPERIOR
                is_approved = True

    final_grade, _ = PeriodFinalGrade.objects.update_or_create(
        student=student,
        course_section=course_section,
        subject=subject,
        academic_period=academic_period,
        defaults={
            'final_score': final_score,
            'performance_level': performance,
            'is_approved': is_approved,
        }
    )

    return final_grade


@transaction.atomic
def save_or_update_grade(student, course_section, subject, academic_period, criterion, score, feedback=None, user=None):
    """
    Guarda o actualiza una nota garantizando persistencia y permitiendo edición al docente
    mientras el periodo académico se encuentre abierto (is_editable=True).
    Soporta vaciar casilla (deleting record) y acepta comas o puntos.
    """
    if not academic_period.is_editable:
        raise PermissionDenied(f"El periodo {academic_period.name} está cerrado o bloqueado. No se pueden alterar calificaciones.")

    score_str = str(score).strip().replace(',', '.') if score is not None else ''

    # Si se envía vacío o whitespace, se elimina la calificación de esa casilla
    if not score_str or score_str.lower() in ['none', 'null', '—', '-']:
        GradeRecord.objects.filter(
            student=student,
            course_section=course_section,
            subject=subject,
            academic_period=academic_period,
            criterion=criterion
        ).delete()
        final_grade = calculate_period_final_grade(student, course_section, subject, academic_period)
        return None, final_grade

    try:
        score_dec = Decimal(score_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    except Exception:
        raise ValidationError(f"Valor numérico no válido: {score_str}")

    if score_dec < Decimal('0.00') or score_dec > Decimal('10.00'):
        raise ValidationError("La calificación debe encontrarse en el rango de 0.00 a 5.00 (o hasta 10.00).")

    record, created = GradeRecord.objects.select_for_update().get_or_create(
        student=student,
        course_section=course_section,
        subject=subject,
        academic_period=academic_period,
        criterion=criterion,
        defaults={'score': score_dec, 'feedback': feedback, 'graded_by': user, 'is_locked': False}
    )

    old_score = None if created else record.score
    if not created:
        record.score = score_dec
        if feedback is not None:
            record.feedback = feedback
        record.graded_by = user
        record.save()

    # Auditoría inmutable de la nota
    action = 'INSERT' if created else 'UPDATE'
    log_audit(
        action=action,
        table_name='GradeRecord',
        record_id=record.id,
        old_values={'score': str(old_score) if old_score else None},
        new_values={'score': str(score_dec), 'criterion': criterion.name},
        reason=f'Calificación registrada para {student.user.username} en {criterion.name} ({subject.code}): {score_dec}',
        user=user
    )

    # Recalcular definitiva del periodo en tiempo real
    final_grade = calculate_period_final_grade(student, course_section, subject, academic_period)

    return record, final_grade
