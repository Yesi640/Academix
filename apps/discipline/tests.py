from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import CustomUser
from apps.accounts.services import create_institutional_user
from apps.courses.models import AcademicYear, GradeLevel, CourseSection
from apps.students.models import StudentProfile
from apps.students.services import get_or_create_student_profile, enroll_student_in_section
from .models import AnotacionDisciplinaria
from .services import (
    create_anotacion,
    add_student_disclaimer,
    sign_parent_anotacion,
    close_anotacion,
    get_student_discipline_summary
)


class DisciplineModuleTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.year = AcademicYear.objects.create(
            year=2026, name='Año 2026', start_date=date(2026, 1, 15), end_date=date(2026, 11, 30),
            status=AcademicYear.Status.ACTIVE, is_current=True
        )
        self.grade = GradeLevel.objects.create(name='Noveno', code='09', order=9)
        self.section = CourseSection.objects.create(academic_year=self.year, grade_level=self.grade, name='9-A')

        self.docente = create_institutional_user(
            username='profesor_carlos', email='carlos@academix.edu.co', password='Password123*',
            role=CustomUser.Role.TEACHER, first_name='Carlos', last_name='Docente'
        )
        self.padre = create_institutional_user(
            username='padre_roberto', email='roberto@academix.edu.co', password='Password123*',
            role=CustomUser.Role.PARENT, first_name='Roberto', last_name='Pérez'
        )
        self.estudiante_user = create_institutional_user(
            username='estudiante_mateo', email='mateo@academix.edu.co', password='Password123*',
            role=CustomUser.Role.STUDENT, first_name='Mateo', last_name='Pérez'
        )
        self.estudiante = get_or_create_student_profile(self.estudiante_user, student_code='EST-MATEO', parent=self.padre)
        enroll_student_in_section(self.estudiante, self.section, self.year)

    def test_create_anotacion_service(self):
        record = create_anotacion(
            student_profile=self.estudiante,
            author_user=self.docente,
            academic_year=self.year,
            title='Llegada tarde reiterada',
            description='El estudiante ingresó 20 minutos tarde a la primera sesión sin excusa.',
            fault_type=AnotacionDisciplinaria.FaultType.TIPO_I,
            location='Entrada Principal'
        )
        self.assertIsNotNone(record.id)
        self.assertEqual(record.status, AnotacionDisciplinaria.Status.ABIERTA)
        self.assertFalse(record.is_signed_by_parent)

    def test_parent_digital_signature(self):
        record = create_anotacion(
            student_profile=self.estudiante,
            author_user=self.docente,
            academic_year=self.year,
            title='Falta de implementos de trabajo',
            description='No trajo el material de laboratorio requerido.',
            fault_type=AnotacionDisciplinaria.FaultType.TIPO_I
        )

        signed_record = sign_parent_anotacion(
            record_id=record.id,
            parent_user=self.padre,
            comments='Enterado, se dialogó con el estudiante en casa.'
        )
        self.assertTrue(signed_record.is_signed_by_parent)
        self.assertEqual(signed_record.parent_signature_name, 'Roberto Pérez')
        self.assertEqual(signed_record.parent_comments, 'Enterado, se dialogó con el estudiante en casa.')

    def test_close_anotacion_workflow(self):
        record = create_anotacion(
            student_profile=self.estudiante,
            author_user=self.docente,
            academic_year=self.year,
            title='Uso inadecuado de dispositivo',
            description='Uso de celular durante evaluación.',
            fault_type=AnotacionDisciplinaria.FaultType.TIPO_I
        )

        closed = close_anotacion(
            record_id=record.id,
            directivo_user=self.docente,
            closing_notes='Compromiso formativo verificado satisfactoriamente.'
        )
        self.assertEqual(closed.status, AnotacionDisciplinaria.Status.CERRADA)
        self.assertIsNotNone(closed.closed_at)

    def test_observer_view_rbac_and_rendering(self):
        url = reverse('discipline:observer', kwargs={'student_id': self.estudiante.id})

        # Docente autenticado
        self.client.force_login(self.docente)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Mateo Pérez')
        self.assertContains(resp, 'Observador Escolar')

        # Padre del estudiante autenticado
        self.client.force_login(self.padre)
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
