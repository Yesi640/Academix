from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import KnowledgeArea, Subject, GradeSubject
from apps.courses.models import GradeLevel

@login_required
def curriculum_view(request):
    """
    Vista de la malla curricular escolar e intensidades horarias.
    Acceso exclusivo para profesores (bloqueado para alumnos, padres de familia y secretarias).
    Garantiza que todos los cursos y asignaturas tengan configurada su intensidad horaria.
    """
    if request.user.is_student or request.user.is_parent or request.user.is_secretary:
        raise PermissionDenied("Acceso denegado: La Malla Curricular es de acceso exclusivo para profesores.")
    if not (request.user.is_teacher or request.user.is_admin_role or request.user.is_rector):
        raise PermissionDenied("Acceso denegado: La Malla Curricular es de acceso exclusivo para profesores.")

    from apps.courses.models import InstitutionSetting
    inst_type = InstitutionSetting.get_settings().institution_type

    areas = KnowledgeArea.objects.filter(institution_type=inst_type).prefetch_related('subjects')
    grades = GradeLevel.objects.filter(institution_type=inst_type).order_by('order')
    selected_grade_id = request.GET.get('grade')

    if selected_grade_id:
        active_grade = get_object_or_404(GradeLevel, id=selected_grade_id, institution_type=inst_type)
    else:
        active_grade = grades.first()



    grade_subjects = GradeSubject.objects.filter(
        grade_level=active_grade
    ).select_related('subject', 'subject__area').order_by('subject__area__order', 'subject__name') if active_grade else []

    context = {
        'areas': areas,
        'grades': grades,
        'active_grade': active_grade,
        'grade_subjects': grade_subjects,
    }
    return render(request, 'subjects/curriculum.html', context)

@login_required
def subjects_by_grade_partial(request):
    """
    Endpoint HTMX que retorna opciones <option> de asignaturas pertenecientes a un grado escolar.
    Utilizado en modales de asignación docente.
    """
    grade_id = request.GET.get('grade_id')
    subjects = []
    if grade_id:
        subjects = Subject.objects.filter(curriculum_grades__grade_level_id=grade_id).distinct()
    else:
        subjects = Subject.objects.all()

    return render(request, 'subjects/partials/subject_options.html', {'subjects': subjects})
