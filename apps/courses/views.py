from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import AcademicYear, GradeLevel, CourseSection, InstitutionSetting
from .services import get_current_academic_year, create_course_section
from apps.accounts.models import CustomUser

@login_required
def academic_structure_view(request):
    """
    Vista principal de la estructura académica institucional.
    Muestra años lectivos, grados escolares y cursos/grupos activos de la institución actual.
    Soporta filtrado por enfoque de colegio (Primaria, Secundaria o Completo).
    """
    inst_settings = InstitutionSetting.get_settings()
    inst_type = inst_settings.institution_type

    # Sincronizar catálogo de grados si es colegio y aún no existen
    if inst_type == InstitutionSetting.InstitutionType.COLEGIO:
        from .services import ensure_standard_colegio_grades
        if not GradeLevel.objects.filter(institution_type=inst_type).exists():
            ensure_standard_colegio_grades(inst_settings.school_scope)

    current_year = get_current_academic_year()
    years = AcademicYear.objects.all().order_by('-year')
    grades_qs = GradeLevel.objects.filter(institution_type=inst_type).order_by('order')

    if inst_type == InstitutionSetting.InstitutionType.COLEGIO:
        if inst_settings.school_scope == InstitutionSetting.SchoolLevelScope.PRIMARIA:
            grades = grades_qs.filter(level_stage__in=[GradeLevel.LevelStage.PREESCOLAR, GradeLevel.LevelStage.PRIMARIA])
        elif inst_settings.school_scope == InstitutionSetting.SchoolLevelScope.SECUNDARIA:
            grades = grades_qs.filter(level_stage__in=[GradeLevel.LevelStage.SECUNDARIA, GradeLevel.LevelStage.MEDIA])
        else:
            grades = grades_qs
    else:
        grades = grades_qs

    teachers = CustomUser.objects.filter(role=CustomUser.Role.TEACHER, is_active=True)

    selected_year_id = request.GET.get('year')
    if selected_year_id:
        active_year = AcademicYear.objects.filter(id=selected_year_id).first() or current_year or years.first()
    else:
        active_year = current_year or years.first()

    sections = CourseSection.objects.filter(
        academic_year=active_year,
        grade_level__in=grades
    ).select_related('grade_level', 'homeroom_teacher') if active_year else []

    # Lista sugerida de años lectivos desde 2026 en adelante
    registered_years = list(years.values_list('year', flat=True))
    suggested_years = [y for y in range(2026, 2035) if y not in registered_years]

    context = {
        'current_year': current_year,
        'active_year': active_year,
        'years': years,
        'grades': grades,
        'teachers': teachers,
        'sections': sections,
        'inst_settings': inst_settings,
        'suggested_years': suggested_years,
        'school_scopes': InstitutionSetting.SchoolLevelScope.choices,
    }
    return render(request, 'courses/academic_structure.html', context)

@login_required
def create_academic_year_view(request):
    """
    Crea un nuevo año lectivo desde 2026 en adelante.
    Permite configurar automáticamente los periodos estándar y los cursos normales de colegio.
    """
    if not (request.user.is_admin_role or request.user.is_rector or request.user.is_secretary):
        messages.error(request, 'No tiene permisos para crear años escolares.')
        return redirect('courses:academic_structure')

    if request.method == 'POST':
        from .services import create_academic_year
        year = request.POST.get('year')
        name = request.POST.get('name', '').strip()
        start_date = request.POST.get('start_date') or None
        end_date = request.POST.get('end_date') or None
        is_current = request.POST.get('is_current') in ['on', 'true', '1', True]
        auto_create_periods = request.POST.get('auto_create_periods') in ['on', 'true', '1', True]
        auto_generate_sections = request.POST.get('auto_generate_sections') in ['on', 'true', '1', True]

        try:
            new_year = create_academic_year(
                year=year,
                name=name,
                start_date=start_date,
                end_date=end_date,
                is_current=is_current,
                auto_create_periods=auto_create_periods,
                auto_generate_sections=auto_generate_sections,
                user=request.user
            )
            messages.success(request, f'¡Año lectivo {new_year.name} configurado exitosamente!')
            return redirect(f"/courses/academic-structure/?year={new_year.id}")
        except Exception as e:
            messages.error(request, f'Error al registrar año lectivo: {str(e)}')

    return redirect('courses:academic_structure')

@login_required
def set_active_year_view(request, year_id):
    """
    Establece el año escolar seleccionado como el año vigente en todo el sistema.
    """
    if not (request.user.is_admin_role or request.user.is_rector or request.user.is_secretary):
        messages.error(request, 'No tiene permisos para modificar el año lectivo vigente.')
        return redirect('courses:academic_structure')

    from .services import set_current_academic_year
    try:
        yr = set_current_academic_year(year_id, user=request.user)
        messages.success(request, f'El {yr.name} es ahora el año lectivo vigente en toda la plataforma.')
    except Exception as e:
        messages.error(request, f'Error al activar año lectivo: {str(e)}')

    return redirect(f"/courses/academic-structure/?year={year_id}")

@login_required
def generate_default_sections_view(request, year_id):
    """
    Genera automáticamente los cursos normales de un colegio para el año lectivo indicado.
    """
    if not (request.user.is_admin_role or request.user.is_rector):
        messages.error(request, 'No tiene permisos para generar cursos automáticamente.')
        return redirect('courses:academic_structure')

    from .services import generate_default_sections_for_year
    academic_year = get_object_or_404(AcademicYear, id=year_id)
    try:
        created_sections = generate_default_sections_for_year(academic_year, user=request.user)
        if created_sections:
            messages.success(request, f'Se generaron {len(created_sections)} cursos estándar para {academic_year.name}.')
        else:
            messages.info(request, f'Los cursos estándar para {academic_year.name} ya se encontraban creados.')
    except Exception as e:
        messages.error(request, f'Error al generar cursos: {str(e)}')

    return redirect(f"/courses/academic-structure/?year={year_id}")

@login_required
def sections_partial(request):
    """
    Endpoint HTMX para búsqueda y filtrado reactivo de secciones de la institución activa.
    """
    inst_type = InstitutionSetting.get_settings().institution_type

    year_id = request.GET.get('year')
    grade_id = request.GET.get('grade')
    query = request.GET.get('q', '').strip()

    sections = CourseSection.objects.filter(
        grade_level__institution_type=inst_type
    ).select_related('grade_level', 'academic_year', 'homeroom_teacher')

    if year_id:
        sections = sections.filter(academic_year_id=year_id)
    if grade_id:
        sections = sections.filter(grade_level_id=grade_id)
    if query:
        sections = sections.filter(name__icontains=query)

    return render(request, 'courses/partials/sections_table.html', {'sections': sections})

@login_required
def create_section_view(request):
    """
    Crea una nueva sección escolar mediante HTMX o petición tradicional.
    """
    if request.method == 'POST':
        year_id = request.POST.get('academic_year')
        grade_id = request.POST.get('grade_level')
        name = request.POST.get('name', '').strip()
        classroom = request.POST.get('classroom', '').strip()
        teacher_id = request.POST.get('homeroom_teacher') or None
        capacity = int(request.POST.get('capacity', 35))

        academic_year = get_object_or_404(AcademicYear, id=year_id)
        grade_level = get_object_or_404(GradeLevel, id=grade_id)
        teacher = get_object_or_404(CustomUser, id=teacher_id) if teacher_id else None

        try:
            create_course_section(
                academic_year=academic_year,
                grade_level=grade_level,
                name=name,
                classroom=classroom,
                homeroom_teacher=teacher,
                capacity=capacity,
                user=request.user
            )
            messages.success(request, f'Grupo {name} creado con éxito.')
        except Exception as e:
            messages.error(request, f'Error al crear grupo: {str(e)}')

    return redirect(f"/courses/academic-structure/?year={year_id}" if 'year_id' in locals() else 'courses:academic_structure')

@login_required
def institution_settings_view(request):
    """
    Panel de Personalización de Marca e Identidad Escolar (White-Label).
    Permite al Administrador y Rector cambiar el logotipo de la escuela,
    la paleta de colores de todo el sitio web (primario y secundario) y
    la información oficial del colegio para comercializar a cualquier institución educativa.
    """
    if not (request.user.is_admin_role or request.user.is_rector):
        messages.error(request, 'No tiene permisos para modificar la identidad y parámetros institucionales.')
        return redirect('dashboard')

    settings_obj = InstitutionSetting.get_settings()

    if request.method == 'POST':
        # 1. Manejo del Logo Institucional
        if 'logo' in request.FILES:
            settings_obj.logo = request.FILES['logo']
        elif request.POST.get('remove_logo') == '1':
            if settings_obj.logo:
                settings_obj.logo.delete(save=False)
            settings_obj.logo = None

        # 2. Paleta de Colores de la Escuela
        primary_color = request.POST.get('primary_color', '').strip()
        secondary_color = request.POST.get('secondary_color', '').strip()
        if primary_color:
            settings_obj.primary_color = primary_color
        if secondary_color:
            settings_obj.secondary_color = secondary_color

        # 3. Datos Oficiales de la Escuela
        inst_name = request.POST.get('institution_name', '').strip()
        if inst_name:
            settings_obj.institution_name = inst_name
        settings_obj.slogan = request.POST.get('slogan', settings_obj.slogan).strip()
        settings_obj.dane_code = request.POST.get('dane_code', '').strip()
        settings_obj.consecutive_resolution = request.POST.get('consecutive_resolution', '').strip()
        settings_obj.contact_email = request.POST.get('contact_email', '').strip()
        settings_obj.contact_phone = request.POST.get('contact_phone', '').strip()
        settings_obj.website_url = request.POST.get('website_url', '').strip()

        # Enfoque escolar (Primaria, Secundaria o Completo)
        school_scope = request.POST.get('school_scope')
        if school_scope in dict(InstitutionSetting.SchoolLevelScope.choices):
            settings_obj.school_scope = school_scope
            from .services import ensure_standard_colegio_grades
            ensure_standard_colegio_grades(school_scope)

        # Fijar permanentemente modelo COLEGIO
        settings_obj.institution_type = InstitutionSetting.InstitutionType.COLEGIO
        settings_obj.save()

        # 4. Sincronizar tema global en todo el sistema
        try:
            from apps.accounts.models import SystemThemeSettings
            theme_data = {
                'key': 'custom_school',
                'name': settings_obj.institution_name,
                'primary': settings_obj.primary_color,
                'primaryDark': settings_obj.primary_color,
                'primaryLight': settings_obj.secondary_color,
                'primaryPastel': settings_obj.secondary_color,
                'sidebarGradient': f"linear-gradient(180deg, {settings_obj.primary_color} 0%, #0f172a 100%)",
                'shadow': f"0 10px 25px -5px {settings_obj.primary_color}40",
            }
            SystemThemeSettings.set_global_theme(theme_data, request.user)
        except Exception:
            pass

        # 5. Registrar en Auditoría Inmutable
        from apps.audit.services import log_audit
        from apps.audit.models import AuditLog
        log_audit(
            action=AuditLog.Action.CONFIG_CHANGE,
            table_name='courses_institutionsetting',
            record_id=str(settings_obj.id),
            new_values={
                'institution_name': settings_obj.institution_name,
                'primary_color': settings_obj.primary_color,
                'secondary_color': settings_obj.secondary_color,
                'has_logo': bool(settings_obj.logo),
            },
            reason=f'Personalización de marca e identidad escolar para {settings_obj.institution_name}',
            user=request.user,
            request=request
        )

        messages.success(request, f'¡Identidad visual y datos de "{settings_obj.institution_name}" actualizados con éxito en todo el sistema!')
        return redirect('courses:institution_settings')

    context = {
        'inst_settings': settings_obj,
        'school_scopes': InstitutionSetting.SchoolLevelScope.choices,
    }
    return render(request, 'courses/institution_settings.html', context)


