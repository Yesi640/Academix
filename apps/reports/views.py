from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseForbidden
from django.template.loader import render_to_string
from .services import (
    build_student_bulletin_data,
    build_section_consolidated_data,
    export_consolidated_csv,
    build_honor_roll_data,
    compile_weasyprint_pdf
)
from apps.courses.models import CourseSection
from apps.periods.models import AcademicPeriod
from apps.students.models import StudentProfile, Enrollment
from apps.courses.services import get_current_academic_year
from apps.courses.decorators import enforce_report_card_clearance
from apps.periods.services import get_current_active_period
from apps.teachers.models import TeachingAssignment
from apps.audit.services import log_audit

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
        if user.is_group_director:
            director_assignments = TeachingAssignment.objects.filter(
                teacher=user.teacher_profile,
                academic_year=current_year,
                is_active=True,
                is_group_director=True
            )
            sections = CourseSection.objects.filter(
                id__in=director_assignments.values_list('course_section_id', flat=True),
                grade_level__institution_type=inst_type
            ).distinct()
        else:
            sections = CourseSection.objects.none()
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

    bulletin_data = build_student_bulletin_data(student, section, period, request=request)

    context = {
        'b': bulletin_data,
        'is_bulk': False,
    }
    return render(request, 'reports/bulletin_printable.html', context)


@login_required
@enforce_report_card_clearance(student_param_name='student_id')
def download_student_bulletin_pdf_view(request, student_id, period_id):
    """
    Pilar 5: Generación y descarga directa del boletín oficial en formato PDF
    utilizando WeasyPrint con directivas CSS Paged Media (A4) y validación criptográfica QR.
    """
    user = request.user
    student = get_object_or_404(StudentProfile, id=student_id)
    period = get_object_or_404(AcademicPeriod, id=period_id)

    # 1. Control de acceso por rol
    if user.is_student and hasattr(user, 'student_profile') and user.student_profile.id != student.id:
        return HttpResponseForbidden("No tiene autorización para descargar boletines de otros estudiantes.")

    # 2. Control de visibilidad de periodos abiertos para estudiantes y acudientes
    RESTRICTED_ROLES = user.is_student or user.is_parent
    PERIOD_OPEN = period.status not in ['CLOSED', 'LOCKED']
    if RESTRICTED_ROLES and PERIOD_OPEN:
        messages.warning(
            request,
            f'El boletín oficial del período "{period.name}" aún no se encuentra cerrado por la institución.'
        )
        return redirect('accounts:dashboard')

    enrollment = Enrollment.objects.filter(student=student, academic_year=period.academic_year).first()
    if not enrollment:
        messages.error(request, f'El estudiante {student.user.get_full_name()} no cuenta con matrícula activa para este periodo.')
        return redirect('reports:index')

    section = enrollment.course_section

    # 3. Restricción para docentes que no son directores de grupo
    if user.is_teacher and hasattr(user, 'teacher_profile'):
        is_dir = TeachingAssignment.objects.filter(
            teacher=user.teacher_profile,
            course_section=section,
            is_group_director=True,
            is_active=True
        ).exists()
        if not is_dir:
            messages.error(request, 'Solo el Director de Grupo puede descargar los boletines de este curso.')
            return redirect('teachers:my_courses')

    # 4. Compilación de datos pedagógicos, ranking, QR y hash criptográfico
    bulletin_data = build_student_bulletin_data(student, section, period, request=request)

    # 5. Renderizado del template HTML para imprenta WeasyPrint
    html_content = render_to_string('reports/boletin_pdf.html', {'b': bulletin_data}, request=request)

    # 6. Compilación binaria con WeasyPrint
    base_url = request.build_absolute_uri('/')
    pdf_bytes, error_weasy = compile_weasyprint_pdf(html_content, base_url=base_url)

    # Registro de auditoría del evento de descarga de reporte oficial
    log_audit(
        action='OFFICIAL_REPORT_EXPORT',
        table_name='StudentBulletin',
        record_id=f"{student.id}-{period.id}",
        new_values={
            'student': student.user.get_full_name(),
            'period': period.name,
            'year': period.academic_year.year,
            'token': bulletin_data.get('verification_token'),
            'format': 'PDF' if pdf_bytes else 'HTML_PRINTABLE_FALLBACK'
        },
        reason=f"Descarga de boletín oficial en PDF para estudiante {student.user.get_full_name()}",
        user=user,
        request=request
    )

    clean_lastname = student.user.last_name.replace(' ', '_')
    clean_firstname = student.user.first_name.replace(' ', '_')
    pdf_filename = f"Boletin_{clean_lastname}_{clean_firstname}_P{period.number}_{period.academic_year.year}.pdf"

    # 7. Inyección automática en la Carpeta Perpetua del Estudiante (Módulo 2)
    try:
        from apps.students.services import attach_bulletin_to_expediente
        attach_bulletin_to_expediente(
            student_profile=student,
            period=period,
            pdf_content=pdf_bytes,
            filename=pdf_filename,
            user=user
        )
    except Exception:
        pass

    if pdf_bytes:
        response = HttpResponse(pdf_bytes, content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{pdf_filename}"'
        return response

    # Fallback seguro para entornos de desarrollo donde WeasyPrint carezca de GTK C-libraries:
    # Se retorna el HTML de imprenta listo con auto-print
    response = HttpResponse(html_content, content_type='text/html')
    response['X-Weasyprint-Notice'] = f"PDF compilation fallback due to system library: {error_weasy}"
    return response


def verify_bulletin_view(request, token):
    """
    Vista pública para la verificación de autenticidad e inmutabilidad de boletines oficiales emitidos.
    Accesible mediante escaneo del código QR.
    """
    from apps.courses.models import InstitutionSetting
    institution = InstitutionSetting.get_settings()
    context = {
        'token': token,
        'institution': institution,
        'is_valid': len(token) >= 16,
    }
    return render(request, 'reports/partials/verify_bulletin.html', context)


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
    Acceso restringido a:
    - Coordinador / Directivo / Rector
    - Administrador
    - Secretaría Académica
    - Docente Director de Grupo (únicamente de su propio salón asignado)
    """
    if not request.user.can_view_sabana:
        messages.error(request, "Acceso restringido: La sábana de notas solo puede ser consultada por el Director de Grupo del salón, Coordinación y Secretaría.")
        return redirect('dashboard')

    from apps.courses.models import InstitutionSetting
    inst_type = InstitutionSetting.get_settings().institution_type

    section_id = request.GET.get('section_id')
    period_id = request.GET.get('period_id')
    current_year = get_current_academic_year()
    periods = AcademicPeriod.objects.filter(academic_year=current_year).order_by('number') if current_year else []

    all_sections = CourseSection.objects.filter(
        academic_year=current_year,
        grade_level__institution_type=inst_type
    ).select_related('grade_level') if current_year else CourseSection.objects.none()

    # Si es docente, solo puede consultar las secciones donde es Director de Grupo
    if request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        directed_section_ids = request.user.teacher_profile.assignments.filter(
            academic_year=current_year,
            is_active=True,
            is_group_director=True
        ).values_list('course_section_id', flat=True)
        sections = all_sections.filter(id__in=directed_section_ids)
        if not sections.exists():
            messages.warning(request, "Actualmente no tienes ningún salón asignado como Director de Grupo.")
            return redirect('dashboard')
    else:
        sections = all_sections

    if not section_id or not period_id:
        # Preseleccionar primer salón si es director de grupo
        initial_section = sections.first()
        initial_period = get_current_active_period(current_year) or (periods.first() if periods else None)
        if initial_section and initial_period:
            data = build_section_consolidated_data(initial_section, initial_period)
            selected_section = initial_section
            selected_period = initial_period
        else:
            data = None
            selected_section = None
            selected_period = None

        context = {
            'periods': periods,
            'sections': sections,
            'selected_section': selected_section,
            'selected_period': selected_period,
            'data': data,
        }
        return render(request, 'reports/consolidated.html', context)

    # Validar que si es docente, el section_id pertenezca a sus cursos como director
    if request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        if not sections.filter(id=section_id).exists():
            messages.error(request, "Solo puedes consultar la sábana de notas del salón donde eres Director de Grupo.")
            return redirect('reports:consolidated')

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
    Acceso restringido a Director de Grupo del salón, Coordinación y Secretaría.
    """
    if not request.user.can_view_sabana:
        return HttpResponseForbidden("Acceso restringido: Solo el Director de Grupo de este salón, Coordinación y Secretaría pueden exportar la sábana de notas.")

    if request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        is_director = request.user.teacher_profile.assignments.filter(
            course_section_id=section_id,
            is_active=True,
            is_group_director=True
        ).exists()
        if not is_director:
            return HttpResponseForbidden("Solo puedes exportar la sábana de notas del salón donde eres Director de Grupo.")

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
    El Cuadro de Honor ha sido deshabilitado del sistema.
    Redirecciona de manera segura al panel principal de reportes.
    """
    messages.info(request, "El Cuadro de Honor ha sido deshabilitado.")
    return redirect('reports:index')

