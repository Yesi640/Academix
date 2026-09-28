from datetime import date
from django.test import TestCase
from django.db import IntegrityError
from apps.accounts.models import CustomUser
from apps.accounts.services import create_institutional_user
from apps.courses.models import AcademicYear, GradeLevel, CourseSection
from apps.subjects.models import KnowledgeArea, Subject
from .models import TeacherProfile, TeachingAssignment
from .services import assign_teacher_to_subject, get_or_create_teacher_profile

class TeachersTests(TestCase):
    def setUp(self):
        self.user = create_institutional_user(
            username='docente_mate',
            email='mate@academix.edu.co',
            password='Password123*',
            role=CustomUser.Role.TEACHER
        )
        self.teacher_profile = get_or_create_teacher_profile(self.user, specialty='Matemáticas')

        self.year = AcademicYear.objects.create(
            year=2026,
            name='Año 2026',
            start_date=date(2026, 1, 15),
            end_date=date(2026, 11, 30),
            status=AcademicYear.Status.ACTIVE,
            is_current=True
        )
        self.grade = GradeLevel.objects.create(name='Séptimo', code='07', order=7)
        self.section = CourseSection.objects.create(academic_year=self.year, grade_level=self.grade, name='7-1')
        self.area = KnowledgeArea.objects.create(name='Matemáticas', order=1)
        self.subject = Subject.objects.create(area=self.area, name='Aritmética', code='ARI-07')

    def test_assign_teacher_success(self):
        assignment = assign_teacher_to_subject(
            teacher=self.teacher_profile,
            course_section=self.section,
            subject=self.subject,
            academic_year=self.year
        )
        self.assertEqual(assignment.teacher, self.teacher_profile)
        self.assertEqual(assignment.subject, self.subject)
        self.assertTrue(assignment.is_active)

    def test_unique_subject_section_assignment(self):
        assign_teacher_to_subject(
            teacher=self.teacher_profile,
            course_section=self.section,
            subject=self.subject,
            academic_year=self.year
        )
        # Crear segundo docente
        user2 = create_institutional_user(
            username='docente_suplente',
            email='suplente@academix.edu.co',
            password='Password123*',
            role=CustomUser.Role.TEACHER
        )
        teacher2 = get_or_create_teacher_profile(user2)

        # Asignar con el servicio actualiza el titular existente sin duplicar
        updated_assignment = assign_teacher_to_subject(
            teacher=teacher2,
            course_section=self.section,
            subject=self.subject,
            academic_year=self.year
        )
        self.assertEqual(TeachingAssignment.objects.count(), 1)
        self.assertEqual(updated_assignment.teacher, teacher2)

    def test_assign_teacher_as_group_director(self):
        """Prueba asignación marcando al docente como director de grupo."""
        assignment = assign_teacher_to_subject(
            teacher=self.teacher_profile,
            course_section=self.section,
            subject=self.subject,
            academic_year=self.year,
            is_group_director=True
        )
        self.assertTrue(assignment.is_group_director)
        self.section.refresh_from_db()
        self.assertEqual(self.section.homeroom_teacher, self.user)
        self.assertTrue(self.user.is_group_director)
