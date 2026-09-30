from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
import json
from .forms import LoginForm, UserProfileForm
from .models import CustomUser, SystemThemeSettings
from apps.audit.services import log_audit

def login_view(request):
    """
    Vista de inicio de sesión con soporte para peticiones estándar y HTMX.
    Permite seleccionar el modelo institucional (Colegio, Universidad, SENA, Academia)
    antes de ingresar. El entorno se adapta automáticamente al modelo elegido.
    Registra intentos en auditoría inmutable.
    """
    from apps.courses.models import InstitutionSetting

    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    form = LoginForm(request, data=request.POST or None)
    institution_types = InstitutionSetting.InstitutionType.choices
    current_institution = InstitutionSetting.get_settings()

    model_param = request.GET.get('model')
    if model_param and model_param in dict(InstitutionSetting.InstitutionType.choices):
        if current_institution.institution_type != model_param:
            current_institution.apply_preset(model_param)
            current_institution.refresh_from_db()

    if request.method == 'POST':
        # Aplicar el modelo institucional seleccionado antes de autenticar
        selected_type = request.POST.get('institution_type', '').strip()
        if selected_type and selected_type in dict(InstitutionSetting.InstitutionType.choices):
            if current_institution.institution_type != selected_type:
                current_institution.apply_preset(selected_type)
                current_institution.refresh_from_db()

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Registrar login en auditoría
            log_audit(
                user=user,
                action='LOGIN',
                table_name='CustomUser',
                record_id=user.id,
                reason=f'Inicio de sesión exitoso. Modelo institucional: {current_institution.get_institution_type_display()}',
                request=request
            )

            messages.success(request, f'¡Bienvenido a ACADEMIX, {user.get_full_name() or user.username}!')

            if user.must_change_password:
                messages.warning(request, 'Por motivos de seguridad institucional en tu primer acceso, debes cambiar tu contraseña temporal.')
                if request.headers.get('HX-Request'):
                    response = HttpResponse(status=200)
                    response['HX-Redirect'] = '/accounts/change-password/'
                    return response
                return redirect('accounts:change_password')

            # Si la petición viene de HTMX, enviamos cabecera de redirección
            if request.headers.get('HX-Request'):
                response = HttpResponse(status=200)
                response['HX-Redirect'] = '/dashboard/'
                return response

            return redirect('accounts:dashboard')
        else:
            # Registrar intento fallido
            attempted_user = request.POST.get('username') or request.POST.get('student_id') or 'Desconocido'
            err_msg = form.non_field_errors()[0] if form.non_field_errors() else 'Credenciales o datos inválidos. Verifique el rol, usuario e ID ÚNICO.'
            log_audit(
                user=None,
                action='FAILED_LOGIN',
                table_name='CustomUser',
                record_id=None,
                new_values={'attempted_username': attempted_user, 'role': request.POST.get('role')},
                reason=f'Intento fallido de autenticación: {err_msg}',
                request=request
            )
            messages.error(request, err_msg)

            if request.headers.get('HX-Request'):
                return render(request, 'accounts/partials/login_form.html', {
                    'form': form,
                    'institution_types': institution_types,
                    'current_institution': current_institution,
                })

    from apps.courses.models import InstitutionSetting, AcademicYear

    current_academic_year = AcademicYear.objects.filter(is_current=True).first()

    return render(request, 'accounts/login.html', {
        'form': form,
        'institution_types': institution_types,
        'current_institution': current_institution,
        'current_academic_year': current_academic_year,
    })



def register_view(request):
    """
    Registro institucional con selección obligatoria de rol y gestión de ID ÚNICO.
    - Alumno: Asigna automáticamente un ID ÚNICO irrepetible.
    - Padre de Familia: Obligatorio ingresar el ID ÚNICO del alumno a representar.
    - Profesor y Secretaría: Registro y configuración de su respectivo perfil.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    from apps.courses.models import InstitutionSetting
    from .forms import RegistrationForm
    from apps.students.models import StudentProfile
    from apps.teachers.models import TeacherProfile
    import random

    current_institution = InstitutionSetting.get_settings()
    institution_types = InstitutionSetting.InstitutionType.choices

    model_param = request.GET.get('model')
    if model_param and model_param in dict(InstitutionSetting.InstitutionType.choices):
        if current_institution.institution_type != model_param:
            current_institution.apply_preset(model_param)
            current_institution.refresh_from_db()

    form = RegistrationForm(request.POST or None)

    if request.method == 'POST':
        # Aplicar el modelo institucional seleccionado si se especificó
        selected_type = request.POST.get('institution_type', '').strip()
        if selected_type and selected_type in dict(InstitutionSetting.InstitutionType.choices):
            if current_institution.institution_type != selected_type:
                current_institution.apply_preset(selected_type)
                current_institution.refresh_from_db()

        if form.is_valid():
            role = form.cleaned_data['role']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data.get('email') or f"{username}@academix.edu.co"
            doc_type = form.cleaned_data['document_type']
            doc_num = form.cleaned_data['document_number']
            password = form.cleaned_data['password']

            # Crear CustomUser
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
                first_name=first_name,
                last_name=last_name,
                document_type=doc_type,
                document_number=doc_num
            )

            extra_msg = ""
            if role == CustomUser.Role.STUDENT:
                # Generar ID ÚNICO al momento del registro
                unique_suffix = random.randint(1000, 9999)
                generated_id = f"ALU-2026-{unique_suffix}"
                while StudentProfile.objects.filter(student_code=generated_id).exists():
                    unique_suffix = random.randint(1000, 9999)
                    generated_id = f"ALU-2026-{unique_suffix}"

                StudentProfile.objects.create(
                    user=user,
                    student_code=generated_id
                )
                extra_msg = f" Su ID ÚNICO de Alumno es: <strong>{generated_id}</strong>. Debe usarlo para iniciar sesión."

            elif role == CustomUser.Role.PARENT:
                target_student = form.cleaned_data.get('target_student_profile')
                if target_student:
                    target_student.parent = user
                    target_student.save()
                    extra_msg = f" Quedó vinculado al alumno {target_student.user.get_full_name()}."

            elif role == CustomUser.Role.TEACHER:
                TeacherProfile.objects.create(user=user, specialty='Docencia General')

            log_audit(
                user=user,
                action='REGISTER',
                table_name='CustomUser',
                record_id=user.id,
                new_values={'role': role, 'username': username},
                reason=f'Registro de usuario con rol {role}',
                request=request
            )

            login(request, user)

            # ── Enviar email con ID único si el alumno tiene correo real ──
            if role == CustomUser.Role.STUDENT and extra_msg:
                try:
                    from django.core.mail import send_mail
                    from django.template.loader import render_to_string
                    if email and '@academix.edu.co' not in email:
                        generated_code = StudentProfile.objects.get(user=user).student_code
                        send_mail(
                            subject='ACADEMIX – Tu ID Único de Estudiante',
                            message=(
                                f'Hola {user.get_full_name() or user.username},\n\n'
                                f'Tu registro en ACADEMIX fue exitoso.\n'
                                f'Tu ID ÚNICO de alumno es: {generated_code}\n'
                                f'Guárdalo con cuidado; lo necesitarás para iniciar sesión.\n\n'
                                f'ACADEMIX – Sistema de Gestión Educativa'
                            ),
                            from_email=None,
                            recipient_list=[email],
                            fail_silently=True,
                        )
                except Exception:
                    pass

            messages.success(request, f"¡Registro completado!{extra_msg}")
            return redirect('accounts:dashboard')
        else:
            first_err = form.non_field_errors()[0] if form.non_field_errors() else 'Por favor revise los datos del formulario.'
            messages.error(request, first_err)

    return render(request, 'accounts/register.html', {
        'form': form,
        'institution_types': institution_types,
        'current_institution': current_institution,
    })


def switch_institution_model_view(request):
    """
    Endpoint AJAX/GET/POST para cambiar inmediatamente el modelo institucional activo
    y retornar su terminología para adaptación dinámica del frontend en login y registro.
    """
    from apps.courses.models import InstitutionSetting
    from django.http import JsonResponse

    model_type = request.POST.get('model') or request.GET.get('model') or request.POST.get('institution_type')
    settings_obj = InstitutionSetting.get_settings()

    if model_type and model_type in dict(InstitutionSetting.InstitutionType.choices):
        if settings_obj.institution_type != model_type:
            settings_obj.apply_preset(model_type)
            settings_obj.refresh_from_db()
        return JsonResponse({
            'status': 'ok',
            'model': model_type,
            'model_display': settings_obj.get_institution_type_display(),
            'terms': {
                'student': settings_obj.term_student,
                'students': settings_obj.term_students,
                'teacher': settings_obj.term_teacher,
                'teachers': settings_obj.term_teachers,
                'grade': settings_obj.term_grade,
                'section': settings_obj.term_section,
                'sections': settings_obj.term_sections,
                'subject': settings_obj.term_subject,
                'subjects': settings_obj.term_subjects,
                'director': settings_obj.term_director,
            }
        })
    return JsonResponse({'status': 'error', 'message': 'Modelo institucional no válido'}, status=400)

def logout_view(request):
    """
    Cierre de sesión seguro con registro de auditoría.
    """
    if request.user.is_authenticated:
        log_audit(
            user=request.user,
            action='LOGOUT',
            table_name='CustomUser',
            record_id=request.user.id,
            reason='Cierre de sesión manual voluntario',
            request=request
        )
        logout(request)
        messages.info(request, 'Has cerrado sesión satisfactoriamente.')
    return redirect('accounts:login')

@login_required
def dashboard_view(request):
    """
    Dashboard central adaptativo por rol.
    Enriquece el contexto con métricas reales del sistema completo.
    """
    from apps.audit.models import AuditLog
    from apps.courses.models import AcademicYear, CourseSection
    from apps.students.models import Enrollment, StudentProfile
    from apps.teachers.models import TeacherProfile, TeachingAssignment
    from apps.attendance.models import AttendanceRecord
    from apps.grades.models import PeriodFinalGrade
    from apps.alerts.models import SystemAlert
    from apps.homework.models import Homework, HomeworkSubmission
    from apps.periods.models import AcademicPeriod
    from apps.courses.services import get_current_academic_year
    from apps.periods.services import get_current_active_period

    user = request.user
    role = user.role

    if user.must_change_password:
        messages.warning(request, 'Por motivos de seguridad institucional en tu primer acceso, debes cambiar tu contraseña temporal antes de ingresar al panel.')
        return redirect('accounts:change_password')

    current_year = get_current_academic_year()
    active_period = get_current_active_period(current_year) if current_year else None

    # Métricas base siempre calculadas
    total_users = CustomUser.objects.count()
    total_students_qs = CustomUser.objects.filter(role=CustomUser.Role.STUDENT)
    total_teachers_qs = CustomUser.objects.filter(role=CustomUser.Role.TEACHER)

    from apps.courses.models import InstitutionSetting
    inst_type = InstitutionSetting.get_settings().institution_type

    inst_enrollments_qs = Enrollment.objects.filter(
        academic_year=current_year,
        course_section__grade_level__institution_type=inst_type
    ) if current_year else Enrollment.objects.none()

    active_students_count = inst_enrollments_qs.filter(status=Enrollment.Status.ACTIVE).values('student').distinct().count()
    total_sections_count = CourseSection.objects.filter(
        academic_year=current_year,
        grade_level__institution_type=inst_type
    ).count() if current_year else 0

    stats = {
        'total_users': total_users,
        'active_students': active_students_count if active_students_count > 0 else CustomUser.objects.filter(role=CustomUser.Role.STUDENT).count(),
        'active_teachers': total_teachers_qs.count(),
        'current_year': current_year,
        'active_period': active_period,
        'active_alerts': SystemAlert.objects.filter(is_active=True).count(),
        'audit_events_today': AuditLog.objects.filter(
            timestamp__date=__import__('django').utils.timezone.now().date()
        ).count(),
        'total_sections': total_sections_count,
        'total_periods': AcademicPeriod.objects.filter(
            academic_year=current_year).count() if current_year else 0,
    }

    # Métricas específicas por rol
    if user.is_teacher:
        teacher = getattr(user, 'teacher_profile', None)
        if teacher:
            my_assignments = TeachingAssignment.objects.filter(
                teacher=teacher, academic_year=current_year, is_active=True
            ).select_related('course_section', 'subject')
            my_sections_ids = my_assignments.values_list('course_section_id', flat=True).distinct()
            enrolled_in_my_sections = Enrollment.objects.filter(
                course_section_id__in=my_sections_ids,
                academic_year=current_year,
                status=Enrollment.Status.ACTIVE
            ).count()
            pending_homework = Homework.objects.filter(
                teacher=teacher,
                academic_period=active_period,
                is_active=True
            ).count()
            stats['my_assignments_count'] = my_assignments.count()
            stats['my_sections_count'] = my_sections_ids.count()
            stats['enrolled_in_my_sections'] = enrolled_in_my_sections
            stats['pending_homework'] = pending_homework
            stats['my_assignments_list'] = my_assignments[:8]
        else:
            stats['my_assignments_count'] = 0
            stats['my_sections_count'] = 0
            stats['enrolled_in_my_sections'] = 0
            stats['pending_homework'] = 0
            stats['my_assignments_list'] = []

    elif user.is_student:
        student = getattr(user, 'student_profile', None)
        enrollment = None
        my_grades = []
        period_avg = None
        failed_count = 0
        pending_submissions = 0

        if student:
            enrollment = Enrollment.objects.filter(
                student=student, academic_year=current_year
            ).select_related('course_section__grade_level').first()
            if active_period:
                my_grades = PeriodFinalGrade.objects.filter(
                    student=student, academic_period=active_period
                )
            if my_grades:
                scores = [g.final_score for g in my_grades]
                from decimal import Decimal, ROUND_HALF_UP
                period_avg = (sum(scores) / Decimal(str(len(scores)))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                failed_count = sum(1 for g in my_grades if not g.is_approved)
            if enrollment:
                pending_submissions = HomeworkSubmission.objects.filter(
                    student=student, submitted_at__isnull=True
                ).count()

        # Actividades institucionales próximas dirigidas a estudiantes
        from apps.alerts.models import InstitutionalActivity
        from datetime import date as date_cls
        upcoming_activities = InstitutionalActivity.objects.filter(
            is_active=True,
            event_date__gte=date_cls.today(),
            target_audience__in=['ALL', 'STUDENTS']
        ).order_by('event_date', 'event_time')[:5]

        # Notificaciones activas del estudiante
        from django.db.models import Q as _Q
        student_notifications = SystemAlert.objects.filter(
            is_active=True
        ).filter(
            _Q(target_role='STUDENT') |
            _Q(recipient_user=user) |
            _Q(recipient_user__isnull=True, target_role__isnull=True)
        ).order_by('-created_at')[:5]

        stats['enrollment'] = enrollment
        stats['period_avg'] = period_avg
        stats['failed_count'] = failed_count
        stats['grades_count'] = len(list(my_grades)) if my_grades else 0
        stats['pending_submissions'] = pending_submissions
        stats['upcoming_activities'] = upcoming_activities
        stats['student_notifications'] = student_notifications


    elif user.is_parent:
        # Acudientes: hijos a cargo
        dependents = StudentProfile.objects.filter(parent=user).select_related('user')
        stats['dependents'] = dependents
        stats['dependents_count'] = dependents.count()

    elif user.is_admin_role or user.is_rector:
        # Estadísticas ejecutivas completas
        active_enrollments = Enrollment.objects.filter(
            academic_year=current_year, status=Enrollment.Status.ACTIVE
        ).count() if current_year else 0
        period_grades_count = PeriodFinalGrade.objects.filter(
            academic_period=active_period
        ).count() if active_period else 0
        recent_audit = AuditLog.objects.select_related('user').order_by('-timestamp')[:6]
        stats['active_enrollments'] = active_enrollments
        stats['period_grades_count'] = period_grades_count
        stats['recent_audit'] = recent_audit
        stats['closed_periods'] = AcademicPeriod.objects.filter(
            academic_year=current_year,
            status__in=['CLOSED', 'LOCKED']
        ).count() if current_year else 0
        stats['pending_alerts'] = SystemAlert.objects.filter(
            is_active=True, level='WARNING'
        ).count()

    elif user.is_secretary:
        pending_enrollments = Enrollment.objects.filter(
            academic_year=current_year
        ).count() if current_year else 0
        stats['pending_enrollments'] = pending_enrollments
        stats['total_sections'] = CourseSection.objects.filter(
            academic_year=current_year).count() if current_year else 0

    context = {
        'user': user,
        'role': role,
        'role_display': user.get_role_display(),
        'role_badge': user.get_role_badge_class(),
        'stats': stats,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def profile_view(request):
    """
    Vista y edición de perfil del usuario con actualización reactiva HTMX.
    """
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            old_data = {'phone': user.phone, 'address': user.address, 'email': user.email}
            form.save()
            new_data = {'phone': user.phone, 'address': user.address, 'email': user.email}
            
            log_audit(
                user=user,
                action='UPDATE',
                table_name='CustomUser',
                record_id=user.id,
                old_values=old_data,
                new_values=new_data,
                reason='Actualización de datos personales de perfil',
                request=request
            )
            messages.success(request, 'Perfil actualizado correctamente.')
            if request.headers.get('HX-Request'):
                return render(request, 'accounts/partials/profile_card.html', {'user': user, 'form': form})
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'accounts/profile.html', {'form': form, 'user': user})


@login_required
def change_password_view(request):
    """
    Permite al usuario autenticado cambiar su contraseña temporal o voluntariamente.
    Si tenía must_change_password=True, se desactiva tras el cambio exitoso.
    Preserva la sesión activa y registra el evento en auditoría inmutable.
    """
    from django.contrib.auth import update_session_auth_hash
    from django.contrib.auth.forms import PasswordChangeForm

    user = request.user
    must_change = user.must_change_password

    if request.method == 'POST':
        form = PasswordChangeForm(user=user, data=request.POST)
        if form.is_valid():
            user = form.save()
            if user.must_change_password:
                user.must_change_password = False
                user.save(update_fields=['must_change_password'])

            # Evitar que la sesión expire al cambiar la contraseña
            update_session_auth_hash(request, user)

            log_audit(
                user=user,
                action='UPDATE',
                table_name='CustomUser',
                record_id=user.id,
                reason='Cambio de contraseña realizado por el usuario',
                request=request
            )

            messages.success(request, '¡Tu contraseña ha sido actualizada exitosamente! Ya puedes continuar con seguridad.')
            return redirect('accounts:dashboard')
        else:
            for error in form.non_field_errors():
                messages.error(request, error)
    else:
        form = PasswordChangeForm(user=user)

    return render(request, 'accounts/change_password.html', {
        'form': form,
        'must_change': must_change,
        'user': user,
    })


@login_required
@require_POST
def rector_save_global_theme(request):
    """
    Vista exclusiva del Rector para guardar el tema global del sistema.
    Solo el rol RECTOR (o ADMIN) puede llamar a este endpoint.
    El tema se persiste en base de datos y sera visible para todos los usuarios
    como tema institucional base.
    """
    user = request.user
    if user.role not in (CustomUser.Role.RECTOR, CustomUser.Role.ADMIN) and not user.is_superuser:
        return JsonResponse({'ok': False, 'error': 'Sin permiso. Solo el Rector puede modificar el tema global.'}, status=403)

    try:
        body = json.loads(request.body)
        theme_data = body.get('theme_data', {})
        if not isinstance(theme_data, dict) or not theme_data:
            return JsonResponse({'ok': False, 'error': 'Datos de tema invalidos.'}, status=400)

        # Marcar que es el tema global del sistema
        theme_data['_global'] = True
        theme_data['_updated_by'] = user.get_full_name() or user.username

        SystemThemeSettings.set_global_theme(theme_data, user)

        log_audit(
            user=user,
            action='UPDATE',
            table_name='SystemThemeSettings',
            record_id=1,
            reason=f'Rector actualizo tema global del sistema: {theme_data.get("name", "(sin nombre)")}',
            request=request
        )

        return JsonResponse({'ok': True, 'message': 'Tema institucional guardado correctamente.'})
    except (json.JSONDecodeError, Exception) as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=400)


@login_required
def get_global_theme_api(request):
    """
    Retorna el tema global del sistema como JSON.
    Todos los usuarios autenticados pueden consultar este endpoint.
    """
    theme = SystemThemeSettings.get_global_theme()
    if theme:
        return JsonResponse({'ok': True, 'theme': theme})
    return JsonResponse({'ok': False, 'theme': None})
