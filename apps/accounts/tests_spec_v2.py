from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from django.core.exceptions import PermissionDenied, ValidationError
from apps.accounts.models import CustomUser
from apps.accounts.services import create_institutional_user, setup_roles_and_permissions
from apps.students.models import StudentProfile, Enrollment
from apps.courses.models import GradeLevel, CourseSection, AcademicYear
from apps.periods.models import AcademicPeriod
from apps.subjects.models import KnowledgeArea, Subject, GradeSubject
from apps.teachers.models import TeacherProfile, TeachingAssignment
from apps.homework.models import Homework, HomeworkSubmission
from apps.homework.services import grade_or_create_submission, bulk_grade_homework_list
from apps.grades.models import EvaluationCriterion, GradeRecord
from apps.grades.services import save_or_update_grade
from datetime import date, timedelta
from django.utils import timezone

class FunctionalSpecTests(TestCase):
    def setUp(self):
        setup_roles_and_permissions()

        # Academic structure
        self.year = AcademicYear.objects.create(
            year=2026,
            name="2026",
            start_date=date(2026, 1, 15),
            end_date=date(2026, 11, 30),
            status=AcademicYear.Status.ACTIVE,
            is_current=True
        )
        self.period = AcademicPeriod.objects.create(
            academic_year=self.year,
            name="Periodo 1",
            number=1,
            start_date=date(2026, 1, 15),
            end_date=date(2026, 4, 15),
            status=AcademicPeriod.Status.ACTIVE
        )
        self.grade_6 = GradeLevel.objects.create(name="Sexto", code="6", order=1)
        self.grade_7 = GradeLevel.objects.create(name="Septimo", code="7", order=2)

        self.area = KnowledgeArea.objects.create(name="Matemáticas", order=1)
        self.subject = Subject.objects.create(name="Matemáticas", code="MAT-6", area=self.area)

        # Teachers
        self.teacher_user = create_institutional_user(
            username='profe_juan',
            email='juan@academix.edu',
            password='TestPassword123!',
            role=CustomUser.Role.TEACHER,
            document_type=CustomUser.DocumentType.CC,
            document_number='11111111'
        )
        self.teacher_profile = TeacherProfile.objects.create(user=self.teacher_user)

        self.other_teacher_user = create_institutional_user(
            username='profe_maria',
            email='maria@academix.edu',
            password='TestPassword123!',
            role=CustomUser.Role.TEACHER,
            document_type=CustomUser.DocumentType.CC,
            document_number='22222222'
        )
        self.other_teacher_profile = TeacherProfile.objects.create(user=self.other_teacher_user)

        # Secretary
        self.secretary_user = create_institutional_user(
            username='secre_lucia',
            email='lucia@academix.edu',
            password='TestPassword123!',
            role=CustomUser.Role.SECRETARIA,
            document_type=CustomUser.DocumentType.CC,
            document_number='33333333'
        )

        # Sections
        self.section_6a = CourseSection.objects.create(
            name="6-A",
            grade_level=self.grade_6,
            academic_year=self.year,
            homeroom_teacher=self.teacher_user
        )
        self.section_7a = CourseSection.objects.create(
            name="7-A",
            grade_level=self.grade_7,
            academic_year=self.year,
            homeroom_teacher=self.other_teacher_user
        )

        # Assign teacher to 6-A only
        TeachingAssignment.objects.create(
            teacher=self.teacher_profile,
            course_section=self.section_6a,
            subject=self.subject,
            academic_year=self.year,
            is_active=True
        )

        # Student user & profile
        self.student_user = create_institutional_user(
            username='alumno_pedro',
            email='pedro@academix.edu',
            password='TestPassword123!',
            role=CustomUser.Role.STUDENT,
            document_type=CustomUser.DocumentType.TI,
            document_number='44444444'
        )
        self.student_profile = StudentProfile.objects.create(
            user=self.student_user,
            student_code='ALU-2026-9999'
        )
        Enrollment.objects.create(
            student=self.student_profile,
            course_section=self.section_6a,
            academic_year=self.year,
            status=Enrollment.Status.ACTIVE
        )

        # Parent user linked to student
        self.parent_user = create_institutional_user(
            username='padre_carlos',
            email='carlos@academix.edu',
            password='TestPassword123!',
            role=CustomUser.Role.PARENT,
            document_type=CustomUser.DocumentType.CC,
            document_number='55555555'
        )
        self.student_profile.parent = self.parent_user
        self.student_profile.save()

        # Homework
        self.homework = Homework.objects.create(
            course_section=self.section_6a,
            subject=self.subject,
            teacher=self.teacher_profile,
            academic_period=self.period,
            title="Taller 1",
            description="Ejercicios del 1 al 10",
            due_date=timezone.now() + timedelta(days=2)
        )

    def test_student_login_requires_student_id(self):
        client = Client()
        # Missing student_id for student role
        resp = client.post(reverse('accounts:login'), {
            'username': 'alumno_pedro',
            'password': 'TestPassword123!',
            'role': CustomUser.Role.STUDENT,
            'student_id': ''
        })
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'obligatorio')

        # Correct login with student_id
        resp_ok = client.post(reverse('accounts:login'), {
            'username': 'alumno_pedro',
            'password': 'TestPassword123!',
            'role': CustomUser.Role.STUDENT,
            'student_id': 'ALU-2026-9999'
        })
        self.assertEqual(resp_ok.status_code, 302)

    def test_parent_login_requires_represented_student_id(self):
        client = Client()
        # Non-existent student_id
        resp_fail = client.post(reverse('accounts:login'), {
            'username': 'padre_carlos',
            'password': 'TestPassword123!',
            'role': CustomUser.Role.PARENT,
            'student_id': 'ALU-2026-0000'
        })
        self.assertEqual(resp_fail.status_code, 200)
        self.assertContains(resp_fail, 'No existe')

        # Create another student not related to this parent
        other_user = create_institutional_user(
            username='alumno_otro',
            email='otro@academix.edu',
            password='TestPassword123!',
            role=CustomUser.Role.STUDENT,
            document_type=CustomUser.DocumentType.TI,
            document_number='99999999'
        )
        StudentProfile.objects.create(
            user=other_user,
            student_code='ALU-2026-1111'
        )

        resp_fail_rel = client.post(reverse('accounts:login'), {
            'username': 'padre_carlos',
            'password': 'TestPassword123!',
            'role': CustomUser.Role.PARENT,
            'student_id': 'ALU-2026-1111'
        })
        self.assertEqual(resp_fail_rel.status_code, 200)
        self.assertContains(resp_fail_rel, 'no coincide')

        # Correct student_id
        resp_ok = client.post(reverse('accounts:login'), {
            'username': 'padre_carlos',
            'password': 'TestPassword123!',
            'role': CustomUser.Role.PARENT,
            'student_id': 'ALU-2026-9999'
        })
        self.assertEqual(resp_ok.status_code, 302)

    def test_teacher_course_isolation(self):
        client = Client()
        client.login(username='profe_juan', password='TestPassword123!')

        # Allowed: Section 6-A (assigned)
        resp = client.get(reverse('homework:course_matrix', args=[self.section_6a.id]))
        self.assertEqual(resp.status_code, 200)

        # Forbidden: Section 7-A (not assigned to Juan)
        resp_forbidden = client.get(reverse('homework:course_matrix', args=[self.section_7a.id]))
        self.assertEqual(resp_forbidden.status_code, 403)

    def test_malla_curricular_access_exclusivity(self):
        client = Client()

        # Teacher: Allowed
        client.login(username='profe_juan', password='TestPassword123!')
        resp_teacher = client.get(reverse('subjects:curriculum'))
        self.assertEqual(resp_teacher.status_code, 200)

        # Secretary: Allowed
        client.login(username='secre_lucia', password='TestPassword123!')
        resp_sec = client.get(reverse('subjects:curriculum'))
        self.assertEqual(resp_sec.status_code, 200)

        # Rector / Directivos: Allowed
        client.login(username='rector_alberto', password='TestPassword123!')
        resp_rector = client.get(reverse('subjects:curriculum'))
        self.assertEqual(resp_rector.status_code, 200)

        # Student: Forbidden
        client.login(username='alumno_pedro', password='TestPassword123!')
        resp_std = client.get(reverse('subjects:curriculum'))
        self.assertEqual(resp_std.status_code, 403)

        # Parent: Forbidden
        client.login(username='padre_carlos', password='TestPassword123!')
        resp_parent = client.get(reverse('subjects:curriculum'))
        self.assertEqual(resp_parent.status_code, 403)

    def test_grade_immutability(self):
        # Grade homework submission for the first time
        sub = grade_or_create_submission(
            homework_id=self.homework.id,
            student_id=self.student_profile.id,
            score=Decimal('8.50'),
            feedback='Buen trabajo',
            user=self.teacher_user
        )
        self.assertTrue(sub.is_locked)
        self.assertEqual(sub.score, Decimal('8.50'))

        # Attempt to modify the locked submission -> must raise ValidationError
        with self.assertRaises(ValidationError):
            grade_or_create_submission(
                homework_id=self.homework.id,
                student_id=self.student_profile.id,
                score=Decimal('9.50'),
                feedback='Intento de cambio',
                user=self.teacher_user
            )

        # Check in DB it remained unchanged
        sub.refresh_from_db()
        self.assertEqual(sub.score, Decimal('8.50'))

    def test_bulk_grade_homework_list(self):
        # Collective grade update
        updated, skipped = bulk_grade_homework_list(
            section=self.section_6a,
            grades_data=[{
                'student_id': str(self.student_profile.id),
                'homework_id': str(self.homework.id),
                'score': '9.00',
                'feedback': 'Excelente desempeño'
            }],
            user=self.teacher_user
        )
        self.assertEqual(updated, 1)
        self.assertEqual(skipped, 0)

        # Second collective grade attempt on the same locked item -> skipped and unchanged
        updated2, skipped2 = bulk_grade_homework_list(
            section=self.section_6a,
            grades_data=[{
                'student_id': str(self.student_profile.id),
                'homework_id': str(self.homework.id),
                'score': '5.00',
                'feedback': 'Cambio no permitido'
            }],
            user=self.teacher_user
        )
        self.assertEqual(updated2, 0)
        self.assertEqual(skipped2, 1)

        sub = HomeworkSubmission.objects.get(homework=self.homework, student=self.student_profile)
        self.assertEqual(sub.score, Decimal('9.00'))
