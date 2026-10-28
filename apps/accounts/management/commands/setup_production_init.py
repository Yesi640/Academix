from decimal import Decimal
import datetime
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from django.db import transaction
from apps.accounts.models import CustomUser, School
from apps.accounts.services import setup_roles_and_permissions, create_institutional_user
from apps.courses.models import AcademicYear, InstitutionSetting, CourseSection, GradeLevel
from apps.courses.services import ensure_standard_colegio_grades, generate_default_sections_for_year
from apps.periods.models import AcademicPeriod
from apps.students.models import StudentProfile, Enrollment
from apps.teachers.models import TeacherProfile, TeachingAssignment
from apps.subjects.models import Subject


class Command(BaseCommand):
    help = 'Inicializa automáticamente usuarios de producción (Admin, Rector, Docente, Alumno, Padre, Secretaría), Año Lectivo y Periodos'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('==> [1/6] Configurando grupos y permisos de roles...'))
        setup_roles_and_permissions()

        admin_password = os.getenv('ADMIN_INITIAL_PASSWORD', 'Academix2026!')
        secretaria_password = os.getenv('SECRETARIA_INITIAL_PASSWORD', '123456789')

        # 1. Parametrización Institucional y Escuelas Multi-Tenant
        self.stdout.write(self.style.NOTICE('==> [2/6] Verificando parametrización institucional y escuelas...'))
        inst_setting = InstitutionSetting.get_settings()
        if not inst_setting.institution_name or inst_setting.institution_name == 'Institución Educativa':
            inst_setting.institution_name = 'ACADEMIX'
            inst_setting.school_scope = InstitutionSetting.SchoolLevelScope.COMPLETA
            inst_setting.save()

        s1 = School.objects.filter(is_active=True).first()
        if not s1:
            s1 = School.objects.create(
                name='Institución Educativa ACADEMIX Central',
                code='ACAD-01',
                city='Sede Principal',
                dane_code='111001000001',
                contact_email='contacto@academix.edu.co',
                contact_phone='+57 300 123 4567',
                primary_color='#7c3aed',
                secondary_color='#c4b5fd',
                is_active=True
            )
            self.stdout.write(self.style.SUCCESS(f'    [OK] Sede escolar principal creada: {s1.name}'))
        else:
            self.stdout.write(self.style.NOTICE(f'    [INFO] Sede escolar activa: {s1.name}'))

        # 2. Año Lectivo y Periodos
        self.stdout.write(self.style.NOTICE('==> [3/6] Verificando Año Lectivo y Periodos Académicos...'))
        current_year = AcademicYear.objects.filter(is_current=True).first()
        if not current_year:
            current_year = AcademicYear.objects.create(
                year=2026,
                name='Año Escolar 2026-2027',
                start_date=datetime.date(2026, 1, 15),
                end_date=datetime.date(2026, 11, 30),
                is_current=True,
                status=AcademicYear.Status.ACTIVE
            )
            self.stdout.write(self.style.SUCCESS('    [OK] Año Lectivo 2026-2027 creado y activado.'))
        else:
            self.stdout.write(self.style.NOTICE(f'    [INFO] Año Lectivo activo: {current_year.name}'))

        # Periodos Académicos
        if not AcademicPeriod.objects.filter(academic_year=current_year).exists():
            periods_def = [
                (1, 'Periodo 1 (Primer Bimestre)', datetime.date(2026, 1, 15), datetime.date(2026, 4, 10), AcademicPeriod.Status.ACTIVE),
                (2, 'Periodo 2 (Segundo Bimestre)', datetime.date(2026, 4, 11), datetime.date(2026, 6, 20), AcademicPeriod.Status.ACTIVE),
                (3, 'Periodo 3 (Tercer Bimestre)', datetime.date(2026, 7, 10), datetime.date(2026, 9, 15), AcademicPeriod.Status.ACTIVE),
                (4, 'Periodo 4 (Cuarto Bimestre)', datetime.date(2026, 9, 16), datetime.date(2026, 11, 28), AcademicPeriod.Status.ACTIVE),
            ]
            for num, name, start, end, status in periods_def:
                AcademicPeriod.objects.create(
                    academic_year=current_year,
                    number=num,
                    name=name,
                    start_date=start,
                    end_date=end,
                    percentage=Decimal('25.00'),
                    status=status
                )
            self.stdout.write(self.style.SUCCESS('    [OK] 4 Periodos académicos creados exitosamente.'))

        # Cursos y Grados estándar
        ensure_standard_colegio_grades(scope=inst_setting.school_scope)
        if not CourseSection.objects.filter(academic_year=current_year).exists():
            generate_default_sections_for_year(current_year)
            self.stdout.write(self.style.SUCCESS('    [OK] Cursos y salones escolares generados.'))

        # 2.1 Catálogo Oficial de Áreas de Conocimiento, Asignaturas y Malla Curricular
        self.stdout.write(self.style.NOTICE('==> [3.5/6] Verificando catálogo oficial de Asignaturas y Mallas por Grado...'))
        from apps.subjects.models import KnowledgeArea, Subject, GradeSubject
        INST = 'COLEGIO'

        AREAS = [
            (1, 'Matemáticas'),
            (2, 'Lengua Castellana e Idiomas'),
            (3, 'Ciencias Naturales y Educación Ambiental'),
            (4, 'Ciencias Sociales, Historia y Geografía'),
            (5, 'Educación Ética y Valores Humanos'),
            (6, 'Educación Religiosa'),
            (7, 'Educación Física, Recreación y Deporte'),
            (8, 'Educación Artística y Cultural'),
            (9, 'Idioma Extranjero Inglés'),
            (10, 'Tecnología e Informática'),
            (11, 'Ciencias Económicas y Políticas'),
            (12, 'Filosofía'),
        ]

        area_objs = {}
        for order, name in AREAS:
            a, _ = KnowledgeArea.objects.get_or_create(
                institution_type=INST,
                name=name,
                defaults={'order': order}
            )
            area_objs[name] = a

        SUBJECTS = [
            ('COL-MAT', 'Matemáticas',                         'PRINCIPAL',    'Matemáticas',                            4),
            ('COL-LEN', 'Lengua Castellana',                   'PRINCIPAL',    'Lengua Castellana e Idiomas',            4),
            ('COL-CNT', 'Ciencias Naturales',                  'PRINCIPAL',    'Ciencias Naturales y Educación Ambiental', 4),
            ('COL-BIO', 'Biología',                            'PRINCIPAL',    'Ciencias Naturales y Educación Ambiental', 3),
            ('COL-FIS', 'Física',                              'PRINCIPAL',    'Ciencias Naturales y Educación Ambiental', 3),
            ('COL-QUI', 'Química',                             'PRINCIPAL',    'Ciencias Naturales y Educación Ambiental', 3),
            ('COL-SOC', 'Ciencias Sociales',                   'PRINCIPAL',    'Ciencias Sociales, Historia y Geografía',  3),
            ('COL-HIS', 'Historia y Geografía',                'HISTORIA',     'Ciencias Sociales, Historia y Geografía',  3),
            ('COL-CON', 'Constitución Política',               'HUMANISTICA',  'Ciencias Sociales, Historia y Geografía',  2),
            ('COL-ETI', 'Ética y Valores',                     'HUMANISTICA',  'Educación Ética y Valores Humanos',       1),
            ('COL-REL', 'Educación Religiosa',                 'HUMANISTICA',  'Educación Religiosa',                     1),
            ('COL-EFI', 'Educación Física',                    'DEPORTE',      'Educación Física, Recreación y Deporte',  2),
            ('COL-ART', 'Educación Artística',                 'ARTE',         'Educación Artística y Cultural',         2),
            ('COL-MUS', 'Música',                              'ARTE',         'Educación Artística y Cultural',         1),
            ('COL-ING', 'Inglés',                              'PRINCIPAL',    'Idioma Extranjero Inglés',                3),
            ('COL-TIC', 'Tecnología e Informática',            'PRINCIPAL',    'Tecnología e Informática',                2),
            ('COL-ECO', 'Economía y Política',                 'HUMANISTICA',  'Ciencias Económicas y Políticas',         2),
            ('COL-FIL', 'Filosofía',                           'HUMANISTICA',  'Filosofía',                               2),
        ]

        sub_objs = {}
        for code, name, cat, area_name, credits in SUBJECTS:
            area = area_objs[area_name]
            s, _ = Subject.objects.get_or_create(
                institution_type=INST,
                code=code,
                defaults={
                    'name': name,
                    'category': cat,
                    'area': area,
                    'credits': credits
                }
            )
            # Asegurar relación con área correcta
            if s.area_id != area.id or s.name != name:
                s.area = area
                s.name = name
                s.category = cat
                s.credits = credits
                s.save()
            sub_objs[code] = s

        CURRICULUM = {
            'GR-00': [('COL-MAT',4),('COL-LEN',5),('COL-CNT',3),('COL-SOC',2),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',2),('COL-TIC',1)],
            'GR-01': [('COL-MAT',5),('COL-LEN',5),('COL-CNT',4),('COL-SOC',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',3),('COL-TIC',2)],
            'GR-02': [('COL-MAT',5),('COL-LEN',5),('COL-CNT',4),('COL-SOC',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',3),('COL-TIC',2)],
            'GR-03': [('COL-MAT',5),('COL-LEN',5),('COL-CNT',4),('COL-SOC',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',3),('COL-TIC',2)],
            'GR-04': [('COL-MAT',5),('COL-LEN',5),('COL-CNT',4),('COL-SOC',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',3),('COL-TIC',2)],
            'GR-05': [('COL-MAT',5),('COL-LEN',5),('COL-CNT',4),('COL-SOC',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',3),('COL-TIC',2)],
            'GR-06': [('COL-MAT',5),('COL-LEN',5),('COL-CNT',4),('COL-SOC',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',4),('COL-TIC',2)],
            'GR-07': [('COL-MAT',5),('COL-LEN',5),('COL-CNT',4),('COL-SOC',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',2),('COL-ING',4),('COL-TIC',2)],
            'GR-08': [('COL-MAT',5),('COL-LEN',4),('COL-BIO',3),('COL-FIS',3),('COL-QUI',3),('COL-HIS',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',1),('COL-ING',4),('COL-TIC',2)],
            'GR-09': [('COL-MAT',5),('COL-LEN',4),('COL-BIO',3),('COL-FIS',3),('COL-QUI',3),('COL-HIS',3),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ART',1),('COL-ING',4),('COL-TIC',2)],
            'GR-10': [('COL-MAT',5),('COL-LEN',4),('COL-BIO',3),('COL-FIS',3),('COL-QUI',3),('COL-HIS',3),('COL-CON',2),('COL-FIL',2),('COL-ECO',2),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ING',4),('COL-TIC',2)],
            'GR-11': [('COL-MAT',5),('COL-LEN',4),('COL-BIO',3),('COL-FIS',3),('COL-QUI',3),('COL-HIS',3),('COL-CON',2),('COL-FIL',2),('COL-ECO',2),('COL-ETI',1),('COL-REL',1),('COL-EFI',2),('COL-ING',4),('COL-TIC',2)],
        }

        for code, subjs in CURRICULUM.items():
            grade = GradeLevel.objects.filter(code=code).first()
            if not grade:
                continue
            for sub_code, hours in subjs:
                s = sub_objs.get(sub_code)
                if s:
                    GradeSubject.objects.get_or_create(
                        grade_level=grade,
                        subject=s,
                        defaults={
                            'weekly_hours': hours,
                            'weight_percentage': Decimal('100.00')
                        }
                    )
        self.stdout.write(self.style.SUCCESS(f'    [OK] Catálogo de {len(sub_objs)} Asignaturas y Mallas por Grado verificadas.'))

        # 3. Limpieza de usuarios residuales: Conservar únicamente las cuentas oficiales requeridas
        self.stdout.write(self.style.NOTICE('==> [4/6] Depurando usuarios: Conservando únicamente cuentas oficiales...'))
        ALLOWED_USERNAMES = {'admin', 'rector', 'docente', 'alumno', 'padre', 'nuryssecretaria'}
        extras = CustomUser.objects.exclude(username__in=ALLOWED_USERNAMES)
        extra_count = extras.count()
        if extra_count > 0:
            with transaction.atomic():
                from django.db.models.deletion import Collector
                from django.db import DEFAULT_DB_ALIAS
                collector = Collector(using=DEFAULT_DB_ALIAS)
                collector.collect(extras)
                collector.delete()
            self.stdout.write(self.style.SUCCESS(f'    [OK] Se eliminaron {extra_count} cuentas residuales del sistema.'))
        else:
            self.stdout.write(self.style.NOTICE('    [INFO] No hay usuarios residuales para depurar.'))

        # 4. Creación / Actualización de los 6 Usuarios Oficiales
        self.stdout.write(self.style.NOTICE('==> [5/6] Creando y asegurando los usuarios oficiales permanentes...'))

        # --- A. Superadministrador ---
        admin_user = CustomUser.objects.filter(username='admin').first()
        if not admin_user:
            admin_user = create_institutional_user(
                username='admin',
                email='admin@academix.edu.co',
                password=admin_password,
                role=CustomUser.Role.ADMIN,
                document_type=CustomUser.DocumentType.CC,
                document_number='1000000001',
                first_name='Administrador',
                last_name='General',
                phone='3001234567',
                address='Sede Central ACADEMIX',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS(f'    [OK] Superusuario creado: admin / {admin_password}'))
        else:
            admin_user.set_password(admin_password)
            admin_user.is_active = True
            admin_user.must_change_password = False
            admin_user.save()
            self.stdout.write(self.style.NOTICE('    [INFO] Usuario admin verificado y actualizado.'))

        # --- B. Rector ---
        rector_user = CustomUser.objects.filter(username='rector').first()
        if not rector_user:
            rector_user = create_institutional_user(
                username='rector',
                email='rector@academix.edu.co',
                password=admin_password,
                role=CustomUser.Role.RECTOR,
                document_type=CustomUser.DocumentType.CC,
                document_number='1000000002',
                first_name='Rector',
                last_name='Institucional',
                phone='3007654321',
                address='Despacho de Rectoría ACADEMIX',
                is_staff=True,
                is_superuser=False
            )
            self.stdout.write(self.style.SUCCESS(f'    [OK] Usuario Rector creado: rector / {admin_password}'))
        else:
            rector_user.set_password(admin_password)
            rector_user.is_active = True
            rector_user.must_change_password = False
            rector_user.save()
            self.stdout.write(self.style.NOTICE('    [INFO] Usuario rector verificado y actualizado.'))

        # --- C. Secretaria (nuryssecretaria / 123456789) ---
        sec_user = CustomUser.objects.filter(username='nuryssecretaria').first()
        if not sec_user:
            sec_user = create_institutional_user(
                username='nuryssecretaria',
                email='nuryssecretaria@academix.edu.co',
                password=secretaria_password,
                role=CustomUser.Role.SECRETARIA,
                document_type=CustomUser.DocumentType.CC,
                document_number='1000000006',
                first_name='Nurys',
                last_name='Secretaría',
                phone='3019876543',
                address='Oficina de Admisiones y Registro ACADEMIX',
                is_staff=True,
                is_superuser=False
            )
            self.stdout.write(self.style.SUCCESS(f'    [OK] Usuario Secretaria creado: nuryssecretaria / {secretaria_password}'))
        else:
            sec_user.set_password(secretaria_password)
            sec_user.is_active = True
            sec_user.must_change_password = False
            sec_user.save()
            self.stdout.write(self.style.NOTICE(f'    [INFO] Usuario nuryssecretaria verificado y actualizado con clave {secretaria_password}.'))

        # --- D. Docente ---
        docente_user = CustomUser.objects.filter(username='docente').first()
        if not docente_user:
            docente_user = create_institutional_user(
                username='docente',
                email='docente@academix.edu.co',
                password=admin_password,
                role=CustomUser.Role.TEACHER,
                document_type=CustomUser.DocumentType.CC,
                document_number='1000000003',
                first_name='Docente',
                last_name='Titular',
                phone='3105551234',
                address='Sala de Docentes ACADEMIX',
                is_staff=False,
                is_superuser=False
            )
            self.stdout.write(self.style.SUCCESS(f'    [OK] Usuario Docente creado: docente / {admin_password}'))
        else:
            docente_user.set_password(admin_password)
            docente_user.is_active = True
            docente_user.must_change_password = False
            docente_user.save()
            self.stdout.write(self.style.NOTICE('    [INFO] Usuario docente verificado y actualizado.'))

        docente_profile, _ = TeacherProfile.objects.get_or_create(
            user=docente_user,
            defaults={'specialty': 'Docencia General y Ciencias'}
        )

        # --- E. Alumno ---
        alumno_user = CustomUser.objects.filter(username='alumno').first()
        if not alumno_user:
            alumno_user = create_institutional_user(
                username='alumno',
                email='alumno@academix.edu.co',
                password=admin_password,
                role=CustomUser.Role.STUDENT,
                document_type=CustomUser.DocumentType.TI,
                document_number='1000000004',
                first_name='Alumno',
                last_name='Ejemplar',
                phone='3124445678',
                address='Barrio Central ACADEMIX',
                is_staff=False,
                is_superuser=False
            )
            self.stdout.write(self.style.SUCCESS(f'    [OK] Usuario Alumno creado: alumno / {admin_password}'))
        else:
            alumno_user.set_password(admin_password)
            alumno_user.is_active = True
            alumno_user.must_change_password = False
            alumno_user.save()
            self.stdout.write(self.style.NOTICE('    [INFO] Usuario alumno verificado y actualizado.'))

        alumno_profile, _ = StudentProfile.objects.get_or_create(
            user=alumno_user,
            defaults={'student_code': 'ALU-2026-1001', 'blood_type': 'O+'}
        )
        if alumno_profile.student_code != 'ALU-2026-1001':
            alumno_profile.student_code = 'ALU-2026-1001'
            alumno_profile.save(update_fields=['student_code'])

        # --- F. Padre de Familia ---
        padre_user = CustomUser.objects.filter(username='padre').first()
        if not padre_user:
            padre_user = create_institutional_user(
                username='padre',
                email='padre@academix.edu.co',
                password=admin_password,
                role=CustomUser.Role.PARENT,
                document_type=CustomUser.DocumentType.CC,
                document_number='1000000005',
                first_name='Padre',
                last_name='Familia',
                phone='3157778899',
                address='Residencia Familiar ACADEMIX',
                is_staff=False,
                is_superuser=False
            )
            self.stdout.write(self.style.SUCCESS(f'    [OK] Usuario Padre creado: padre / {admin_password}'))
        else:
            padre_user.set_password(admin_password)
            padre_user.is_active = True
            padre_user.must_change_password = False
            padre_user.save()
            self.stdout.write(self.style.NOTICE('    [INFO] Usuario padre verificado y actualizado.'))

        # Vincular padre al perfil del alumno
        if alumno_profile.parent_id != padre_user.id:
            alumno_profile.parent = padre_user
            alumno_profile.save(update_fields=['parent'])
            self.stdout.write(self.style.SUCCESS('    [OK] Alumno vinculado formalmente con su acudiente (Padre de Familia).'))

        # Asignar sede escolar a todos los usuarios oficiales
        CustomUser.objects.filter(username__in=ALLOWED_USERNAMES).update(school=s1)

        # 5. Matrícula y Asignación de Aula
        self.stdout.write(self.style.NOTICE('==> [6/6] Vinculando Matrícula y Asignación Académica...'))
        first_section = CourseSection.objects.filter(academic_year=current_year).first()
        if first_section:
            enrollment, enr_created = Enrollment.objects.get_or_create(
                student=alumno_profile,
                academic_year=current_year,
                defaults={'course_section': first_section, 'status': Enrollment.Status.ACTIVE}
            )
            if not enr_created and enrollment.course_section_id != first_section.id:
                enrollment.course_section = first_section
                enrollment.status = Enrollment.Status.ACTIVE
                enrollment.save(update_fields=['course_section', 'status'])
            self.stdout.write(self.style.SUCCESS(f'    [OK] Alumno matriculado en el grupo: {first_section.name}'))

            # Asignar docente al grupo si hay asignaturas
            subject = Subject.objects.filter(institution_type='COLEGIO').first()
            if subject:
                TeachingAssignment.objects.get_or_create(
                    teacher=docente_profile,
                    course_section=first_section,
                    subject=subject,
                    academic_year=current_year,
                    defaults={'is_active': True, 'is_group_director': True}
                )
                self.stdout.write(self.style.SUCCESS(f'    [OK] Docente asignado a {subject.name} en {first_section.name}'))

        self.stdout.write(self.style.SUCCESS('\n============================================================'))
        self.stdout.write(self.style.SUCCESS('*** INICIALIZACION DE USUARIOS Y DATOS COMPLETADA CON EXITO ***'))
        self.stdout.write(self.style.SUCCESS('============================================================'))
        self.stdout.write(self.style.NOTICE('CREDENCIALES INSTITUCIONALES ACTIVAS:'))
        self.stdout.write(f'  1. ADMIN:       Usuario: admin            | Clave: {admin_password}')
        self.stdout.write(f'  2. RECTOR:      Usuario: rector           | Clave: {admin_password}')
        self.stdout.write(f'  3. SECRETARIA:  Usuario: nuryssecretaria  | Clave: {secretaria_password}')
        self.stdout.write(f'  4. DOCENTE:     Usuario: docente          | Clave: {admin_password}')
        self.stdout.write(f'  5. ALUMNO:      ID Único: ALU-2026-1001   | Clave: {admin_password}')
        self.stdout.write(f'  6. PADRE:       Usuario: padre            | ID Hijo: ALU-2026-1001 | Clave: {admin_password}')
        self.stdout.write(self.style.SUCCESS('============================================================\n'))
