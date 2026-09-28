from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import KnowledgeArea, Subject, GradeSubject, SubjectNorm
from apps.courses.models import GradeLevel, CourseSection, InstitutionSetting
from apps.teachers.models import TeachingAssignment
from apps.courses.services import get_current_academic_year

@login_required
def curriculum_view(request):
    """
    Vista de la Malla Curricular e Intensidades Horarias por Asignatura y Grado.
    Reglas de visibilidad:
    - Profesor de Grupo (Director de Grupo) y Equipo Directivo (Rector, Coordinador, Admin):
      Tienen acceso a la malla curricular completa (todas las áreas y asignaturas del colegio).
    - Docentes regulares (no directores de grupo):
      Solo pueden ver las áreas que tienen asignadas, sus asignaturas, las horas semanales
      que les tocan y el contenido curricular (descripción, estándares MEN, normas).
    - Al entrar en cada asignatura:
      Se despliega su Intensidad Horaria por Grado, las horas asignadas al docente y su contenido.
    """
    user = request.user
    if user.is_student or user.is_parent or user.is_secretary:
        raise PermissionDenied("Acceso denegado: La Malla Curricular es de acceso exclusivo para profesores y directivos.")

    if not (user.is_teacher or user.is_admin_role or user.is_rector or getattr(user, 'is_coordinator', False)):
        raise PermissionDenied("Acceso denegado: La Malla Curricular es de acceso exclusivo para profesores y directivos.")

    # Manejo de POST para registrar una nueva norma o competencia curricular
    if request.method == 'POST':
        subject_id = request.POST.get('subject_id')
        code = request.POST.get('code', '').strip()
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        order = request.POST.get('order', 1)

        if subject_id and code and title:
            subject = get_object_or_404(Subject, id=subject_id)
            try:
                order_val = int(order)
            except (ValueError, TypeError):
                order_val = 1
            SubjectNorm.objects.create(
                subject=subject,
                code=code,
                title=title,
                description=description,
                order=order_val
            )
            messages.success(request, f'Competencia / Norma "{code}" agregada correctamente a {subject.name}.')
            return redirect(f"{request.path}?subject={subject.id}")
        else:
            messages.error(request, 'El código y título de la norma son requeridos.')

    inst_type = InstitutionSetting.get_settings().institution_type
    current_year = get_current_academic_year()

    # 1. Determinar privilegios directivos o de Profesor de Grupo
    is_admin_or_rector = (
        user.is_superuser or
        user.is_admin_role or
        user.is_rector or
        getattr(user, 'is_coordinator', False) or
        getattr(user, 'role', '') in ['ADMIN', 'RECTOR', 'COORDINADOR']
    )

    # Identificar si es Director de Grupo (Profesor de Grupo)
    homeroom_section = CourseSection.objects.filter(
        homeroom_teacher=user,
        is_active=True
    ).select_related('grade_level', 'academic_year').first()

    if not homeroom_section:
        ta_dir = TeachingAssignment.objects.filter(
            teacher__user=user,
            is_group_director=True,
            is_active=True
        ).select_related('course_section__grade_level', 'course_section__academic_year').first()
        if ta_dir:
            homeroom_section = ta_dir.course_section

    is_group_director = homeroom_section is not None
    is_full_curriculum_viewer = is_admin_or_rector or is_group_director

    # 2. Consultar la carga académica del docente logueado
    teacher_assignments = TeachingAssignment.objects.filter(
        teacher__user=user,
        is_active=True
    ).select_related('course_section__grade_level', 'subject', 'subject__area')

    my_assigned_map = {}
    total_teacher_hours = 0
    assigned_grade_ids = set()

    for asg in teacher_assignments:
        s_id = asg.subject_id
        if s_id not in my_assigned_map:
            my_assigned_map[s_id] = {
                'subject_id': s_id,
                'sections': [],
                'total_hours': 0,
            }

        # Obtener intensidad horaria oficial para el grado de este curso
        gs = GradeSubject.objects.filter(
            grade_level=asg.course_section.grade_level,
            subject=asg.subject
        ).first()
        h = gs.weekly_hours if gs else 4

        my_assigned_map[s_id]['sections'].append({
            'section_id': asg.course_section_id,
            'section_name': asg.course_section.name,
            'grade_id': asg.course_section.grade_level_id,
            'grade_name': asg.course_section.grade_level.name,
            'hours': h,
            'is_group_director': asg.is_group_director,
        })
        my_assigned_map[s_id]['total_hours'] += h
        total_teacher_hours += h
        assigned_grade_ids.add(asg.course_section.grade_level_id)

    # 3. Filtrar Áreas y Asignaturas visibles según rol
    if is_full_curriculum_viewer:
        subjects_qs = Subject.objects.filter(
            institution_type=inst_type
        ).select_related('area').prefetch_related('norms', 'curriculum_grades__grade_level').order_by('area__order', 'category', 'name')

        areas_qs = KnowledgeArea.objects.filter(
            institution_type=inst_type
        ).prefetch_related('subjects').order_by('order', 'name')
    else:
        # Docente regular: solo ve sus asignaturas y sus áreas asignadas
        assigned_subj_ids = list(my_assigned_map.keys())
        subjects_qs = Subject.objects.filter(
            id__in=assigned_subj_ids,
            institution_type=inst_type
        ).select_related('area').prefetch_related('norms', 'curriculum_grades__grade_level').order_by('area__order', 'category', 'name')

        assigned_area_ids = subjects_qs.values_list('area_id', flat=True).distinct()
        areas_qs = KnowledgeArea.objects.filter(
            id__in=assigned_area_ids,
            institution_type=inst_type
        ).prefetch_related('subjects').order_by('order', 'name')

    # 4. Estructurar datos de cada asignatura con su intensidad horaria por grado y contenido
    subjects_list = []
    subject_lookup = {}
    for s in subjects_qs:
        curriculum_entries = []
        for cg in s.curriculum_grades.all().select_related('grade_level').order_by('grade_level__order'):
            curriculum_entries.append({
                'grade_id': cg.grade_level_id,
                'grade_name': cg.grade_level.name,
                'grade_code': cg.grade_level.code,
                'weekly_hours': cg.weekly_hours,
                'weight_percentage': cg.weight_percentage,
                'is_my_grade': cg.grade_level_id in assigned_grade_ids,
            })

        norms_list = []
        for norm in s.norms.all().order_by('order', 'code'):
            norms_list.append({
                'id': norm.id,
                'code': norm.code,
                'title': norm.title,
                'description': norm.description,
            })

        teacher_assigned_info = my_assigned_map.get(s.id, None)

        s_dict = {
            'id': s.id,
            'name': s.name,
            'code': s.code,
            'area_id': s.area_id,
            'area_name': s.area.name,
            'category': s.category,
            'category_display': s.get_category_display(),
            'description': s.description or 'Contenido curricular conforme a los lineamientos y estándares del MEN.',
            'curriculum': curriculum_entries,
            'norms': norms_list,
            'assigned_info': teacher_assigned_info,
            'is_assigned_to_me': teacher_assigned_info is not None,
        }
        subjects_list.append(s_dict)
        subject_lookup[s.id] = s_dict

    # Agrupar las asignaturas visibles por área para el panel izquierdo
    areas_data = []
    for area in areas_qs:
        area_subjs = [s for s in subjects_list if s['area_id'] == area.id]
        if area_subjs:
            areas_data.append({
                'id': area.id,
                'name': area.name,
                'order': area.order,
                'subjects': area_subjs,
                'subjects_count': len(area_subjs),
            })

    # Asignatura activa
    selected_subject_id = request.GET.get('subject')
    active_subject = None
    if selected_subject_id:
        try:
            active_subject = subject_lookup.get(int(selected_subject_id))
        except (ValueError, TypeError):
            pass

    if not active_subject and subjects_list:
        active_subject = subjects_list[0]

    # Para directivos / profesores de grupo: soporte opcional de vista de matriz por grado
    all_grades = GradeLevel.objects.filter(institution_type=inst_type).order_by('order')
    selected_grade_id = request.GET.get('grade')
    active_grade = None
    grade_subjects = []

    if is_full_curriculum_viewer:
        if selected_grade_id:
            active_grade = all_grades.filter(id=selected_grade_id).first()
        if not active_grade and homeroom_section:
            active_grade = homeroom_section.grade_level
        if not active_grade:
            active_grade = all_grades.first()

        if active_grade:
            grade_subjects = GradeSubject.objects.filter(
                grade_level=active_grade
            ).select_related('subject', 'subject__area').order_by('subject__area__order', 'subject__name')

    view_mode = request.GET.get('mode', 'subject')  # 'subject' o 'grade'

    context = {
        'is_full_curriculum_viewer': is_full_curriculum_viewer,
        'is_group_director': is_group_director,
        'is_admin_or_rector': is_admin_or_rector,
        'homeroom_section': homeroom_section,
        'total_teacher_hours': total_teacher_hours,
        'areas_data': areas_data,
        'subjects_list': subjects_list,
        'active_subject': active_subject,
        'grades': all_grades,
        'active_grade': active_grade,
        'grade_subjects': grade_subjects,
        'view_mode': view_mode,
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
