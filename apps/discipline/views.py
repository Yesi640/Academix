from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib import messages
from apps.students.models import StudentProfile
from apps.courses.models import AcademicYear, CourseSection
from apps.periods.models import AcademicPeriod
from apps.courses.services import get_current_academic_year
from .models import AnotacionDisciplinaria
from .services import (
    create_anotacion,
    add_student_disclaimer,
    sign_parent_anotacion,
    close_anotacion,
    get_student_discipline_summary
)


@login_required
def student_observer_view(request, student_id):
    """
    Vista del Observador del Estudiante con línea de tiempo y formulario de registro.
    """
    user = request.user
    student = get_object_or_404(StudentProfile.objects.select_related('user', 'parent'), id=student_id)
    current_year = get_current_academic_year()

    # Validar permisos de acceso
    is_staff = user.is_superuser or user.is_admin_role or user.is_rector or user.is_secretary
    is_teacher = user.is_teacher
    is_parent = (user.is_parent and student.parent == user)
    is_student_self = (user.is_student and student.user == user)

    if not (is_staff or is_teacher or is_parent or is_student_self):
        raise PermissionDenied("No tienes autorización para consultar este Observador Escolar.")

    periods = AcademicPeriod.objects.filter(academic_year=current_year).order_by('number') if current_year else []
    summary = get_student_discipline_summary(student, current_year)

    can_create = is_staff or is_teacher
    can_sign = is_parent or is_staff

    context = {
        'student': student,
        'current_year': current_year,
        'periods': periods,
        'summary': summary,
        'can_create': can_create,
        'can_sign': can_sign,
        'fault_types': AnotacionDisciplinaria.FaultType.choices,
    }
    return render(request, 'discipline/observer.html', context)


@login_required
def create_anotacion_view(request, student_id):
    """
    Registra una nueva anotación disciplinaria en el observador del alumno.
    """
    user = request.user
    is_staff = user.is_superuser or user.is_admin_role or user.is_rector or user.is_secretary
    if not (is_staff or user.is_teacher):
        raise PermissionDenied("Solo docentes y directivos pueden registrar situaciones en el observador.")

    student = get_object_or_404(StudentProfile, id=student_id)
    current_year = get_current_academic_year()

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        fault_type = request.POST.get('fault_type', AnotacionDisciplinaria.FaultType.TIPO_I)
        location = request.POST.get('location', 'Aula de Clase').strip()
        student_disclaimer = request.POST.get('student_disclaimer', '').strip()
        pedagogical_commitment = request.POST.get('pedagogical_commitment', '').strip()
        period_id = request.POST.get('period_id')
        parent_notified = request.POST.get('parent_notified') in ['on', 'true', '1', True]

        period = AcademicPeriod.objects.filter(id=period_id).first() if period_id else None

        try:
            record = create_anotacion(
                student_profile=student,
                author_user=user,
                academic_year=current_year,
                title=title,
                description=description,
                fault_type=fault_type,
                period=period,
                location=location,
                student_disclaimer=student_disclaimer,
                pedagogical_commitment=pedagogical_commitment,
                parent_notified=parent_notified
            )
            messages.success(request, f'Anotación "{record.title}" registrada exitosamente en el observador.')
        except Exception as e:
            messages.error(request, f'Error al registrar la anotación: {str(e)}')

    return redirect('discipline:observer', student_id=student.id)


@login_required
def sign_anotacion_view(request, record_id):
    """
    Firma digital de conformidad y enterado del acudiente.
    """
    record = get_object_or_404(AnotacionDisciplinaria.objects.select_related('student'), id=record_id)
    if request.method == 'POST':
        comments = request.POST.get('parent_comments', '').strip()
        try:
            sign_parent_anotacion(record_id=record.id, parent_user=request.user, comments=comments)
            messages.success(request, 'Firma y enterado del acudiente registrado con éxito.')
        except Exception as e:
            messages.error(request, f'No se pudo firmar la anotación: {str(e)}')

    return redirect('discipline:observer', student_id=record.student.id)


@login_required
def close_anotacion_view(request, record_id):
    """
    Cierre formal de la anotación por parte de directiva o docente.
    """
    record = get_object_or_404(AnotacionDisciplinaria.objects.select_related('student'), id=record_id)
    if request.method == 'POST':
        closing_notes = request.POST.get('closing_notes', '').strip()
        try:
            close_anotacion(record_id=record.id, directivo_user=request.user, closing_notes=closing_notes)
            messages.success(request, 'Situación convivencial cerrada exitosamente.')
        except Exception as e:
            messages.error(request, f'Error al cerrar la anotación: {str(e)}')

    return redirect('discipline:observer', student_id=record.student.id)
