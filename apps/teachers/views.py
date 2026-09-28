import json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TeacherProfile, TeachingAssignment
from .services import assign_teacher_to_subject, get_or_create_teacher_profile
from apps.courses.models import CourseSection, AcademicYear
from apps.subjects.models import Subject
from apps.courses.services import get_current_academic_year

@login_required
def teachers_list_view(request):
    """
    Lista de docentes institucionales y gestión de carga académica para la institución activa.
    """
    import json
    from apps.courses.models import InstitutionSetting
    from apps.subjects.models import GradeSubject
    inst_type = InstitutionSetting.get_settings().institution_type

    current_year = get_current_academic_year()
    teachers = TeacherProfile.objects.select_related('user').all()
    assignments = TeachingAssignment.objects.filter(
        academic_year=current_year,
        course_section__grade_level__institution_type=inst_type
    ).select_related('teacher__user', 'course_section', 'subject') if current_year else []
    sections = CourseSection.objects.filter(
        academic_year=current_year,
        grade_level__institution_type=inst_type
    ).select_related('grade_level') if current_year else []
    subjects = Subject.objects.filter(institution_type=inst_type)

    # Mapa embebido: section_id -> lista de asignaturas del grado
    # Se carga una vez en el servidor y se pasa como JSON al template (sin AJAX)
    section_subjects_map = {}
    for sec in sections:
        gs_list = GradeSubject.objects.filter(
            grade_level=sec.grade_level
        ).select_related('subject__area').order_by(
            'subject__category', 'subject__area__order', 'subject__name'
        )
        subj_data = []
        if gs_list.exists():
            for gs in gs_list:
                s = gs.subject
                subj_data.append({
                    'id': s.id,
                    'name': s.name,
                    'code': s.code,
                    'area': s.area.name,
                    'category': s.get_category_display(),
                    'hours': gs.weekly_hours,
                })
        else:
            # Fallback: si no hay malla para ese grado, mostrar asignaturas de la institución
            for s in subjects.select_related('area').order_by('category', 'area__order', 'name'):
                subj_data.append({
                    'id': s.id,
                    'name': s.name,
                    'code': s.code,
                    'area': s.area.name,
                    'category': s.get_category_display(),
                    'hours': None,
                })

        section_subjects_map[str(sec.id)] = subj_data

    context = {
        'current_year': current_year,
        'teachers': teachers,
        'assignments': assignments,
        'sections': sections,
        'subjects': subjects,
        'section_subjects_map_json': json.dumps(section_subjects_map, ensure_ascii=True),
    }
    return render(request, 'teachers/list.html', context)

@login_required
def assign_teacher_view(request):
    """
    Crea o actualiza una asignación académica mediante formulario HTMX o POST tradicional.
    """
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        section_id = request.POST.get('section_id')
        subject_id = request.POST.get('subject_id')
        year_id = request.POST.get('academic_year_id')

        is_group_director = request.POST.get('is_group_director') in ['on', 'true', 'True', '1', True]

        teacher = get_object_or_404(TeacherProfile, id=teacher_id)
        section = get_object_or_404(CourseSection, id=section_id)
        subject = get_object_or_404(Subject, id=subject_id)
        academic_year = get_object_or_404(AcademicYear, id=year_id)

        try:
            assign_teacher_to_subject(
                teacher=teacher,
                course_section=section,
                subject=subject,
                academic_year=academic_year,
                is_group_director=is_group_director,
                user=request.user
            )
            director_txt = " (Designado como Director de Grupo)" if is_group_director else ""
            messages.success(request, f'Docente {teacher.user.get_full_name()} asignado a {subject.name} en {section.name}{director_txt}.')
        except Exception as e:
            messages.error(request, f'Error al asignar docente: {str(e)}')

    return redirect('teachers:list')


@login_required
def create_teacher_view(request):
    """
    Registra un nuevo docente en la planta institucional (Usuario y Perfil).
    Exclusivo para Directivos y Secretaría.
    """
    if not (request.user.is_admin_role or request.user.is_rector or request.user.is_secretary):
        messages.error(request, 'No tiene permisos para registrar nuevos docentes.')
        return redirect('teachers:list')

    if request.method == 'POST':
        from apps.accounts.models import CustomUser
        from apps.accounts.services import create_institutional_user
        from apps.audit.services import log_audit

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        doc_type = request.POST.get('document_type', 'CC')
        doc_num = request.POST.get('document_number', '').strip()
        specialty = request.POST.get('specialty', '').strip() or 'Docente de Área'
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        username = f"doc_{doc_num}" if doc_num else f"{first_name.lower()[:3]}{last_name.lower()[:3]}"
        if CustomUser.objects.filter(username=username).exists():
            username = f"{username}_{CustomUser.objects.count() + 1}"

        if not email:
            email = f"{username}@academix.edu.co"

        password = doc_num if doc_num else 'docente123'

        try:
            with __import__('django').db.transaction.atomic():
                user = create_institutional_user(
                    username=username,
                    email=email,
                    password=password,
                    role=CustomUser.Role.TEACHER,
                    document_type=doc_type,
                    document_number=doc_num,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone or None,
                    must_change_password=True
                )

                profile = get_or_create_teacher_profile(
                    user=user,
                    specialty=specialty
                )

                log_audit(
                    user=request.user,
                    action='CREATE_TEACHER',
                    table_name='TeacherProfile',
                    record_id=profile.id,
                    new_values={'username': username, 'specialty': specialty},
                    reason=f'Registro de nuevo docente por {request.user.username}',
                    request=request
                )

                messages.success(request, f'¡Docente {user.get_full_name()} registrado exitosamente! Usuario: {username} (Contraseña inicial: {password})')
        except Exception as e:
            messages.error(request, f'Error al registrar docente: {str(e)}')

    return redirect('teachers:list')


@login_required
def teacher_courses_view(request):
    """
    Vista principal "Mis Cursos" para el docente: listado de grupos asignados
    con acceso directo a su espacio de trabajo institucional.
    """
    from apps.courses.models import InstitutionSetting
    inst_type = InstitutionSetting.get_settings().institution_type
    current_year = get_current_academic_year()

    user = request.user
    if user.is_teacher and hasattr(user, 'teacher_profile'):
        assignments = TeachingAssignment.objects.filter(
            teacher=user.teacher_profile,
            academic_year=current_year,
            is_active=True
        ).select_related('course_section__grade_level', 'subject')

        section_ids = assignments.values_list('course_section_id', flat=True).distinct()
        sections = CourseSection.objects.filter(id__in=section_ids).select_related('grade_level')
    else:
        # Administradores y directivos pueden explorar todos los cursos
        sections = CourseSection.objects.filter(
            academic_year=current_year,
            grade_level__institution_type=inst_type
        ).select_related('grade_level')
        assignments = TeachingAssignment.objects.filter(academic_year=current_year).select_related('subject')

    courses_data = []
    for s in sections:
        sec_assignments = assignments.filter(course_section=s)
        student_count = s.enrollments.filter(status='ACTIVE').count()
        courses_data.append({
            'section': s,
            'assignments': sec_assignments,
            'subjects_count': sec_assignments.values('subject').distinct().count(),
            'students_count': student_count,
        })

    context = {
        'courses_data': courses_data,
        'current_year': current_year,
    }
    return render(request, 'teachers/my_courses.html', context)


@login_required
def course_workspace_view(request, section_id):
    """
    Espacio de trabajo del curso seleccionado con la Planilla de Notas integrada como primera opción:
    1. Planilla de Notas (Matriz interactiva, KPIs en vivo, persistencia y cambio ágil de materia/periodo)
    2. Asistencia (Llamado de lista y modificación en cualquier momento)
    3. Malla Curricular y Normas (Clasificación en Principales, Humanísticas y Arte/Deporte con RAPs/Estándares)
    """
    from apps.subjects.models import Subject, SubjectNorm, GradeSubject
    from apps.periods.models import AcademicPeriod
    from apps.periods.services import get_current_active_period
    from apps.attendance.models import AttendanceSession, AttendanceRecord
    import datetime

    section = get_object_or_404(CourseSection.objects.select_related('grade_level', 'academic_year'), id=section_id)
    current_year = section.academic_year
    active_period = get_current_active_period(current_year) if current_year else None
    user = request.user

    # Todos los cursos asignados al docente para el selector rápido superior (Curso A, Curso B, Curso C...)
    if user.is_teacher and hasattr(user, 'teacher_profile'):
        my_sec_ids = TeachingAssignment.objects.filter(
            teacher=user.teacher_profile,
            academic_year=current_year,
            is_active=True
        ).values_list('course_section_id', flat=True).distinct()
        all_my_sections = CourseSection.objects.filter(id__in=my_sec_ids).select_related('grade_level').order_by('grade_level__order', 'name')
    else:
        all_my_sections = CourseSection.objects.filter(
            academic_year=current_year
        ).select_related('grade_level').order_by('grade_level__order', 'name')

    # Asignaciones del docente en este curso específico
    if user.is_teacher and hasattr(user, 'teacher_profile'):
        my_assignments = TeachingAssignment.objects.filter(
            teacher=user.teacher_profile,
            course_section=section,
            is_active=True
        ).select_related('subject')
        assigned_subject_ids = list(my_assignments.values_list('subject_id', flat=True))
    else:
        my_assignments = TeachingAssignment.objects.filter(
            course_section=section,
            is_active=True
        ).select_related('subject', 'teacher__user')
        assigned_subject_ids = list(my_assignments.values_list('subject_id', flat=True))

    # Asignaturas en el curso
    subjects_in_course = Subject.objects.filter(
        id__in=assigned_subject_ids
    ).prefetch_related('norms') if assigned_subject_ids else Subject.objects.filter(
        curriculum_grades__grade_level=section.grade_level
    ).prefetch_related('norms')

    principales = [s for s in subjects_in_course if s.category == Subject.Category.PRINCIPAL]
    humanisticas = [s for s in subjects_in_course if s.category == Subject.Category.HUMANISTICA]
    arte_deporte = [s for s in subjects_in_course if s.category == Subject.Category.ARTE_DEPORTE]

    # Periodos del año lectivo
    periods = AcademicPeriod.objects.filter(academic_year=current_year).order_by('number') if current_year else []
    period_id = request.GET.get('period_id')
    if period_id:
        selected_period = AcademicPeriod.objects.filter(id=period_id).first() or active_period
    else:
        selected_period = active_period or (periods.first() if periods.exists() else None)

    # Asignatura seleccionada para la planilla de notas
    subject_id = request.GET.get('subject_id')
    if subject_id:
        selected_subject = subjects_in_course.filter(id=subject_id).first() or subjects_in_course.first()
    else:
        selected_subject = subjects_in_course.first()

    # 1. CÁLCULO DE LA PLANILLA DE NOTAS (Matriz de Calificaciones integrada)
    matrix_rows = []
    criteria = []
    kpis = {}
    is_editable = False

    if selected_subject and selected_period:
        from apps.grades.services import get_or_create_default_criteria, calculate_period_final_grade
        from apps.grades.models import GradeRecord
        from decimal import Decimal, ROUND_HALF_UP

        is_editable = selected_period.is_editable
        if user.is_teacher and hasattr(user, 'teacher_profile'):
            has_assignment = TeachingAssignment.objects.filter(
                teacher=user.teacher_profile,
                course_section=section,
                subject=selected_subject,
                academic_year=current_year,
                is_active=True
            ).exists()
            if not has_assignment and not (user.is_admin_role or user.is_rector):
                is_editable = False

        criteria = get_or_create_default_criteria(section, selected_subject, selected_period)
        enrollments = section.enrollments.filter(
            status='ACTIVE'
        ).select_related('student__user').order_by('student__user__last_name', 'student__user__first_name')

        for enr in enrollments:
            student = enr.student
            scores_by_criterion = []
            for crit in criteria:
                rec = GradeRecord.objects.filter(
                    student=student,
                    course_section=section,
                    subject=selected_subject,
                    academic_period=selected_period,
                    criterion=crit
                ).first()
                scores_by_criterion.append({
                    'criterion': crit,
                    'record': rec,
                    'score': rec.score if rec else None
                })

            final_grade = calculate_period_final_grade(student, section, selected_subject, selected_period)
            matrix_rows.append({
                'student': student,
                'scores': scores_by_criterion,
                'final_grade': final_grade,
            })

        total_students = len(matrix_rows)
        final_grades_list = [r['final_grade'].final_score for r in matrix_rows if r.get('final_grade') and r['final_grade'].final_score > Decimal('0.00')]
        if final_grades_list and len(final_grades_list) > 0:
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

    # ¿Es el docente director de grupo de este curso? Solo director de grupo ve toda la malla y boletines/sábana.
    is_group_director = False
    if user.is_teacher and hasattr(user, 'teacher_profile'):
        is_group_director = (
            section.homeroom_teacher == user or
            TeachingAssignment.objects.filter(
                teacher=user.teacher_profile,
                course_section=section,
                is_group_director=True,
                is_active=True
            ).exists()
        )
    elif user.is_admin_role or user.is_rector or user.is_secretary or getattr(user, 'is_coordinator', False):
        is_group_director = True

    # 2. Malla Curricular del Grado y Control de Acceso:
    # - El Director de Grupo o Directivo puede ver toda la malla del grado.
    # - Los demás docentes solo pueden ver su área asignada, sus asignaturas, las horas que les tocan y el contenido.
    if is_group_director:
        curriculum_qs = GradeSubject.objects.filter(
            grade_level=section.grade_level
        ).select_related('subject__area').prefetch_related(
            'subject__norms',
            'subject__curriculum_grades__grade_level'
        ).order_by('subject__area__order', 'subject__category', 'subject__name')
    else:
        curriculum_qs = GradeSubject.objects.filter(
            grade_level=section.grade_level,
            subject_id__in=assigned_subject_ids
        ).select_related('subject__area').prefetch_related(
            'subject__norms',
            'subject__curriculum_grades__grade_level'
        ).order_by('subject__area__order', 'subject__category', 'subject__name')

    curriculum_data = []
    for gs in curriculum_qs:
        s = gs.subject
        # Intensidades de esta materia en todos los grados escolares
        intensities = []
        for cg in s.curriculum_grades.all().select_related('grade_level').order_by('grade_level__order'):
            intensities.append({
                'grade_name': cg.grade_level.name,
                'grade_code': cg.grade_level.code,
                'weekly_hours': cg.weekly_hours,
                'weight_percentage': cg.weight_percentage,
                'is_current': cg.grade_level_id == section.grade_level_id,
            })

        curriculum_data.append({
            'grade_subject': gs,
            'subject': s,
            'weekly_hours': gs.weekly_hours,
            'weight_percentage': gs.weight_percentage,
            'description': s.description or 'Contenido curricular conforme a los lineamientos del MEN.',
            'norms': s.norms.all().order_by('order', 'code'),
            'intensities': intensities,
            'is_assigned_to_me': s.id in assigned_subject_ids,
        })

    # Asignaturas para las tarjetas superiores de categorías en la pestaña Malla
    malla_subjects = [item['subject'] for item in curriculum_data]
    principales = [s for s in malla_subjects if s.category == Subject.Category.PRINCIPAL]
    humanisticas = [s for s in malla_subjects if s.category == Subject.Category.HUMANISTICA]
    arte_deporte = [s for s in malla_subjects if s.category == Subject.Category.ARTE_DEPORTE]

    # 3. Control de Asistencia del Curso - Llamado de Lista Completo e Interactivo
    from apps.attendance.services import get_or_create_attendance_session, calculate_student_absence_stats
    active_enrollments = section.enrollments.filter(status='ACTIVE').select_related('student__user').order_by('student__user__last_name')
    date_str = request.GET.get('date', datetime.date.today().isoformat())
    try:
        current_date = datetime.date.fromisoformat(date_str)
    except ValueError:
        current_date = datetime.date.today()

    # Asignatura seleccionada para el llamado (puede ser distinta a la de notas)
    att_subject_id = request.GET.get('att_subject_id')
    if att_subject_id:
        att_subject = subjects_in_course.filter(id=att_subject_id).first() or subjects_in_course.first()
    else:
        att_subject = selected_subject or subjects_in_course.first()

    # Crear o recuperar la sesión de asistencia del día
    attendance_session = None
    enriched_records = []
    is_att_editable = False

    if att_subject and active_period:
        try:
            attendance_session = get_or_create_attendance_session(
                course_section=section,
                subject=att_subject,
                session_date=current_date,
                recorded_by=user
            )
            is_att_editable = attendance_session.academic_period.is_editable
            if user.is_secretary:
                is_att_editable = False
            elif user.is_teacher and hasattr(user, 'teacher_profile'):
                has_att_assignment = TeachingAssignment.objects.filter(
                    teacher=user.teacher_profile,
                    course_section=section,
                    subject=att_subject,
                    academic_year=current_year,
                    is_active=True
                ).exists()
                if not has_att_assignment and not (user.is_admin_role or user.is_rector):
                    is_att_editable = False

            # Enriquecer registros con estadísticas de ausentismo
            for rec in attendance_session.records.select_related('student__user').all():
                stats = calculate_student_absence_stats(rec.student, att_subject, attendance_session.academic_period)
                enriched_records.append({
                    'record': rec,
                    'student': rec.student,
                    'stats': stats,
                })
        except Exception:
            attendance_session = None
            enriched_records = []

    # Pestaña activa: por defecto 'planilla' (Planilla de Notas al entrar)
    active_tab = request.GET.get('tab', 'planilla')

    # Sábana de notas del curso (consolidado) - Solo accesible para el Director de Grupo de este salón o Directivos/Secretaría
    sabana_period = None
    sabana_data = None
    if is_group_director:
        from apps.reports.services import build_section_consolidated_data
        sabana_period_id = request.GET.get('sabana_period_id')
        if sabana_period_id:
            sabana_period = AcademicPeriod.objects.filter(id=sabana_period_id).first()
        if not sabana_period:
            sabana_period = selected_period
        if sabana_period:
            try:
                sabana_data = build_section_consolidated_data(section, sabana_period)
            except Exception:
                sabana_data = None
    else:
        if active_tab in ['sabana', 'boletines']:
            active_tab = 'planilla'

    context = {
        'section': section,
        'current_year': current_year,
        'active_period': active_period,
        'selected_period': selected_period,
        'periods': periods,
        'all_my_sections': all_my_sections,
        'my_assignments': my_assignments,
        'subjects_in_course': subjects_in_course,
        'selected_subject': selected_subject,
        'principales': principales,
        'humanisticas': humanisticas,
        'arte_deporte': arte_deporte,
        'curriculum': curriculum_data,
        'curriculum_data': curriculum_data,
        'active_enrollments': active_enrollments,
        'current_date': current_date,
        # Llamado de lista completo
        'attendance_session': attendance_session,
        'session': attendance_session,
        'enriched_records': enriched_records,
        'is_att_editable': is_att_editable,
        'att_subject': att_subject,
        'active_tab': active_tab,
        'matrix_rows': matrix_rows,
        'criteria': criteria,
        'kpis': kpis,
        'is_editable': is_editable,
        'is_group_director': is_group_director,
        'sabana_data': sabana_data,
        'sabana_period': sabana_period,
    }
    return render(request, 'teachers/course_workspace.html', context)


@login_required
def add_subject_norm_view(request, subject_id):
    """
    Permite asociar una Norma, Estándar MEN o Competencia a una Asignatura / Módulo.
    """
    from apps.subjects.models import Subject, SubjectNorm

    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        order = request.POST.get('order', 1)

        if code and title and description:
            try:
                order_val = int(order)
            except ValueError:
                order_val = 1

            SubjectNorm.objects.create(
                subject=subject,
                code=code,
                title=title,
                description=description,
                order=order_val
            )
            messages.success(request, f'Norma/Competencia "{code}" asociada correctamente a {subject.name}.')
        else:
            messages.error(request, 'Todos los campos de la norma son obligatorios.')

    return redirect(request.META.get('HTTP_REFERER', 'teachers:my_courses'))


@login_required
def api_subjects_for_section(request, section_id):
    """
    API JSON: Retorna las asignaturas disponibles para la sección (según la malla curricular
    del grado) agrupadas por categoría. Usado en el modal de asignación para filtrado dinámico.
    """
    # Si la sesión expiró durante la petición AJAX, retornar 401 en lugar de redirigir
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'No autenticado'}, status=401)

    from apps.subjects.models import Subject, GradeSubject
    from apps.courses.models import InstitutionSetting

    section = get_object_or_404(CourseSection, id=section_id)
    inst_type = InstitutionSetting.get_settings().institution_type

    # Asignaturas del plan de estudios del grado de la sección
    # Se busca primero con filtro institution_type, luego sin él como fallback
    curriculum_qs = GradeSubject.objects.filter(
        grade_level=section.grade_level,
        subject__institution_type=inst_type
    ).select_related('subject__area').order_by(
        'subject__category', 'subject__area__order', 'subject__name'
    )

    # Fallback: si no hay malla con inst_type, buscar sin ese filtro
    if not curriculum_qs.exists():
        curriculum_qs = GradeSubject.objects.filter(
            grade_level=section.grade_level
        ).select_related('subject__area').order_by(
            'subject__category', 'subject__area__order', 'subject__name'
        )

    subjects_data = []
    for gs in curriculum_qs:
        s = gs.subject
        subjects_data.append({
            'id': s.id,
            'name': s.name,
            'code': s.code,
            'area': s.area.name,
            'category': s.get_category_display(),
            'weekly_hours': gs.weekly_hours,
        })

    # Último fallback: si tampoco hay malla, devuelve TODAS las asignaturas de la institución
    if not subjects_data:
        for s in Subject.objects.filter(
            institution_type=inst_type
        ).select_related('area').order_by('category', 'area__order', 'name'):
            subjects_data.append({
                'id': s.id,
                'name': s.name,
                'code': s.code,
                'area': s.area.name,
                'category': s.get_category_display(),
                'weekly_hours': None,
            })
        # Si aun así no hay nada, retorna todas sin filtro de institution_type
        if not subjects_data:
            for s in Subject.objects.all().select_related('area').order_by('name'):
                subjects_data.append({
                    'id': s.id,
                    'name': s.name,
                    'code': s.code,
                    'area': s.area.name,
                    'category': s.get_category_display(),
                    'weekly_hours': None,
                })

    return JsonResponse({
        'section_id': section_id,
        'section_name': section.name,
        'grade_name': section.grade_level.name,
        'subjects': subjects_data,
    })
