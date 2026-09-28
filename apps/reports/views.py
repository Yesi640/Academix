from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from .services import (
    build_student_bulletin_data,
    build_section_consolidated_data,
    export_consolidated_csv,
    build_honor_roll_data
)
from apps.courses.models import CourseSection
from apps.periods.models import AcademicPeriod
from apps.students.models import StudentProfile, Enrollment
from apps.courses.services import get_current_academic_year
from apps.periods.services import get_current_active_period
from apps.teachers.models import TeachingAssignment

@login_required
def reports_index_view(request):
    """
    Panel de selección de reportes institucionales, adaptado según el rol del usuario.
    """
    current_year = get_current_academic_year()
    active_period = get_current_active_period(current_year) if current_year else None
    periods = AcademicPeriod.objects.filter(academic_year=current_year).order_by('number') if current_year else []

    user = request.user
    if user.is_student and hasattr(user, 'student_profile'):
        enrollment = Enrollment.objects.filter(student=user.student_profile, academic_year=current_year).first()
        section = enrollment.course_section if enrollment else None
        return redirect('reports:student_bulletin', student_id=user.student_profile.id, period_id=active_period.id if active_period else 1)

    from apps.courses.models import InstitutionSetting
    inst_type = InstitutionSetting.get_settings().institution_type

    if user.is_teacher and hasattr(user, 'teacher_profile'):
        assignments = TeachingAssignment.objects.filter(teacher=user.teacher_profile, academic_year=current_year, is_active=True)
        sections = CourseSection.objects.filter(
            id__in=assignments.values_list('course_section_id', flat=True),
            grade_level__institution_type=inst_type
        ).distinct()
    else:
        sections = CourseSection.objects.filter(
            academic_year=current_year,
            grade_level__institution_type=inst_type
        ).select_related('grade_level') if current_year else []

    context = {
        'current_year': current_year,
        'active_period': active_period,
        'periods': periods,
        'sections': sections,
    }
    return render(request, 'reports/index.html', context)

@login_required
def student_bulletin_view(request, student_id, period_id):
    """
    Vista de visualización e impresión oficial del boletín de un estudiante.
    Incluye estilos CSS de alta fidelidad para impresión y exportación a PDF.
    """
    user = request.user
    student = get_object_or_404(StudentProfile, id=student_id)
    period = get_object_or_404(AcademicPeriod, id=period_id)

    # Control estricto de acceso por rol
    if user.is_student and hasattr(user, 'student_profile') and user.student_profile.id != student.id:
        return HttpResponseForbidden("No está autorizado para visualizar boletines de otros estudiantes.")

    # Alumnos y padres: solo pueden ver el boletín si el período está CERRADO o BLOQUEADO
    RESTRICTED_ROLES = user.is_student or user.is_parent
    PERIOD_OPEN = period.status not in ['CLOSED', 'LOCKED']
    if RESTRICTED_ROLES and PERIOD_OPEN:
        messages.warning(
            request,
            f'El boletín del período "{period.name}" aún no está disponible. '
            f'Solo podrá consultarlo una vez que el período sea cerrado oficialmente por la institución.'
        )
        return redirect('accounts:dashboard')

    enrollment = Enrollment.objects.filter(student=student, academic_year=period.academic_year).first()
    if not enrollment:
        messages.error(request, f'El estudiante {student.user.get_full_name()} no cuenta con matrícula activa para este periodo.')
        return redirect('reports:index')

    section = enrollment.course_section

    # Docentes que NO son director de grupo de este estudiante no pueden ver boletines
    if user.is_teacher and hasattr(user, 'teacher_profile'):
        from apps.teachers.models import TeachingAssignment
        is_dir = TeachingAssignment.objects.filter(
            teacher=user.teacher_profile,
            course_section=section,
            is_group_director=True,
            is_active=True
        ).exists()
        if not is_dir:
            messages.error(request, 'Solo el Director de Grupo puede consultar los boletines de este curso.')
            return redirect('teachers:my_courses')

    bulletin_data = build_student_bulletin_data(student, section, period)

    context = {
        'b': bulletin_data,
        'is_bulk': False,
    }
    return render(request, 'reports/bulletin_printable.html', context)

@login_required
def section_bulletins_bulk_view(request, section_id, period_id):
    """
    Genera en un solo documento continuo todos los boletines de una sección con saltos de página CSS.
    """
    user = request.user
    if user.is_student:
        return HttpResponseForbidden("Acceso denegado.")

    # Docentes: solo el director de grupo de ese curso puede ver/imprimir boletines masivos
    if user.is_teacher and hasattr(user, 'teacher_profile'):
        from apps.teachers.models import TeachingAssignment as TA
        is_dir = TA.objects.filter(
            teacher=user.teacher_profile,
            course_section_id=section_id,
            is_group_director=True,
            is_active=True
        ).exists()
        if not is_dir:
            messages.error(request, 'Solo el Director de Grupo puede imprimir boletines masivos de este curso.')
            return redirect('teachers:my_courses')

    section = get_object_or_404(CourseSection, id=section_id)
    period = get_object_or_404(AcademicPeriod, id=period_id)

    enrollments = Enrollment.objects.filter(
        course_section=section,
        academic_year=period.academic_year,
        status=Enrollment.Status.ACTIVE
    ).select_related('student__user').order_by('student__user__last_name', 'student__user__first_name')

    bulletins_list = []
    for enr in enrollments:
        data = build_student_bulletin_data(enr.student, section, period)
        bulletins_list.append(data)

    context = {
        'bulletins_list': bulletins_list,
        'section': section,
        'period': period,
        'is_bulk': True,
    }
    return render(request, 'reports/bulletin_printable.html', context)

@login_required
def section_consolidated_view(request):
    """
    Sábana consolidada de calificaciones de una sección escolar para el periodo seleccionado.
    """
    from apps.courses.models import InstitutionSetting
    inst_type = InstitutionSetting.get_settings().institution_type

    section_id = request.GET.get('section_id')
    period_id = request.GET.get('period_id')
    current_year = get_current_academic_year()
    periods = AcademicPeriod.objects.filter(academic_year=current_year).order_by('number') if current_year else []
    sections = CourseSection.objects.filter(
        academic_year=current_year,
        grade_level__institution_type=inst_type
    ).select_related('grade_level') if current_year else []

    if not section_id or not period_id:
        context = {
            'periods': periods,
            'sections': sections,
            'data': None,
        }
        return render(request, 'reports/consolidated.html', context)

    section = get_object_or_404(CourseSection, id=section_id, grade_level__institution_type=inst_type)
    period = get_object_or_404(AcademicPeriod, id=period_id)
    data = build_section_consolidated_data(section, period)

    context = {
        'periods': periods,
        'sections': sections,
        'selected_section': section,
        'selected_period': period,
        'data': data,
    }
    return render(request, 'reports/consolidated.html', context)

@login_required
def export_consolidated_csv_view(request, section_id, period_id):
    """
    Descarga la sábana consolidada en formato CSV con soporte UTF-8 BOM para Excel.
    """
    section = get_object_or_404(CourseSection, id=section_id)
    period = get_object_or_404(AcademicPeriod, id=period_id)

    csv_content = export_consolidated_csv(section, period)
    filename = f"Consolidado_{section.name.replace(' ', '_')}_{period.name.replace(' ', '_')}.csv"

    response = HttpResponse(csv_content, content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response

@login_required
def honor_roll_view(request):
    """
    Cuadro de honor con los mejores promedios y estadísticas directivas de rendimiento.
    """
    from apps.courses.models import InstitutionSetting
    inst_type = InstitutionSetting.get_settings().institution_type

    section_id = request.GET.get('section_id')
    period_id = request.GET.get('period_id')
    current_year = get_current_academic_year()
    periods = AcademicPeriod.objects.filter(academic_year=current_year).order_by('number') if current_year else []
    sections = CourseSection.objects.filter(
        academic_year=current_year,
        grade_level__institution_type=inst_type
    ).select_related('grade_level') if current_year else []

    if not section_id or not period_id:
        # Por defecto seleccionar primera sección y periodo activo
        active_period = get_current_active_period(current_year)
        section = sections.first() if sections.exists() else None
        period = active_period if active_period else (periods.first() if periods.exists() else None)
    else:
        section = get_object_or_404(CourseSection, id=section_id, grade_level__institution_type=inst_type)
        period = get_object_or_404(AcademicPeriod, id=period_id)

    data = build_honor_roll_data(section, period) if (section and period) else None

    context = {
        'periods': periods,
        'sections': sections,
        'selected_section': section,
        'selected_period': period,
        'data': data,
    }
    return render(request, 'reports/honor_roll.html', context)
