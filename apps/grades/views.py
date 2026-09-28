from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import EvaluationCriterion, GradeRecord, PeriodFinalGrade
from .services import (
    get_or_create_default_criteria,
    calculate_period_final_grade,
    save_or_update_grade
)
from apps.courses.models import CourseSection
from apps.subjects.models import Subject
from apps.periods.models import AcademicPeriod
from apps.students.models import StudentProfile, Enrollment
from apps.courses.services import get_current_academic_year
from apps.periods.services import get_current_active_period
from apps.teachers.models import TeachingAssignment

@login_required
def grades_index_view(request):
    """
    Selector de curso, asignatura y periodo para abrir la matriz de notas.
    Si el usuario es estudiante, muestra directamente su libreta de calificaciones personal.
    """
    current_year = get_current_academic_year()
    active_period = get_current_active_period(current_year) if current_year else None
    periods = AcademicPeriod.objects.filter(academic_year=current_year).order_by('number') if current_year else []

    # 1. Modo Estudiante: Consulta exclusiva y segura de sus propias calificaciones
    if request.user.is_student:
        student = getattr(request.user, 'student_profile', None)
        enrollment = Enrollment.objects.filter(
            student=student,
            academic_year=current_year,
            status=Enrollment.Status.ACTIVE
        ).select_related('course_section__grade_level').first() if student else None

        grades_data = []
        if enrollment and active_period:
            section = enrollment.course_section
            from apps.subjects.models import Subject
            # Buscar asignaturas que tengan criterios en este grupo y periodo
            criteria_subjs = EvaluationCriterion.objects.filter(
                course_section=section,
                academic_period=active_period
            ).values_list('subject_id', flat=True).distinct()
            subjects = Subject.objects.filter(id__in=criteria_subjs)
            if not subjects.exists():
                subjects = Subject.objects.all()

            for subj in subjects:
                criteria = EvaluationCriterion.objects.filter(
                    course_section=section,
                    subject=subj,
                    academic_period=active_period
                ).order_by('order')

                scores_list = []
                for crit in criteria:
                    rec = GradeRecord.objects.filter(
                        student=student,
                        course_section=section,
                        subject=subj,
                        academic_period=active_period,
                        criterion=crit
                    ).first()
                    scores_list.append({
                        'criterion': crit,
                        'score': rec.score if rec else None,
                        'feedback': rec.feedback if rec else None
                    })

                final_grade = PeriodFinalGrade.objects.filter(
                    student=student,
                    course_section=section,
                    subject=subj,
                    academic_period=active_period
                ).first()

                grades_data.append({
                    'subject': subj,
                    'scores': scores_list,
                    'final_grade': final_grade,
                })

        return render(request, 'grades/student_grades.html', {
            'enrollment': enrollment,
            'active_period': active_period,
            'current_year': current_year,
            'grades_data': grades_data,
            'student': student,
        })

    # 1.1 Modo Padre de Familia (Solo Lectura Estricto)
    if request.user.is_parent:
        children = StudentProfile.objects.filter(parent=request.user).select_related('user')
        child_id = request.GET.get('student_id')
        student = children.filter(id=child_id).first() if child_id else children.first()
        enrollment = Enrollment.objects.filter(
            student=student,
            academic_year=current_year,
            status=Enrollment.Status.ACTIVE
        ).select_related('course_section__grade_level').first() if student else None

        grades_data = []
        if enrollment and active_period:
            section = enrollment.course_section
            from apps.subjects.models import Subject
            criteria_subjs = EvaluationCriterion.objects.filter(
                course_section=section,
                academic_period=active_period
            ).values_list('subject_id', flat=True).distinct()
            subjects = Subject.objects.filter(id__in=criteria_subjs)
            if not subjects.exists():
                subjects = Subject.objects.all()

            for subj in subjects:
                criteria = EvaluationCriterion.objects.filter(
                    course_section=section,
                    subject=subj,
                    academic_period=active_period
                ).order_by('order')

                scores_list = []
                for crit in criteria:
                    rec = GradeRecord.objects.filter(
                        student=student,
                        course_section=section,
                        subject=subj,
                        academic_period=active_period,
                        criterion=crit
                    ).first()
                    scores_list.append({
                        'criterion': crit,
                        'score': rec.score if rec else None,
                        'feedback': rec.feedback if rec else None
                    })

                final_grade = PeriodFinalGrade.objects.filter(
                    student=student,
                    course_section=section,
                    subject=subj,
                    academic_period=active_period
                ).first()

                grades_data.append({
                    'subject': subj,
                    'scores': scores_list,
                    'final_grade': final_grade,
                })

        return render(request, 'grades/student_grades.html', {
            'enrollment': enrollment,
            'active_period': active_period,
            'current_year': current_year,
            'grades_data': grades_data,
            'student': student,
            'children': children,
            'is_parent': True,
        })

    from apps.courses.models import InstitutionSetting
    inst_type = InstitutionSetting.get_settings().institution_type

    # 2. Modo Docente: Redirigir directamente a Mis Asignaciones (el módulo externo se integra en cada curso)
    if request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        return redirect('teachers:my_courses')

    # 3. Modo Directivo / Rector / Secretaría: Selector de asignación
    assignments = TeachingAssignment.objects.filter(
        academic_year=current_year,
        course_section__grade_level__institution_type=inst_type,
        is_active=True
    ).select_related('course_section', 'subject')
    sections = CourseSection.objects.filter(
        academic_year=current_year,
        grade_level__institution_type=inst_type
    ).select_related('grade_level') if current_year else []

    context = {
        'current_year': current_year,
        'active_period': active_period,
        'periods': periods,
        'sections': sections,
        'assignments': assignments,
    }
    return render(request, 'grades/index.html', context)

@login_required
def grades_matrix_view(request):
    """
    Matriz interactiva de calificaciones para una asignatura, grupo y periodo.
    Estudiantes y padres tienen prohibido el acceso a la matriz global.
    Secretaría tiene acceso de solo lectura (no editable).
    Docentes solo pueden editar sus propias asignaciones.
    """
    if request.user.is_student or request.user.is_parent:
        messages.error(request, 'No está autorizado para consultar planillas globales de otros estudiantes.')
        return redirect('grades:index')

    section_id = request.GET.get('section_id')
    subject_id = request.GET.get('subject_id')
    period_id = request.GET.get('period_id')

    if not section_id or not subject_id or not period_id:
        messages.warning(request, 'Por favor seleccione grupo, asignatura y periodo.')
        return redirect('grades:index')

    section = get_object_or_404(CourseSection, id=section_id)
    subject = get_object_or_404(Subject, id=subject_id)
    period = get_object_or_404(AcademicPeriod, id=period_id)

    # Secretaría solo lectura; Docente verifica asignación
    is_editable = period.is_editable
    if request.user.is_secretary:
        is_editable = False
    elif request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        has_assignment = TeachingAssignment.objects.filter(
            teacher=request.user.teacher_profile,
            course_section=section,
            subject=subject,
            academic_year=section.academic_year,
            is_active=True
        ).exists()
        if not has_assignment:
            is_editable = False

    criteria = get_or_create_default_criteria(section, subject, period)

    # Estudiantes matriculados activos
    enrollments = Enrollment.objects.filter(
        course_section=section,
        academic_year=section.academic_year,
        status=Enrollment.Status.ACTIVE
    ).select_related('student__user').order_by('student__user__last_name', 'student__user__first_name')

    matrix_rows = []
    for enr in enrollments:
        student = enr.student
        scores_by_criterion = []
        for crit in criteria:
            rec = GradeRecord.objects.filter(
                student=student,
                course_section=section,
                subject=subject,
                academic_period=period,
                criterion=crit
            ).first()
            scores_by_criterion.append({
                'criterion': crit,
                'record': rec,
                'score': rec.score if rec else None
            })

        final_grade = calculate_period_final_grade(student, section, subject, period)
        matrix_rows.append({
            'student': student,
            'scores': scores_by_criterion,
            'final_grade': final_grade,
        })

    # Cálculo del Área de Indicadores (KPIs en tiempo real)
    total_students = len(matrix_rows)
    final_grades_list = [r['final_grade'].final_score for r in matrix_rows if r.get('final_grade') and r['final_grade'].final_score > Decimal('0.00')]
    if final_grades_list and len(final_grades_list) > 0:
        from decimal import ROUND_HALF_UP
        group_average = (sum(final_grades_list) / Decimal(len(final_grades_list))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        approved_count = sum(1 for r in matrix_rows if r.get('final_grade') and r['final_grade'].is_approved)
        failed_count = sum(1 for r in matrix_rows if r.get('final_grade') and not r['final_grade'].is_approved and r['final_grade'].final_score > Decimal('0.00'))
        at_risk_count = sum(1 for r in matrix_rows if r.get('final_grade') and Decimal('0.00') < r['final_grade'].final_score < Decimal('3.00'))
    else:
        group_average = Decimal('0.00')
        approved_count = 0
        failed_count = 0
        at_risk_count = 0

    total_cells = total_students * len(criteria) if criteria else 0
    filled_cells = sum(1 for r in matrix_rows for s in r['scores'] if s.get('record') is not None)
    completion_percentage = int((filled_cells / total_cells * 100)) if total_cells > 0 else 0

    kpis = {
        'total_students': total_students,
        'group_average': group_average,
        'approved_count': approved_count,
        'failed_count': failed_count,
        'at_risk_count': at_risk_count,
        'completion_percentage': completion_percentage,
    }

    context = {
        'section': section,
        'subject': subject,
        'period': period,
        'criteria': criteria,
        'matrix_rows': matrix_rows,
        'is_editable': is_editable,
        'kpis': kpis,
    }
    return render(request, 'grades/matrix.html', context)

@login_required
def update_score_inline_view(request):
    """
    Endpoint para autoguardado en línea de calificaciones individuales.
    Soporta JSON para actualización reactiva fluida sin destruir inputs del DOM
    y sin que los números se borren o desaparezcan.
    """
    from django.http import JsonResponse

    if request.method == 'POST':
        # Bloquear inmediatamente roles no autorizados
        if request.user.is_secretary or request.user.is_student or request.user.is_parent:
            err_msg = 'No tiene permisos para modificar calificaciones.'
            if request.headers.get('Accept') == 'application/json' or not request.headers.get('HX-Request'):
                return JsonResponse({'status': 'error', 'message': err_msg}, status=403)
            return HttpResponse(f'<div class="text-danger small fw-bold">{err_msg}</div>', status=403)

        student_id = request.POST.get('student_id')
        section_id = request.POST.get('section_id')
        subject_id = request.POST.get('subject_id')
        period_id = request.POST.get('period_id')
        criterion_id = request.POST.get('criterion_id')
        score_val = request.POST.get('score', '').strip()

        student = get_object_or_404(StudentProfile, id=student_id)
        section = get_object_or_404(CourseSection, id=section_id)
        subject = get_object_or_404(Subject, id=subject_id)
        period = get_object_or_404(AcademicPeriod, id=period_id)
        criterion = get_object_or_404(EvaluationCriterion, id=criterion_id)

        # Si es docente, verificar asignación obligatoria
        if request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
            has_assignment = TeachingAssignment.objects.filter(
                teacher=request.user.teacher_profile,
                course_section=section,
                subject=subject,
                academic_year=section.academic_year,
                is_active=True
            ).exists()
            if not has_assignment and not (request.user.is_admin_role or request.user.is_rector):
                err_msg = 'No está asignado como docente de esta materia.'
                if request.headers.get('Accept') == 'application/json' or not request.headers.get('HX-Request'):
                    return JsonResponse({'status': 'error', 'message': err_msg}, status=403)
                return HttpResponse(f'<div class="text-danger small fw-bold">{err_msg}</div>', status=403)

        try:
            record, final_grade = save_or_update_grade(
                student=student,
                course_section=section,
                subject=subject,
                academic_period=period,
                criterion=criterion,
                score=score_val,
                user=request.user
            )
        except Exception as e:
            if request.headers.get('Accept') == 'application/json' or not request.headers.get('HX-Request'):
                return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
            return HttpResponse(f'<div class="text-danger small">{str(e)}</div>', status=400)

        # Calcular métricas actualizadas del grupo
        from decimal import Decimal, ROUND_HALF_UP
        all_final_grades = PeriodFinalGrade.objects.filter(
            course_section=section,
            subject=subject,
            academic_period=period
        )
        scores_list = [g.final_score for g in all_final_grades if g.final_score > Decimal('0.00')]
        if scores_list:
            group_avg = (sum(scores_list) / Decimal(len(scores_list))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            approved = sum(1 for g in all_final_grades if g.is_approved)
            failed = sum(1 for g in all_final_grades if not g.is_approved and g.final_score > Decimal('0.00'))
        else:
            group_avg = Decimal('0.00')
            approved = 0
            failed = 0

        # Respuesta JSON estándar para fetch / AJAX (evita parpadeos y desaparición de datos)
        if request.headers.get('Accept') == 'application/json' or not request.headers.get('HX-Request'):
            return JsonResponse({
                'status': 'success',
                'student_id': student.id,
                'criterion_id': criterion.id,
                'score': str(record.score) if record else '',
                'final_score': str(final_grade.final_score) if final_grade and final_grade.final_score > Decimal('0.00') else '—',
                'is_approved': final_grade.is_approved if final_grade else False,
                'performance_level': final_grade.get_performance_level_display() if final_grade and final_grade.final_score > Decimal('0.00') else 'Sin Nota',
                'badge_class': final_grade.badge_class if final_grade and final_grade.final_score > Decimal('0.00') else 'bg-secondary text-white',
                'kpis': {
                    'group_average': str(group_avg),
                    'approved_count': approved,
                    'failed_count': failed,
                }
            })

        # Reconstruir datos de la fila si la petición fue hecha con HTMX puro
        criteria = get_or_create_default_criteria(section, subject, period)
        scores_by_criterion = []
        for crit in criteria:
            rec = GradeRecord.objects.filter(
                student=student,
                course_section=section,
                subject=subject,
                academic_period=period,
                criterion=crit
            ).first()
            scores_by_criterion.append({
                'criterion': crit,
                'record': rec,
                'score': rec.score if rec else None
            })

        row_data = {
            'student': student,
            'scores': scores_by_criterion,
            'final_grade': final_grade,
        }

        context = {
            'row': row_data,
            'section': section,
            'subject': subject,
            'period': period,
            'criteria': criteria,
            'is_editable': period.is_editable,
        }
        return render(request, 'grades/partials/grade_row.html', context)

    return HttpResponse(status=405)
