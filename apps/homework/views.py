from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from .models import Homework, HomeworkSubmission
from .services import create_homework, submit_homework, grade_submission, grade_or_create_submission
from apps.courses.models import CourseSection
from apps.subjects.models import Subject
from apps.periods.models import AcademicPeriod
from apps.courses.services import get_current_academic_year
from apps.periods.services import get_current_active_period
from apps.teachers.models import TeachingAssignment
from apps.students.models import Enrollment, StudentProfile

@login_required
def homework_index_view(request):
    """
    Panel inicial de tareas escolares adaptado según el rol:
    - Padre de Familia: Consulta exclusiva y segura de las tareas de su acudido (Solo lectura).
    - Estudiante: Consulta y envío de sus propias tareas escolares.
    - Docente / Directivo / Secretaría: Catálogo de Cursos para ingresar a calificar por curso.
    """
    current_year = get_current_academic_year()
    active_period = get_current_active_period(current_year) if current_year else None
    user = request.user

    # 1. Modo Padre de Familia (Solo Lectura Estricto)
    if user.is_parent:
        children = StudentProfile.objects.filter(parent=user).select_related('user')
        selected_student_id = request.GET.get('student_id')
        student = children.filter(id=selected_student_id).first() if selected_student_id else children.first()

        enrollment = None
        homeworks = []
        student_submissions = {}

        if student and current_year:
            enrollment = Enrollment.objects.filter(
                student=student,
                academic_year=current_year,
                status=Enrollment.Status.ACTIVE
            ).select_related('course_section__grade_level').first()

            if enrollment and active_period:
                homeworks = Homework.objects.filter(
                    course_section=enrollment.course_section,
                    academic_period=active_period,
                    is_active=True
                ).select_related('subject', 'teacher__user').order_by('due_date')

                subs = HomeworkSubmission.objects.filter(student=student)
                for s in subs:
                    student_submissions[s.homework_id] = s

                for hw in homeworks:
                    hw.child_submission = student_submissions.get(hw.id)

        context = {
            'is_parent': True,
            'children': children,
            'student': student,
            'enrollment': enrollment,
            'current_year': current_year,
            'active_period': active_period,
            'homeworks': homeworks,
        }
        return render(request, 'homework/parent_homework.html', context)

    # 2. Modo Estudiante: Consulta y entrega de actividades
    if user.is_student and hasattr(user, 'student_profile'):
        enrollment = Enrollment.objects.filter(
            student=user.student_profile,
            academic_year=current_year,
            status=Enrollment.Status.ACTIVE
        ).select_related('course_section__grade_level').first()

        if enrollment and active_period:
            homeworks = Homework.objects.filter(
                course_section=enrollment.course_section,
                academic_period=active_period,
                is_active=True
            ).select_related('subject', 'teacher__user').order_by('due_date')
        else:
            homeworks = Homework.objects.none()

        student_submissions = {}
        subs = HomeworkSubmission.objects.filter(student=user.student_profile)
        for s in subs:
            student_submissions[s.homework_id] = s
        for hw in homeworks:
            hw.my_submission = student_submissions.get(hw.id)

        context = {
            'is_student': True,
            'current_year': current_year,
            'active_period': active_period,
            'enrollment': enrollment,
            'homeworks': homeworks,
        }
        return render(request, 'homework/student_homework.html', context)

    from apps.courses.models import InstitutionSetting
    inst_type = InstitutionSetting.get_settings().institution_type

    # 3. Modo Docente / Directivo / Secretaría: Catálogo de Cursos de la institución activa
    if user.is_teacher and hasattr(user, 'teacher_profile'):
        assignments = TeachingAssignment.objects.filter(
            teacher=user.teacher_profile,
            academic_year=current_year,
            course_section__grade_level__institution_type=inst_type,
            is_active=True
        ).select_related('course_section', 'subject')
        assigned_section_ids = assignments.values_list('course_section_id', flat=True)
        sections = CourseSection.objects.filter(
            id__in=assigned_section_ids,
            grade_level__institution_type=inst_type
        ).select_related('grade_level', 'homeroom_teacher')
    else:
        sections = CourseSection.objects.filter(
            academic_year=current_year,
            grade_level__institution_type=inst_type
        ).select_related('grade_level', 'homeroom_teacher') if current_year else []

    # Calcular estadísticas de tareas por curso para el periodo activo
    course_cards = []
    for sec in sections:
        hw_qs = Homework.objects.filter(course_section=sec, academic_period=active_period)
        enrolled_count = sec.enrollments.filter(status=Enrollment.Status.ACTIVE).count()
        hw_count = hw_qs.count()

        course_cards.append({
            'section': sec,
            'enrolled_count': enrolled_count,
            'hw_count': hw_count,
        })

    # Asignaturas filtradas: docente solo ve las suyas; admin/rector ve todas las del tipo institucional
    if request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        teacher_subject_ids = TeachingAssignment.objects.filter(
            teacher=request.user.teacher_profile,
            academic_year=current_year,
            is_active=True
        ).values_list('subject_id', flat=True)
        subjects = Subject.objects.filter(id__in=teacher_subject_ids, institution_type=inst_type).order_by('name')
    else:
        subjects = Subject.objects.filter(institution_type=inst_type).order_by('name')

    context = {
        'current_year': current_year,
        'active_period': active_period,
        'course_cards': course_cards,
        'sections': sections,
        'subjects': subjects,
    }
    return render(request, 'homework/index.html', context)


@login_required
def homework_course_matrix_view(request, section_id):
    """
    Matriz de Calificación de Tareas del Curso:
    - Profesor: Acceso exclusivo a su curso asignado (no puede ver cursos ajenos).
    - Los alumnos en FILAS.
    - Los trabajos/tareas al LADO (en columnas adyacentes).
    - Lista optimizada para calificación colectiva con botón único al final.
    """
    if request.user.is_parent or request.user.is_student or request.user.is_secretary:
        raise PermissionDenied("Acceso restringido: El módulo de calificación es exclusivo para docentes y directivos.")

    section = get_object_or_404(CourseSection, id=section_id)

    # Restricción: Cada profesor solo puede ver el curso que tiene asignado
    if request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        assigned = TeachingAssignment.objects.filter(
            teacher=request.user.teacher_profile,
            course_section=section,
            is_active=True
        ).exists()
        if not assigned and not (request.user.is_admin_role or request.user.is_rector):
            raise PermissionDenied("Acceso restringido: Solo puede visualizar el curso que tiene asignado.")

    current_year = get_current_academic_year()
    active_period = get_current_active_period(current_year) if current_year else None

    subject_id = request.GET.get('subject_id')

    # Filtrar tareas del curso
    homeworks = Homework.objects.filter(
        course_section=section,
        academic_period=active_period
    ).select_related('subject', 'teacher__user').order_by('due_date')

    if subject_id:
        homeworks = homeworks.filter(subject_id=subject_id)

    # Estudiantes matriculados activos en filas
    enrollments = Enrollment.objects.filter(
        course_section=section,
        academic_year=section.academic_year,
        status=Enrollment.Status.ACTIVE
    ).select_related('student__user').order_by('student__user__last_name', 'student__user__first_name')

    # Reconstruir matriz [Estudiante x Tareas]
    matrix_rows = []
    for enr in enrollments:
        student = enr.student
        items = []
        for hw in homeworks:
            sub = HomeworkSubmission.objects.filter(homework=hw, student=student).first()
            is_locked = bool(sub and sub.is_locked)
            items.append({
                'homework': hw,
                'submission': sub,
                'score': sub.score if sub else None,
                'feedback': sub.teacher_feedback if sub else '',
                'status': sub.status if sub else 'PENDING',
                'is_locked': is_locked,
                'has_attachment': bool(sub and sub.attachment),
                'attachment_url': sub.attachment.url if sub and sub.attachment else None,
                'submission_text': sub.submission_text if sub else None,
            })
        matrix_rows.append({
            'student': student,
            'enrollment': enr,
            'items': items,
        })

    # Filtrar asignaturas según el rol del usuario:
    # - Docente: solo las áreas/asignaturas que tiene asignadas en este curso
    # - Admin / Rector / Directivo: todas las asignaturas con asignación activa en el curso
    if request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        teacher_subject_ids = TeachingAssignment.objects.filter(
            teacher=request.user.teacher_profile,
            course_section=section,
            academic_year=section.academic_year,
            is_active=True
        ).values_list('subject_id', flat=True)
        subjects = Subject.objects.filter(id__in=teacher_subject_ids).order_by('name')
    else:
        # Rector / Admin: mostrar asignaturas con asignación activa en el curso
        all_assigned_ids = TeachingAssignment.objects.filter(
            course_section=section,
            academic_year=section.academic_year,
            is_active=True
        ).values_list('subject_id', flat=True)
        subjects = Subject.objects.filter(id__in=all_assigned_ids).order_by('name')
        if not subjects.exists():
            subjects = Subject.objects.all().order_by('name')

    context = {
        'section': section,
        'current_year': current_year,
        'active_period': active_period,
        'homeworks': homeworks,
        'matrix_rows': matrix_rows,
        'subjects': subjects,
        'selected_subject_id': subject_id or '',
    }
    return render(request, 'homework/course_matrix.html', context)


@login_required
def bulk_grade_course_view(request, section_id):
    """
    Calificación colectiva masiva de alumnos para un curso específico.
    Un único botón al final de la lista procesa y actualiza todas las calificaciones
    bloqueándolas de forma permanente (inmutabilidad estricta).
    """
    if request.user.is_parent or request.user.is_student or request.user.is_secretary:
        raise PermissionDenied("No tiene permisos para calificar tareas.")

    section = get_object_or_404(CourseSection, id=section_id)

    if request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        assigned = TeachingAssignment.objects.filter(
            teacher=request.user.teacher_profile,
            course_section=section,
            is_active=True
        ).exists()
        if not assigned and not (request.user.is_admin_role or request.user.is_rector):
            raise PermissionDenied("No está asignado como docente de este curso.")

    if request.method == 'POST':
        from .services import bulk_grade_homework_list

        grades_data = []
        for key, val in request.POST.items():
            if key.startswith('score_'):
                parts = key.split('_')
                if len(parts) == 3:
                    student_id = parts[1]
                    homework_id = parts[2]
                    feedback = request.POST.get(f"feedback_{student_id}_{homework_id}", "")
                    if val.strip():
                        grades_data.append({
                            'student_id': student_id,
                            'homework_id': homework_id,
                            'score': val.strip(),
                            'feedback': feedback.strip()
                        })

        if grades_data:
            updated_count, skipped_locked = bulk_grade_homework_list(section, grades_data, user=request.user)
            if updated_count > 0:
                messages.success(request, f"¡Actualización completada! Se registraron y bloquearon las notas de {updated_count} entrega(s).")
            if skipped_locked > 0:
                messages.info(request, f"{skipped_locked} calificación(es) ya estaban actualizadas previamente y no pueden ser modificadas.")
        else:
            messages.warning(request, "No se ingresaron calificaciones nuevas para guardar.")

    return redirect('homework:course_matrix', section_id=section.id)


@login_required
def manual_grade_cell_view(request):
    """
    Endpoint para calificar manualmente a un estudiante en una tarea.
    Permite guardado instantáneo desde la matriz mediante formulario o HTMX.
    """
    if request.user.is_parent or request.user.is_student:
        return HttpResponse('<div class="text-danger small">No autorizado.</div>', status=403)

    if request.method == 'POST':
        homework_id = request.POST.get('homework_id')
        student_id = request.POST.get('student_id')
        score = request.POST.get('score')
        feedback = request.POST.get('feedback', '').strip()
        section_id = request.POST.get('section_id')

        try:
            sub = grade_or_create_submission(
                homework_id=homework_id,
                student_id=student_id,
                score=score,
                feedback=feedback,
                user=request.user
            )

            # Si es petición HTMX, retornar el fragmento de la celda actualizada
            if request.headers.get('HX-Request'):
                return render(request, 'homework/partials/grade_cell.html', {
                    'item': {
                        'homework': sub.homework,
                        'submission': sub,
                        'score': sub.score,
                        'feedback': sub.teacher_feedback,
                        'status': sub.status,
                        'is_locked': sub.is_locked,
                        'has_attachment': bool(sub.attachment),
                        'attachment_url': sub.attachment.url if sub.attachment else None,
                        'submission_text': sub.submission_text,
                    },
                    'student': sub.student,
                    'section': sub.homework.course_section,
                    'saved_now': True,
                })

            messages.success(request, f'Calificación guardada para {sub.student.user.get_full_name()}.')
        except Exception as e:
            if request.headers.get('HX-Request'):
                return HttpResponse(f'<div class="text-danger small">{str(e)}</div>', status=400)
            messages.error(request, f'Error al calificar: {str(e)}')

        if section_id:
            return redirect('homework:course_matrix', section_id=section_id)
        return redirect('homework:index')

    return HttpResponse(status=405)


@login_required
def create_homework_view(request):
    """
    Crea una nueva tarea escolar asignada a un grupo.
    """
    if request.method == 'POST' and (request.user.is_teacher or request.user.is_admin_role or request.user.is_rector):
        section_id = request.POST.get('section_id')
        subject_id = request.POST.get('subject_id')
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        due_date_str = request.POST.get('due_date')
        attachment = request.FILES.get('attachment')

        section = get_object_or_404(CourseSection, id=section_id)
        subject = get_object_or_404(Subject, id=subject_id)
        current_year = get_current_academic_year()
        active_period = get_current_active_period(current_year)

        teacher_profile = getattr(request.user, 'teacher_profile', None)
        if not teacher_profile:
            assignment = TeachingAssignment.objects.filter(course_section=section, subject=subject).first()
            teacher_profile = assignment.teacher if assignment else None

        if not teacher_profile:
            # Si es admin o rector, buscar cualquier docente titular o asignar perfil
            from apps.teachers.models import TeacherProfile
            teacher_profile = TeacherProfile.objects.first()

        if not teacher_profile:
            messages.error(request, 'No se pudo identificar el docente asignador para esta tarea.')
            return redirect('homework:index')

        try:
            create_homework(
                teacher=teacher_profile,
                course_section=section,
                subject=subject,
                academic_period=active_period,
                title=title,
                description=description,
                due_date=due_date_str,
                attachment=attachment,
                user=request.user
            )
            messages.success(request, f'Tarea "{title}" publicada con éxito para {section.name}.')
            return redirect('homework:course_matrix', section_id=section.id)
        except Exception as e:
            messages.error(request, f'Error al publicar tarea: {str(e)}')

    return redirect('homework:index')


@login_required
def submit_homework_view(request, homework_id):
    """
    Registra la entrega de la tarea por parte del estudiante.
    Padres tienen prohibido enviar tareas en nombre del alumno.
    """
    if request.user.is_parent:
        raise PermissionDenied("Los padres de familia solo tienen permisos de lectura y no pueden enviar tareas.")

    if request.method == 'POST' and request.user.is_student:
        homework = get_object_or_404(Homework, id=homework_id)
        student_profile = request.user.student_profile
        submission_text = request.POST.get('submission_text', '').strip()
        attachment = request.FILES.get('attachment')

        try:
            submit_homework(
                homework=homework,
                student=student_profile,
                submission_text=submission_text,
                attachment=attachment,
                user=request.user
            )
            messages.success(request, f'¡Tu trabajo para "{homework.title}" fue enviado con éxito!')
        except Exception as e:
            messages.error(request, f'Error al enviar la tarea: {str(e)}')

    return redirect('homework:index')


@login_required
def grade_submission_view(request, submission_id):
    """
    Califica y retroalimenta la entrega de una tarea.
    """
    if request.user.is_parent or request.user.is_student:
        raise PermissionDenied("No tiene permisos para calificar tareas.")

    if request.method == 'POST' and (request.user.is_teacher or request.user.is_admin_role or request.user.is_rector):
        score = request.POST.get('score')
        feedback = request.POST.get('feedback', '').strip()

        try:
            grade_submission(submission_id, score, feedback=feedback, user=request.user)
            messages.success(request, 'Calificación de tarea registrada con éxito.')
        except Exception as e:
            messages.error(request, f'Error al calificar tarea: {str(e)}')

    return redirect('homework:index')
