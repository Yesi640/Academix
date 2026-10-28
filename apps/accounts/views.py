from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
import json
from .forms import LoginForm, UserProfileForm
from .models import CustomUser, SystemThemeSettings, School
from apps.audit.services import log_audit

def login_view(request):
    """
    Vista de inicio de sesión con soporte multi-escuela.
    Si hay varias escuelas registradas, el usuario elige su institución antes de ingresar.
    """
    from apps.courses.models import InstitutionSetting, AcademicYear

    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    # ── Escuelas activas registradas en la plataforma ──
    active_schools = School.objects.filter(is_active=True).order_by('name')
    selected_school_id = request.POST.get('school_id') or request.GET.get('school_id')
    selected_school = None
    if selected_school_id:
        selected_school = active_schools.filter(pk=selected_school_id).first()

    form = LoginForm(request, data=request.POST or None)
    institution_types = InstitutionSetting.InstitutionType.choices
    current_institution = InstitutionSetting.get_settings()

    if selected_school:
        if selected_school.primary_color:
            current_institution.primary_color = selected_school.primary_color
        if selected_school.secondary_color:
            current_institution.secondary_color = selected_school.secondary_color
        if selected_school.logo:
            current_institution.logo = selected_school.logo
        current_institution.institution_name = selected_school.name

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()

            # Asignar escuela seleccionada al usuario si se eligió una
            if selected_school and user.school_id != selected_school.pk:
                user.school = selected_school
                user.save(update_fields=['school'])

            login(request, user)

            school_name = (user.school.name if user.school else current_institution.institution_name)
            log_audit(
                user=user,
                action='LOGIN',
                table_name='CustomUser',
                record_id=user.id,
                reason=f'Inicio de sesión exitoso — Escuela: {school_name}',
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

            if request.headers.get('HX-Request'):
                response = HttpResponse(status=200)
                response['HX-Redirect'] = '/dashboard/'
                return response

            return redirect('accounts:dashboard')
        else:
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
                    'active_schools': active_schools,
                    'selected_school': selected_school,
                })

    current_academic_year = AcademicYear.objects.filter(is_current=True).first()

    return render(request, 'accounts/login.html', {
        'form': form,
        'institution_types': institution_types,
        'current_institution': current_institution,
        'current_academic_year': current_academic_year,
        'active_schools': active_schools,
        'selected_school': selected_school,
        'multi_school_mode': active_schools.count() > 1,
    })




def register_view(request):
    """
    Registro institucional con selección obligatoria de rol, escuela e ID ÚNICO.
    En modo multi-escuela el usuario elige su institución antes de registrarse.
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

    # ── Escuelas activas disponibles ──
    active_schools = School.objects.filter(is_active=True).order_by('name')
    selected_school_id = request.POST.get('school_id') or request.GET.get('school_id')
    selected_school = active_schools.filter(pk=selected_school_id).first() if selected_school_id else None
    multi_school_mode = active_schools.count() > 1

    if selected_school:
        if selected_school.primary_color:
            current_institution.primary_color = selected_school.primary_color
        if selected_school.secondary_color:
            current_institution.secondary_color = selected_school.secondary_color
        if selected_school.logo:
            current_institution.logo = selected_school.logo
        current_institution.institution_name = selected_school.name

    form = RegistrationForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            role = form.cleaned_data['role']
            username = form.cleaned_data['username']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data.get('email') or f"{username}@academix.edu.co"
            doc_type = form.cleaned_data['document_type']
            doc_num = form.cleaned_data['document_number']
            password = form.cleaned_data['password']

            # Crear CustomUser con escuela asignada
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role,
                first_name=first_name,
                last_name=last_name,
                document_type=doc_type,
                document_number=doc_num,
                school=selected_school,
            )

            extra_msg = ""
            if role == CustomUser.Role.STUDENT:
                unique_suffix = random.randint(1000, 9999)
                generated_id = f"ALU-2026-{unique_suffix}"
                while StudentProfile.objects.filter(student_code=generated_id).exists():
                    unique_suffix = random.randint(1000, 9999)
                    generated_id = f"ALU-2026-{unique_suffix}"

                StudentProfile.objects.create(user=user, student_code=generated_id)
                extra_msg = f" Su ID ÚNICO de Alumno es: <strong>{generated_id}</strong>. Debe usarlo para iniciar sesión."

            elif role == CustomUser.Role.PARENT:
                target_student = form.cleaned_data.get('target_student_profile')
                if target_student:
                    target_student.parent = user
                    target_student.save()
                    extra_msg = f" Quedó vinculado al alumno {target_student.user.get_full_name()}."

            elif role == CustomUser.Role.TEACHER:
                TeacherProfile.objects.create(user=user, specialty='Docencia General')

            school_name = selected_school.name if selected_school else 'Plataforma General'
            log_audit(
                user=user,
                action='REGISTER',
                table_name='CustomUser',
                record_id=user.id,
                new_values={'role': role, 'username': username, 'school': school_name},
                reason=f'Registro de usuario con rol {role} — Escuela: {school_name}',
                request=request
            )

            login(request, user)

            # Enviar correo de bienvenida con credenciales completas
            mail_sent = False
            try:
                from apps.accounts.email_service import send_registration_email
                student_code = None
                if role == CustomUser.Role.STUDENT:
                    sp = StudentProfile.objects.filter(user=user).first()
                    student_code = sp.student_code if sp else None
                mail_sent = send_registration_email(
                    user=user,
                    password=password,
                    student_code=student_code,
                    role_label=user.get_role_display()
                )
            except Exception as mail_err:
                logger.warning(f"No se pudo enviar correo de bienvenida: {mail_err}")

            if mail_sent:
                messages.success(request, f"¡Registro completado! Hemos enviado tus credenciales de acceso a {user.email}.{extra_msg}")
            else:
                messages.success(request, f"¡Registro completado!{extra_msg}")
            return redirect('accounts:dashboard')
        else:
            first_err = form.non_field_errors()[0] if form.non_field_errors() else 'Por favor revise los datos del formulario.'
            messages.error(request, first_err)

    return render(request, 'accounts/register.html', {
        'form': form,
        'institution_types': institution_types,
        'current_institution': current_institution,
        'active_schools': active_schools,
        'selected_school': selected_school,
        'multi_school_mode': multi_school_mode,
    })


def switch_institution_model_view(request):
    """
    Endpoint de terminología institucional fija para Colegio / Escuela.
    """
    from apps.courses.models import InstitutionSetting
    from django.http import JsonResponse

    model_type = request.POST.get('model') or request.GET.get('model') or request.POST.get('institution_type')
    settings_obj = InstitutionSetting.get_settings()
    if model_type and model_type in dict(InstitutionSetting.InstitutionType.choices):
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

    return JsonResponse({
        'status': 'ok',
        'model': 'COLEGIO',
        'model_display': 'Colegio / Escuela (Básica y Media)',
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


@login_required
def users_management_view(request):
    """
    Panel Administrativo Integral de Gestión de Usuarios.
    Permite al Administrador y Rector ver, buscar, filtrar por rol y alternar el estado
    (activo/inactivo) de cualquier usuario de la institución sin necesidad de ingresar al admin de Django.
    """
    if not (request.user.is_admin_role or request.user.is_rector or request.user.is_superuser or request.user.is_staff):
        messages.error(request, 'No tiene permisos para administrar usuarios institucionales.')
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        action = request.POST.get('action')
        target_user_id = request.POST.get('user_id')

        if action == 'toggle_active' and target_user_id:
            try:
                target_user = CustomUser.objects.get(id=target_user_id)
                if target_user.id == request.user.id:
                    messages.warning(request, 'No puedes desactivar tu propia cuenta de acceso actual.')
                else:
                    target_user.is_active = not target_user.is_active
                    target_user.save(update_fields=['is_active'])
                    estado_str = "activado" if target_user.is_active else "desactivado"
                    messages.success(request, f'Usuario {target_user.username} {estado_str} correctamente.')
            except CustomUser.DoesNotExist:
                messages.error(request, 'Usuario no encontrado.')

        elif action == 'create_user':
            username = request.POST.get('new_username', '').strip()
            first_name = request.POST.get('new_first_name', '').strip()
            last_name = request.POST.get('new_last_name', '').strip()
            role = request.POST.get('new_role', '').strip()
            email = request.POST.get('new_email', '').strip()
            password = request.POST.get('new_password', '').strip()
            doc_type = request.POST.get('new_doc_type', 'CC').strip()
            doc_num = request.POST.get('new_doc_num', '').strip() or None

            if not username or not password or not role:
                messages.error(request, 'El nombre de usuario, la contraseña y el rol son obligatorios.')
            elif not email or '@' not in email:
                messages.error(request, 'Debe ingresar un correo electrónico válido para enviarle las credenciales de acceso al usuario.')
            elif CustomUser.objects.filter(username=username).exists():
                messages.error(request, f'El nombre de usuario "{username}" ya existe en el sistema.')
            elif doc_num and CustomUser.objects.filter(document_number=doc_num).exists():
                messages.error(request, f'Ya existe un usuario con el documento {doc_num}.')
            else:
                new_user = CustomUser(
                    username=username,
                    first_name=first_name,
                    last_name=last_name,
                    role=role,
                    email=email or f"{username}@academix.edu.co",
                    document_type=doc_type,
                    document_number=doc_num,
                    is_active=True
                )
                new_user.set_password(password)
                if getattr(request.user, 'school', None):
                    new_user.school = request.user.school
                new_user.save()

                # Crear perfiles institucionales según el rol
                if role == CustomUser.Role.TEACHER:
                    from apps.teachers.models import TeacherProfile
                    TeacherProfile.objects.get_or_create(user=new_user, defaults={'specialty': 'Docencia General'})
                elif role == CustomUser.Role.STUDENT:
                    import random
                    from apps.students.models import StudentProfile
                    code = f"ALU-2026-{random.randint(1000, 9999)}"
                    StudentProfile.objects.get_or_create(user=new_user, defaults={'student_code': code})

                # Notificación por correo si se ingresó email externo
                mail_sent = False
                has_external_mail = bool(email and not email.endswith('@academix.edu.co'))
                if has_external_mail:
                    try:
                        from apps.accounts.email_service import send_registration_email
                        mail_sent = send_registration_email(new_user, password=password, role_label=new_user.get_role_display())
                    except Exception as err:
                        import logging
                        logging.getLogger(__name__).warning(f"Error enviando correo de credenciales: {err}")

                log_audit(
                    user=request.user,
                    action='CREATE',
                    table_name='CustomUser',
                    record_id=new_user.id,
                    new_values={'username': new_user.username, 'role': new_user.role},
                    reason=f'Creación de usuario institucional: {new_user.username} ({new_user.get_role_display()})',
                    request=request
                )

                if mail_sent:
                    messages.success(request, f'¡Usuario {new_user.username} ({new_user.get_role_display()}) creado exitosamente! Credenciales enviadas a {email}.')
                else:
                    messages.success(request, f'¡Usuario {new_user.username} ({new_user.get_role_display()}) creado! Puede ingresar con su usuario "{new_user.username}" o con su documento "{doc_num or username}".')

        return redirect('accounts:users_list')

    role_filter = request.GET.get('role', '').strip()
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()

    users_qs = CustomUser.objects.all().order_by('-date_joined')

    if role_filter:
        users_qs = users_qs.filter(role=role_filter)

    if status_filter == 'active':
        users_qs = users_qs.filter(is_active=True)
    elif status_filter == 'inactive':
        users_qs = users_qs.filter(is_active=False)

    if search_query:
        from django.db.models import Q
        users_qs = users_qs.filter(
            Q(username__icontains=search_query) |
            Q(first_name__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(document_number__icontains=search_query) |
            Q(email__icontains=search_query)
        )

    context = {
        'users_list': users_qs[:200],
        'total_count': users_qs.count(),
        'roles': CustomUser.Role.choices,
        'selected_role': role_filter,
        'search_query': search_query,
        'selected_status': status_filter,
    }
    return render(request, 'accounts/users_list.html', context)


# ══════════════════════════════════════════════════════════════════
#  GESTIÓN DE ESCUELAS  (Solo Administrador de la Plataforma)
# ══════════════════════════════════════════════════════════════════

@login_required
def schools_list_view(request):
    """Lista todas las escuelas registradas en la plataforma."""
    if not (request.user.is_admin_role or request.user.is_rector or request.user.is_superuser):
        messages.error(request, 'Acceso restringido: Solo el Administrador de la plataforma o Rector pueden gestionar escuelas.')
        return redirect('accounts:dashboard')

    schools = School.objects.all().annotate(
        user_count=__import__('django').db.models.Count('users', distinct=True)
    ).order_by('name')

    return render(request, 'accounts/schools_list.html', {
        'schools': schools,
    })


@login_required
def school_create_edit_view(request, school_id=None):
    """Crear o editar una escuela institucional."""
    if not (request.user.is_admin_role or request.user.is_rector or request.user.is_superuser):
        messages.error(request, 'Acceso restringido.')
        return redirect('accounts:dashboard')

    school = get_object_or_404(School, pk=school_id) if school_id else None
    is_new = school is None

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        code = request.POST.get('code', '').strip().upper()
        city = request.POST.get('city', '').strip()
        dane_code = request.POST.get('dane_code', '').strip()
        contact_email = request.POST.get('contact_email', '').strip()
        contact_phone = request.POST.get('contact_phone', '').strip()
        primary_color = request.POST.get('primary_color', '#7c3aed').strip()
        secondary_color = request.POST.get('secondary_color', '#c4b5fd').strip()
        is_active = request.POST.get('is_active') == 'on'

        if not name or not code:
            messages.error(request, 'El nombre y el código de la escuela son obligatorios.')
        elif School.objects.filter(code=code).exclude(pk=school_id).exists():
            messages.error(request, f'Ya existe otra escuela con el código "{code}".')
        else:
            if school is None:
                school = School()
            school.name = name
            school.code = code
            school.city = city
            school.dane_code = dane_code
            school.contact_email = contact_email
            school.contact_phone = contact_phone
            school.primary_color = primary_color
            school.secondary_color = secondary_color
            school.is_active = is_active

            if 'logo' in request.FILES:
                school.logo = request.FILES['logo']

            school.save()

            log_audit(
                user=request.user,
                action='CREATE' if is_new else 'UPDATE',
                table_name='School',
                record_id=school.pk,
                new_values={'name': school.name, 'code': school.code},
                reason=f'{"Creación" if is_new else "Actualización"} de escuela: {school.name}',
                request=request
            )
            messages.success(request, f'Escuela {"creada" if is_new else "actualizada"} exitosamente: {school.name}')
            return redirect('accounts:schools_list')

    return render(request, 'accounts/school_form.html', {
        'school': school,
        'is_new': is_new,
    })


@login_required
@require_POST
def school_toggle_active_view(request, school_id):
    """Activar/desactivar una escuela en la plataforma."""
    if not (request.user.is_admin_role or request.user.is_rector or request.user.is_superuser):
        return JsonResponse({'ok': False, 'error': 'Sin permiso.'}, status=403)

    school = get_object_or_404(School, pk=school_id)
    school.is_active = not school.is_active
    school.save(update_fields=['is_active'])

    log_audit(
        user=request.user,
        action='UPDATE',
        table_name='School',
        record_id=school.pk,
        new_values={'is_active': school.is_active},
        reason=f'Escuela {"activada" if school.is_active else "desactivada"}: {school.name}',
        request=request
    )
    return JsonResponse({'ok': True, 'is_active': school.is_active, 'name': school.name})


@login_required
def school_api_list(request):
    """API pública: retorna lista de escuelas activas (para selector en login/registro)."""
    schools = School.objects.filter(is_active=True).values(
        'id', 'name', 'city', 'primary_color', 'secondary_color', 'contact_email', 'contact_phone'
    ).order_by('name')
    return JsonResponse({'schools': list(schools)})


# ══════════════════════════════════════════════════════════════════
#  RECUPERACIÓN DE CONTRASEÑA (PASSWORD RESET)
# ══════════════════════════════════════════════════════════════════

def password_reset_request_view(request):
    """
    Permite solicitar el restablecimiento de contraseña mediante correo, usuario o documento.
    Envía un enlace seguro firmado con token criptográfico temporal.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    if request.method == 'POST':
        ident = request.POST.get('identifier', '').strip()
        if not ident:
            messages.error(request, 'Debe ingresar su correo, usuario o documento.')
            return render(request, 'accounts/password_reset.html')

        user = (
            CustomUser.objects.filter(email__iexact=ident).first()
            or CustomUser.objects.filter(username__iexact=ident).first()
            or CustomUser.objects.filter(document_number=ident).first()
        )

        if user and user.email and '@' in user.email:
            from django.utils.http import urlsafe_base64_encode
            from django.utils.encoding import force_bytes
            from django.contrib.auth.tokens import default_token_generator
            from django.template.loader import render_to_string
            from django.utils.html import strip_tags
            from django.core.mail import EmailMultiAlternatives
            from django.urls import reverse

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_url = request.build_absolute_uri(
                reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
            )

            context = {
                'user': user,
                'reset_url': reset_url,
            }
            html_message = render_to_string('emails/password_reset.html', context)
            plain_message = strip_tags(html_message)

            try:
                from_email = getattr(settings, 'DEFAULT_FROM_EMAIL', 'ACADEMIX <academix651@gmail.com>')
                msg = EmailMultiAlternatives(
                    subject="ACADEMIX - Restablecimiento de Contraseña",
                    body=plain_message,
                    from_email=from_email,
                    to=[user.email]
                )
                msg.attach_alternative(html_message, "text/html")
                msg.send(fail_silently=False)

                log_audit(
                    user=user,
                    action='PASSWORD_RESET_REQUEST',
                    table_name='CustomUser',
                    record_id=user.id,
                    reason=f'Solicitud de restablecimiento de contraseña para {user.username}',
                    request=request
                )
            except Exception as mail_err:
                logger.warning(f"Error enviando correo de restablecimiento a {user.email}: {mail_err}")

        # Siempre redirigir a done para evitar enumeración de usuarios
        return redirect('accounts:password_reset_done')

    return render(request, 'accounts/password_reset.html')


def password_reset_done_view(request):
    """Confirmación de solicitud de recuperación de contraseña enviada."""
    return render(request, 'accounts/password_reset_done.html')


def password_reset_confirm_view(request, uidb64, token):
    """
    Valida el token de recuperación y permite definir una nueva contraseña.
    """
    from django.utils.http import urlsafe_base64_decode
    from django.contrib.auth.tokens import default_token_generator

    user = None
    validlink = False

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.filter(pk=uid).first()
    except (TypeError, ValueError, OverflowError):
        user = None

    if user and default_token_generator.check_token(user, token):
        validlink = True

    error_msg = None
    if request.method == 'POST' and validlink:
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()

        if not new_password or not confirm_password:
            error_msg = 'Todos los campos son obligatorios.'
        elif len(new_password) < 8:
            error_msg = 'La nueva contraseña debe tener al menos 8 caracteres.'
        elif new_password != confirm_password:
            error_msg = 'Las contraseñas no coinciden.'
        else:
            user.set_password(new_password)
            user.must_change_password = False
            user.save()

            log_audit(
                user=user,
                action='PASSWORD_RESET_COMPLETE',
                table_name='CustomUser',
                record_id=user.id,
                reason=f'Contraseña restablecida exitosamente para {user.username}',
                request=request
            )
            return redirect('accounts:password_reset_complete')

    return render(request, 'accounts/password_reset_confirm.html', {
        'validlink': validlink,
        'error_msg': error_msg,
    })


def password_reset_complete_view(request):
    """Confirmación de que la contraseña fue cambiada exitosamente."""
    return render(request, 'accounts/password_reset_complete.html')

