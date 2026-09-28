from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudentProfile, Enrollment
from .services import enroll_student_in_section, get_or_create_student_profile
from apps.courses.models import CourseSection, AcademicYear
from apps.accounts.models import CustomUser
from apps.courses.services import get_current_academic_year

@login_required
def students_list_view(request):
    """
    Directorio de expedientes estudiantiles y estado de matrículas para la institución activa.
    """
    from apps.courses.models import InstitutionSetting
    inst_type = InstitutionSetting.get_settings().institution_type

    current_year = get_current_academic_year()
    section_id = request.GET.get('section')
    query = request.GET.get('q', '').strip()

    sections = CourseSection.objects.filter(
        academic_year=current_year,
        grade_level__institution_type=inst_type
    ).select_related('grade_level') if current_year else []

    enrollments = Enrollment.objects.filter(
        academic_year=current_year,
        course_section__grade_level__institution_type=inst_type
    ).select_related('student__user', 'student__parent', 'course_section__grade_level') if current_year else []

    if section_id:
        enrollments = enrollments.filter(course_section_id=section_id)
    if query:
        enrollments = enrollments.filter(
            student__user__first_name__icontains=query
        ) | enrollments.filter(
            student__user__last_name__icontains=query
        ) | enrollments.filter(
            student__student_code__icontains=query
        )

    # Estudiantes sin matricular en el año actual (para el modal de matrícula)
    enrolled_student_ids = Enrollment.objects.filter(
        academic_year=current_year,
        course_section__grade_level__institution_type=inst_type
    ).values_list('student__user_id', flat=True) if current_year else []
    available_users = CustomUser.objects.filter(role=CustomUser.Role.STUDENT, is_active=True).exclude(id__in=enrolled_student_ids)

    context = {
        'current_year': current_year,
        'sections': sections,
        'enrollments': enrollments,
        'available_users': available_users,
        'selected_section_id': section_id,
        'query': query,
    }
    return render(request, 'students/list.html', context)

@login_required
def enroll_student_view(request):
    """
    Registra formalmente una matrícula en un curso mediante modal o petición POST.
    """
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        section_id = request.POST.get('section_id')
        year_id = request.POST.get('academic_year_id')
        student_code = request.POST.get('student_code', '').strip()

        user = get_object_or_404(CustomUser, id=user_id, role=CustomUser.Role.STUDENT)
        section = get_object_or_404(CourseSection, id=section_id)
        academic_year = get_object_or_404(AcademicYear, id=year_id)

        try:
            profile = get_or_create_student_profile(user, student_code=student_code or None)
            enroll_student_in_section(
                student_profile=profile,
                course_section=section,
                academic_year=academic_year,
                user=request.user
            )
            messages.success(request, f'Estudiante {user.get_full_name()} matriculado exitosamente en {section.name}.')
        except Exception as e:
            messages.error(request, f'Error al matricular estudiante: {str(e)}')

    return redirect('students:list')


@login_required
def create_student_view(request):
    """
    Registra un nuevo alumno en la institución (Usuario, Perfil y Matrícula) en un solo paso.
    Exclusivo para Secretaría y Directivos.
    """
    if not (request.user.is_admin_role or request.user.is_rector or request.user.is_secretary):
        messages.error(request, 'No tiene permisos para registrar nuevos alumnos.')
        return redirect('students:list')

    if request.method == 'POST':
        from apps.accounts.services import create_institutional_user
        from apps.audit.services import log_audit

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        doc_type = request.POST.get('document_type', 'TI')
        doc_num = request.POST.get('document_number', '').strip()
        student_code = request.POST.get('student_code', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        section_id = request.POST.get('section_id')
        parent_id = request.POST.get('parent_id')

        # Si no se define código, auto-generar uno
        if not student_code:
            student_code = f"EST-{doc_num[-6:] if len(doc_num)>=6 else doc_num}"

        # Username único basado en documento o nombre
        username = f"est_{doc_num}" if doc_num else f"{first_name.lower()[:3]}{last_name.lower()[:3]}"
        if CustomUser.objects.filter(username=username).exists():
            username = f"{username}_{CustomUser.objects.count() + 1}"

        if not email:
            email = f"{username}@academix.edu.co"

        # Contraseña inicial = documento o 'estudiante123'
        password = doc_num if doc_num else 'estudiante123'

        try:
            with __import__('django').db.transaction.atomic():
                # 1. Crear CustomUser con rol STUDENT
                user = create_institutional_user(
                    username=username,
                    email=email,
                    password=password,
                    role=CustomUser.Role.STUDENT,
                    document_type=doc_type,
                    document_number=doc_num,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone or None,
                    must_change_password=True
                )

                # 2. Crear StudentProfile
                parent_user = CustomUser.objects.filter(id=parent_id, role=CustomUser.Role.PARENT).first() if parent_id else None
                profile = get_or_create_student_profile(
                    user=user,
                    student_code=student_code,
                    parent=parent_user
                )

                # 3. Matricular en sección si se seleccionó
                current_year = get_current_academic_year()
                section_name = ""
                if section_id and current_year:
                    section = CourseSection.objects.get(id=section_id)
                    section_name = section.name
                    enroll_student_in_section(
                        student_profile=profile,
                        course_section=section,
                        academic_year=current_year,
                        user=request.user
                    )

                log_audit(
                    user=request.user,
                    action='CREATE_STUDENT',
                    table_name='StudentProfile',
                    record_id=profile.id,
                    new_values={'username': username, 'student_code': student_code, 'section': section_name},
                    reason=f'Registro de nuevo alumno por {request.user.username}',
                    request=request
                )

                messages.success(request, f'¡Estudiante {user.get_full_name()} registrado exitosamente! Usuario: {username} (Contraseña inicial: {password})')
        except Exception as e:
            messages.error(request, f'Error al registrar nuevo estudiante: {str(e)}')

    return redirect('students:list')


@login_required
def student_observations_view(request, student_id):
    """
    Bitácora / Observador del estudiante.
    Muestra el historial de observaciones académicas, convivenciales y citaciones.
    Rector, Secretaría y Docentes pueden registrar nuevas observaciones.
    Estudiantes y Padres solo tienen acceso de lectura (solo lectura estricto).
    """
    from .models import StudentObservation
    student = get_object_or_404(StudentProfile, id=student_id)

    # Restricción de acceso para padres y estudiantes
    if request.user.is_parent:
        if student.parent_id != request.user.id and student.user.id != request.user.id:
            messages.error(request, 'No tiene autorización para consultar las observaciones de este estudiante.')
            return redirect('dashboard')
    elif request.user.is_student:
        if student.user_id != request.user.id:
            messages.error(request, 'Solo puede consultar su propio observador.')
            return redirect('dashboard')

    current_year = get_current_academic_year()
    observations = StudentObservation.objects.filter(student=student).select_related('author', 'academic_year', 'academic_period').order_by('-created_at')

    # Permiso para agregar observaciones: Solo Rector, Secretaría, Docentes y Admin
    can_add_observation = (
        request.user.is_admin_role or
        request.user.is_rector or
        request.user.is_secretary or
        request.user.is_teacher
    )

    from apps.periods.models import AcademicPeriod
    periods = AcademicPeriod.objects.filter(academic_year=current_year).order_by('number') if current_year else []

    context = {
        'student': student,
        'observations': observations,
        'can_add_observation': can_add_observation,
        'current_year': current_year,
        'periods': periods,
        'categories': StudentObservation.Category.choices,
        'severities': StudentObservation.Severity.choices,
    }
    return render(request, 'students/observations.html', context)


@login_required
def create_observation_view(request, student_id):
    """
    Registra una nueva observación para un estudiante.
    Exclusivo para Rector, Secretaría, Docente y Administrador.
    Padres y Estudiantes tienen PROHIBIDA la creación (403).
    """
    if request.user.is_parent or request.user.is_student:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("Los padres y estudiantes no tienen autorización para registrar observaciones.")

    if not (request.user.is_admin_role or request.user.is_rector or request.user.is_secretary or request.user.is_teacher):
        messages.error(request, 'No tiene permisos para registrar observaciones.')
        return redirect('students:list')

    if request.method == 'POST':
        from .models import StudentObservation
        from apps.periods.models import AcademicPeriod
        from apps.audit.services import log_audit

        student = get_object_or_404(StudentProfile, id=student_id)
        current_year = get_current_academic_year()
        period_id = request.POST.get('period_id')
        period = AcademicPeriod.objects.filter(id=period_id).first() if period_id else None

        category = request.POST.get('category', StudentObservation.Category.ACADEMIC)
        severity = request.POST.get('severity', StudentObservation.Severity.INFO)
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        commitments = request.POST.get('commitments', '').strip()
        parent_notified = request.POST.get('parent_notified') == 'on'

        if not title or not description:
            messages.error(request, 'El título y la descripción son obligatorios.')
            return redirect('students:observations', student_id=student.id)

        try:
            obs = StudentObservation.objects.create(
                student=student,
                author=request.user,
                academic_year=current_year or student.current_enrollment.academic_year,
                academic_period=period,
                category=category,
                severity=severity,
                title=title,
                description=description,
                commitments=commitments or None,
                parent_notified=parent_notified
            )

            log_audit(
                user=request.user,
                action='CREATE_OBSERVATION',
                table_name='StudentObservation',
                record_id=obs.id,
                new_values={'student': student.student_code, 'title': title, 'category': category},
                reason=f'Observación agregada por {request.user.get_full_name() or request.user.username}',
                request=request
            )

            messages.success(request, f'Observación "{title}" registrada correctamente en la bitácora del estudiante.')
        except Exception as e:
            messages.error(request, f'Error al registrar observación: {str(e)}')

    return redirect('students:observations', student_id=student_id)


@login_required
def bulk_upload_students_view(request):
    """
    Subida masiva de lista de estudiantes para un curso/sección escolar.
    Permite subir archivo CSV o pegar lista de texto directamente desde Excel.
    Crea automáticamente los usuarios, expedientes y matrículas en lote.
    """
    if request.user.is_parent or request.user.is_student:
        from django.core.exceptions import PermissionDenied
        raise PermissionDenied("Acceso denegado para este rol.")

    import csv
    import io
    from apps.accounts.services import create_institutional_user
    from apps.audit.services import log_audit

    current_year = get_current_academic_year()
    section_id = request.GET.get('section') or request.POST.get('section_id')

    from apps.courses.models import InstitutionSetting
    inst_type = InstitutionSetting.get_settings().institution_type

    if request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        from apps.teachers.models import TeachingAssignment
        assignments = TeachingAssignment.objects.filter(teacher=request.user.teacher_profile, academic_year=current_year, is_active=True)
        sections = CourseSection.objects.filter(
            id__in=assignments.values_list('course_section_id', flat=True),
            grade_level__institution_type=inst_type
        )
    else:
        sections = CourseSection.objects.filter(
            academic_year=current_year,
            grade_level__institution_type=inst_type
        ).select_related('grade_level') if current_year else []

    selected_section = CourseSection.objects.filter(id=section_id, grade_level__institution_type=inst_type).first() if section_id else None

    if request.method == 'POST':
        if not selected_section:
            messages.error(request, 'Debe seleccionar un curso/sección para matricular a los estudiantes.')
            return redirect('students:bulk_upload')

        raw_text = request.POST.get('raw_data', '').strip()
        uploaded_file = request.FILES.get('csv_file')

        rows_data = []

        if uploaded_file:
            # Leer archivo subido
            content = uploaded_file.read()
            for encoding in ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252']:
                try:
                    text_content = content.decode(encoding)
                    break
                except UnicodeDecodeError:
                    continue
            else:
                text_content = content.decode('utf-8', errors='ignore')

            # Detectar delimitador
            sample = text_content[:2048]
            delimiter = ';' if ';' in sample and sample.count(';') > sample.count(',') else (',' if ',' in sample else '\t')
            reader = csv.reader(io.StringIO(text_content), delimiter=delimiter)
            rows_data = list(reader)
        elif raw_text:
            # Procesar texto pegado de Excel o tabla
            delimiter = '\t' if '\t' in raw_text else (';' if ';' in raw_text else ',')
            reader = csv.reader(io.StringIO(raw_text), delimiter=delimiter)
            rows_data = list(reader)

        if not rows_data:
            messages.warning(request, 'No se proporcionaron datos para importar. Suba un archivo CSV o pegue el contenido.')
            return redirect(f"{request.path}?section={selected_section.id}")

        created_count = 0
        enrolled_count = 0
        errors = []
        credentials_to_send = []

        # Analizar encabezados: Si la primera celda no es numérica, es fila de encabezados
        first_col = rows_data[0][0].strip().lower() if rows_data and rows_data[0] else ''
        has_headers = not first_col.isdigit()
        start_idx = 1 if has_headers else 0

        for row_num, row in enumerate(rows_data[start_idx:], start=start_idx + 1):
            if not row or not any(row):
                continue

            cleaned = [c.strip() for c in row]
            if len(cleaned) < 3:
                continue

            # Mapeo posicional estándar:
            # Col 0: Documento
            # Col 1: Tipo Documento (TI, CC, etc.) o Nombre si omitido
            # Col 2: Nombres
            # Col 3: Apellidos
            # Col 4: Email (opcional)
            # Col 5: Teléfono (opcional)
            # Col 6: Código (opcional)
            try:
                doc_num = cleaned[0]
                if not doc_num:
                    continue

                if len(cleaned) >= 4 and cleaned[1].upper() in ['TI', 'CC', 'CE', 'PASSPORT', 'PEP', 'RC']:
                    doc_type = cleaned[1].upper()
                    first_name = cleaned[2]
                    last_name = cleaned[3]
                    email = cleaned[4] if len(cleaned) > 4 and '@' in cleaned[4] else ''
                    phone = cleaned[5] if len(cleaned) > 5 else ''
                    student_code = cleaned[6] if len(cleaned) > 6 else ''
                else:
                    doc_type = 'TI'
                    first_name = cleaned[1] if len(cleaned) > 1 else 'Estudiante'
                    last_name = cleaned[2] if len(cleaned) > 2 else doc_num
                    email = cleaned[3] if len(cleaned) > 3 and '@' in cleaned[3] else ''
                    phone = cleaned[4] if len(cleaned) > 4 else ''
                    student_code = cleaned[5] if len(cleaned) > 5 else ''

                if not student_code:
                    student_code = f"EST-{doc_num[-6:] if len(doc_num)>=6 else doc_num}"

                username = f"est_{doc_num}"
                user_email = email if email else f"{username}@academix.edu.co"
                password = doc_num

                # 1. Buscar o crear usuario
                user = CustomUser.objects.filter(document_number=doc_num).first()
                if not user:
                    user = CustomUser.objects.filter(username=username).first()

                is_new_user = False
                if not user:
                    user = create_institutional_user(
                        username=username,
                        email=user_email,
                        password=password,
                        role=CustomUser.Role.STUDENT,
                        document_type=doc_type,
                        document_number=doc_num,
                        first_name=first_name,
                        last_name=last_name,
                        phone=phone or None,
                        must_change_password=True
                    )
                    created_count += 1
                    is_new_user = True
                else:
                    # Si ya existía y se proporcionó correo real nuevo, actualizarlo
                    if email and user.email != email:
                        user.email = email
                        user.save(update_fields=['email'])

                # 2. Perfil de estudiante
                profile = get_or_create_student_profile(user, student_code=student_code)

                # 3. Matricular en la sección seleccionada
                enroll_student_in_section(
                    student_profile=profile,
                    course_section=selected_section,
                    academic_year=current_year,
                    user=request.user
                )
                enrolled_count += 1

                # 4. Encolar para envío de credenciales por correo
                if is_new_user or user.must_change_password:
                    credentials_to_send.append({
                        'user': user,
                        'password': password,
                        'student_code': student_code,
                        'section_name': selected_section.name,
                        'academic_year': current_year.year if current_year else '',
                        'email': email or user.email,
                    })

            except Exception as ex:
                errors.append(f"Fila {row_num} ({cleaned[0]}): {str(ex)}")

        # Envío automático de credenciales por correo electrónico
        from apps.students.services import send_bulk_student_credentials
        login_url = request.build_absolute_uri('/accounts/login/')
        email_stats = send_bulk_student_credentials(credentials_to_send, login_url=login_url)

        log_audit(
            user=request.user,
            action='BULK_ENROLL_STUDENTS',
            table_name='Enrollment',
            record_id=selected_section.id,
            new_values={
                'section': selected_section.name,
                'enrolled': enrolled_count,
                'created_users': created_count,
                'emails_sent': email_stats['sent'],
                'emails_failed': email_stats['failed'],
            },
            reason=f'Carga masiva de lista de estudiantes en {selected_section.name}',
            request=request
        )

        if enrolled_count > 0:
            success_msg = (
                f'¡Éxito! Se matricularon {enrolled_count} estudiantes en {selected_section.name}. '
                f'({created_count} nuevas cuentas de usuario creadas).'
            )
            if email_stats['sent'] > 0:
                success_msg += f' Se enviaron automáticamente {email_stats["sent"]} correos con el usuario, contraseña inicial y enlace para cambio de contraseña.'
            if email_stats['skipped'] > 0:
                success_msg += f' ({email_stats["skipped"]} estudiantes no tenían correo electrónico válido registrado).'
            messages.success(request, success_msg)

        if errors:
            messages.warning(request, f'Se presentaron {len(errors)} advertencias durante la carga: ' + ' | '.join(errors[:3]))

        return redirect('students:list')

    context = {
        'current_year': current_year,
        'sections': sections,
        'selected_section': selected_section,
        'selected_section_id': str(selected_section.id) if selected_section else '',
    }
    return render(request, 'students/bulk_upload.html', context)


@login_required
def download_student_template_csv(request):
    """
    Descarga una plantilla CSV estructurada para la carga masiva de alumnos por curso.
    """
    import csv
    from django.http import HttpResponse

    response = HttpResponse(content_type='text/csv; charset=utf-8-sig')
    response['Content-Disposition'] = 'attachment; filename="plantilla_carga_masiva_estudiantes.csv"'

    writer = csv.writer(response, delimiter=';')
    writer.writerow(['documento', 'tipo_doc', 'nombres', 'apellidos', 'email', 'telefono', 'codigo_estudiantil'])
    writer.writerow(['1023456789', 'TI', 'Carlos Andrés', 'Gómez Pérez', 'carlos.gomez@ejemplo.edu', '3101234567', 'EST-101'])
    writer.writerow(['1098765432', 'TI', 'María José', 'Rodríguez Silva', 'maria.rodriguez@ejemplo.edu', '3159876543', 'EST-102'])
    writer.writerow(['1055566677', 'CC', 'Juan Camilo', 'Hernández Castro', 'juan.hernandez@ejemplo.edu', '3205556677', 'EST-103'])

    return response


@login_required
def confirm_enrollment_view(request, enrollment_id):
    """
    Confirma (aprueba) la matrícula de un estudiante que estaba en estado PENDIENTE.
    Solo puede ser ejecutado por: Secretaria, Rector o Administrador.
    Al confirmar, el estado pasa de PENDING → ACTIVE.
    """
    if not (request.user.is_admin_role or request.user.is_rector or request.user.is_secretary):
        messages.error(request, 'No tiene permisos para confirmar matrículas.')
        return redirect('students:list')

    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if request.method == 'POST':
        if enrollment.status != Enrollment.Status.PENDING:
            messages.warning(request, f'La matrícula ya estaba en estado: {enrollment.get_status_display()}')
            return redirect('students:list')

        from apps.audit.services import log_audit
        old_status = enrollment.status
        enrollment.status = Enrollment.Status.ACTIVE
        enrollment.save()

        log_audit(
            user=request.user,
            action='CONFIRM_ENROLLMENT',
            table_name='Enrollment',
            record_id=enrollment.id,
            old_values={'status': old_status},
            new_values={
                'status': 'ACTIVE',
                'student': enrollment.student.user.get_full_name(),
                'course': enrollment.course_section.name,
            },
            reason=f'Matrícula confirmada por {request.user.get_full_name() or request.user.username}',
            request=request
        )

        messages.success(
            request,
            f'✅ Matrícula confirmada: {enrollment.student.user.get_full_name()} '
            f'quedó inscrito en {enrollment.course_section.name}.'
        )

    return redirect('students:list')


@login_required
def cancel_enrollment_view(request, enrollment_id):
    """
    Cancela la matrícula de un estudiante, cambiando su estado a WITHDRAWN (Retirado).
    Solo puede ser ejecutado por: Secretaria, Rector o Administrador.
    Registra el evento en el sistema de auditoría.
    """
    if not (request.user.is_admin_role or request.user.is_rector or request.user.is_secretary):
        messages.error(request, 'No tiene permisos para cancelar matrículas.')
        return redirect('students:list')

    enrollment = get_object_or_404(Enrollment, id=enrollment_id)

    if request.method == 'POST':
        if enrollment.status == Enrollment.Status.WITHDRAWN:
            messages.warning(request, 'La matrícula de este estudiante ya estaba cancelada.')
            return redirect('students:list')

        from apps.audit.services import log_audit
        old_status = enrollment.status
        student_name = enrollment.student.user.get_full_name() or enrollment.student.user.username
        course_name = enrollment.course_section.name

        enrollment.status = Enrollment.Status.WITHDRAWN
        enrollment.save()

        log_audit(
            user=request.user,
            action='CANCEL_ENROLLMENT',
            table_name='Enrollment',
            record_id=enrollment.id,
            old_values={'status': old_status},
            new_values={
                'status': 'WITHDRAWN',
                'student': student_name,
                'course': course_name,
            },
            reason=f'Matricula cancelada por {request.user.get_full_name() or request.user.username}',
            request=request
        )

        messages.success(
            request,
            f'La matricula de {student_name} en {course_name} fue cancelada correctamente.'
        )

    return redirect('students:list')
