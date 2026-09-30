from datetime import date
from django.test import TestCase
from apps.accounts.models import CustomUser
from apps.accounts.services import create_institutional_user
from apps.courses.models import AcademicYear, GradeLevel, CourseSection
from .models import StudentProfile, Enrollment
from .services import enroll_student_in_section, get_or_create_student_profile

class StudentsTests(TestCase):
    def setUp(self):
        self.user = create_institutional_user(
            username='estudiante_juan',
            email='juan@academix.edu.co',
            password='Password123*',
            role=CustomUser.Role.STUDENT
        )
        self.profile = get_or_create_student_profile(self.user, student_code='EST-2026-001')

        self.year = AcademicYear.objects.create(
            year=2026,
            name='Año 2026',
            start_date=date(2026, 1, 15),
            end_date=date(2026, 11, 30),
            status=AcademicYear.Status.ACTIVE,
            is_current=True
        )
        self.grade = GradeLevel.objects.create(name='Sexto', code='06', order=6)
        self.section1 = CourseSection.objects.create(academic_year=self.year, grade_level=self.grade, name='6-A')
        self.section2 = CourseSection.objects.create(academic_year=self.year, grade_level=self.grade, name='6-B')

    def test_enrollment_success(self):
        enrollment = enroll_student_in_section(
            student_profile=self.profile,
            course_section=self.section1,
            academic_year=self.year
        )
        self.assertEqual(enrollment.student, self.profile)
        self.assertEqual(enrollment.course_section, self.section1)
        self.assertEqual(enrollment.status, Enrollment.Status.ACTIVE)

    def test_single_enrollment_per_year_update(self):
        # Matricular en 6-A
        enroll_student_in_section(
            student_profile=self.profile,
            course_section=self.section1,
            academic_year=self.year
        )
        # Trasladar a 6-B en el mismo año escolar actualiza la matrícula sin duplicar
        updated = enroll_student_in_section(
            student_profile=self.profile,
            course_section=self.section2,
            academic_year=self.year
        )
        self.assertEqual(Enrollment.objects.filter(student=self.profile, academic_year=self.year).count(), 1)
        self.assertEqual(updated.course_section, self.section2)


class ExpedienteDigitalRBACAndServicesTests(TestCase):
    """
    Pruebas unitarias para el Módulo 2: Carpeta Perpetua y Expediente Digital con RBAC.
    """
    def setUp(self):
        from django.test import Client
        from django.core.files.uploadedfile import SimpleUploadedFile
        from apps.teachers.models import TeacherProfile, TeachingAssignment
        from apps.periods.models import AcademicPeriod
        from .models import ExpedienteDocumento

        self.client = Client()

        # Año y grado
        self.year = AcademicYear.objects.create(
            year=2026, name='Año 2026', start_date=date(2026, 1, 15), end_date=date(2026, 11, 30),
            status=AcademicYear.Status.ACTIVE, is_current=True
        )
        self.grade = GradeLevel.objects.create(name='Octavo', code='08', order=8)
        self.section = CourseSection.objects.create(academic_year=self.year, grade_level=self.grade, name='8-A')

        # Usuarios
        self.secretaria = create_institutional_user(
            username='sec_expediente', email='sec@academix.edu.co', password='Password123*',
            role=CustomUser.Role.SECRETARIA
        )
        self.padre1 = create_institutional_user(
            username='padre_carlos', email='padre1@academix.edu.co', password='Password123*',
            role=CustomUser.Role.PARENT
        )
        self.padre2 = create_institutional_user(
            username='padre_pedro', email='padre2@academix.edu.co', password='Password123*',
            role=CustomUser.Role.PARENT
        )

        self.student_user1 = create_institutional_user(
            username='alumno_lucas', email='lucas@academix.edu.co', password='Password123*',
            role=CustomUser.Role.STUDENT, first_name='Lucas', last_name='Gómez'
        )
        self.student1 = get_or_create_student_profile(self.student_user1, student_code='EST-LUCAS', parent=self.padre1)
        enroll_student_in_section(self.student1, self.section, self.year)

        self.student_user2 = create_institutional_user(
            username='alumno_sara', email='sara@academix.edu.co', password='Password123*',
            role=CustomUser.Role.STUDENT, first_name='Sara', last_name='Díaz'
        )
        self.student2 = get_or_create_student_profile(self.student_user2, student_code='EST-SARA', parent=self.padre2)

        # Docentes
        from apps.subjects.models import Subject, KnowledgeArea
        self.area = KnowledgeArea.objects.create(name='Ciencias')
        self.subject = Subject.objects.create(name='Ciencias Naturales', code='CN-08', area=self.area)
        self.docente_dir_user = create_institutional_user(
            username='profe_director', email='dir@academix.edu.co', password='Password123*',
            role=CustomUser.Role.TEACHER
        )
        self.docente_dir = TeacherProfile.objects.create(user=self.docente_dir_user, specialty='Ciencias')
        TeachingAssignment.objects.create(
            teacher=self.docente_dir, course_section=self.section, subject=self.subject, academic_year=self.year,
            is_group_director=True, is_active=True
        )

        self.docente_otro_user = create_institutional_user(
            username='profe_otro', email='otro@academix.edu.co', password='Password123*',
            role=CustomUser.Role.TEACHER
        )
        self.docente_otro = TeacherProfile.objects.create(user=self.docente_otro_user, specialty='Sociales')

        self.dummy_file = SimpleUploadedFile("registro_civil.pdf", b"Contenido de prueba PDF", content_type="application/pdf")

    def test_rbac_access_matrix(self):
        """Prueba la matriz estricta de control de acceso basada en roles al expediente."""
        from django.urls import reverse
        url = reverse('students:expediente', kwargs={'student_id': self.student1.id})

        # 1. Secretaría: Acceso concedido
        self.client.force_login(self.secretaria)
        self.assertEqual(self.client.get(url).status_code, 200)

        # 2. Docente Director del curso de Lucas: Acceso concedido
        self.client.force_login(self.docente_dir_user)
        self.assertEqual(self.client.get(url).status_code, 200)

        # 3. Docente que NO es director del curso: Acceso denegado (HTTP 403)
        self.client.force_login(self.docente_otro_user)
        self.assertEqual(self.client.get(url).status_code, 403)

        # 4. Padre de Lucas: Acceso concedido
        self.client.force_login(self.padre1)
        self.assertEqual(self.client.get(url).status_code, 200)

        # 5. Padre de otro estudiante (Sara): Acceso denegado (HTTP 403)
        self.client.force_login(self.padre2)
        self.assertEqual(self.client.get(url).status_code, 403)

        # 6. Propio estudiante: Acceso concedido
        self.client.force_login(self.student_user1)
        self.assertEqual(self.client.get(url).status_code, 200)

        # 7. Otro estudiante ajeno: Acceso denegado (HTTP 403)
        self.client.force_login(self.student_user2)
        self.assertEqual(self.client.get(url).status_code, 403)

    def test_upload_and_verify_expediente_document(self):
        """Prueba subida y verificación oficial con firma de secretaría."""
        from .models import ExpedienteDocumento
        from .services import verify_expediente_document

        doc = ExpedienteDocumento.objects.create(
            student=self.student1,
            category=ExpedienteDocumento.Category.ADMISSION,
            document_type=ExpedienteDocumento.DocumentType.REGISTRO_CIVIL,
            title='Registro Civil Original',
            file=self.dummy_file,
            academic_year=self.year,
            uploaded_by=self.secretaria,
            is_verified=False
        )
        self.assertFalse(doc.is_verified)
        self.assertTrue('expedientes/student_' in doc.file.name)

        # Verificar
        verified_doc = verify_expediente_document(doc.id, self.secretaria)
        self.assertTrue(verified_doc.is_verified)
        self.assertEqual(verified_doc.verified_by, self.secretaria)
        self.assertIsNotNone(verified_doc.verified_at)

    def test_admission_checklist_validator(self):
        """Valida cálculo de requisitos completos y pendientes de matrícula."""
        from .models import ExpedienteDocumento
        from .services import validate_admission_checklist

        chk_initial = validate_admission_checklist(self.student1)
        self.assertFalse(chk_initial['is_complete'])
        self.assertEqual(chk_initial['completed_count'], 0)

        # Adjuntar documento de identidad
        ExpedienteDocumento.objects.create(
            student=self.student1,
            category=ExpedienteDocumento.Category.ADMISSION,
            document_type=ExpedienteDocumento.DocumentType.TARJETA_IDENTIDAD,
            title='Tarjeta de Identidad',
            file=self.dummy_file,
            uploaded_by=self.secretaria
        )

        chk_partial = validate_admission_checklist(self.student1)
        self.assertTrue(chk_partial['completed_count'] >= 1)
        self.assertTrue(chk_partial['percentage'] > 0)

    def test_attach_bulletin_to_expediente_automation(self):
        """Prueba la inyección automática del boletín en la carpeta perpetua."""
        from apps.periods.models import AcademicPeriod
        from .services import attach_bulletin_to_expediente
        from .models import ExpedienteDocumento

        period = AcademicPeriod.objects.create(
            academic_year=self.year, number=1, name='Periodo 1',
            start_date=date(2026, 2, 1), end_date=date(2026, 4, 30),
            percentage=Decimal('25.00'), status=AcademicPeriod.Status.CLOSED
        )

        doc = attach_bulletin_to_expediente(
            student_profile=self.student1,
            period=period,
            pdf_content=b"%PDF-1.4 Fake PDF Content",
            filename="boletin_test.pdf",
            user=self.secretaria
        )

        self.assertIsNotNone(doc.id)
        self.assertEqual(doc.category, ExpedienteDocumento.Category.ACADEMIC)
        self.assertEqual(doc.document_type, ExpedienteDocumento.DocumentType.BOLETIN_OFICIAL)
        self.assertTrue(doc.is_verified)
        self.assertTrue(doc.file.name.endswith('.pdf'))

