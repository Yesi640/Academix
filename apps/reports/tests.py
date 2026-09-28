from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import CustomUser
from apps.courses.models import AcademicYear, GradeLevel, CourseSection
from apps.subjects.models import KnowledgeArea, Subject
from apps.periods.models import AcademicPeriod
from apps.teachers.models import TeacherProfile, TeachingAssignment
from apps.students.models import StudentProfile, Enrollment
from apps.grades.models import EvaluationCriterion, GradeRecord, PeriodFinalGrade
from apps.attendance.models import AttendanceSession, AttendanceRecord
from apps.reports.services import (
    build_student_bulletin_data,
    calculate_section_ranking,
    build_section_consolidated_data,
    export_consolidated_csv,
    build_honor_roll_data
)

class ReportsAndBulletinsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin = CustomUser.objects.create_superuser('admin_rep', 'admin@test.com', 'Pass123*')
        self.docente_user = CustomUser.objects.create_user('doc_rep', 'doc@test.com', 'Pass123*', role=CustomUser.Role.TEACHER)
        self.docente = TeacherProfile.objects.create(user=self.docente_user, specialty='Matemáticas')

        self.student_user1 = CustomUser.objects.create_user('est_rep1', 'est1@test.com', 'Pass123*', role=CustomUser.Role.STUDENT, first_name='Carlos', last_name='Alvarez')
        self.student1 = StudentProfile.objects.create(user=self.student_user1, student_code='EST-001')

        self.student_user2 = CustomUser.objects.create_user('est_rep2', 'est2@test.com', 'Pass123*', role=CustomUser.Role.STUDENT, first_name='Beatriz', last_name='Castro')
        self.student2 = StudentProfile.objects.create(user=self.student_user2, student_code='EST-002')

        self.year = AcademicYear.objects.create(
            year=2026,
            name='Año 2026',
            start_date='2026-02-01',
            end_date='2026-11-30',
            status=AcademicYear.Status.ACTIVE,
            is_current=True
        )

        self.grade = GradeLevel.objects.create(name='Sexto', code='6')
        self.section = CourseSection.objects.create(academic_year=self.year, grade_level=self.grade, name='6-A')

        self.enr1 = Enrollment.objects.create(student=self.student1, course_section=self.section, academic_year=self.year, status=Enrollment.Status.ACTIVE)
        self.enr2 = Enrollment.objects.create(student=self.student2, course_section=self.section, academic_year=self.year, status=Enrollment.Status.ACTIVE)

        self.period = AcademicPeriod.objects.create(
            academic_year=self.year,
            number=1,
            name='Periodo 1',
            start_date='2026-02-01',
            end_date='2026-04-30',
            percentage=Decimal('25.00'),
            status=AcademicPeriod.Status.ACTIVE
        )

        self.area = KnowledgeArea.objects.create(name='Matemáticas')
        self.subject = Subject.objects.create(name='Matemáticas Básicas', code='MAT-01', area=self.area)
        self.assignment = TeachingAssignment.objects.create(
            teacher=self.docente,
            course_section=self.section,
            subject=self.subject,
            academic_year=self.year,
            is_active=True
        )

        # Calificaciones: Student1 = 4.80 (Superior), Student2 = 2.50 (Bajo)
        PeriodFinalGrade.objects.create(
            student=self.student1,
            course_section=self.section,
            subject=self.subject,
            academic_period=self.period,
            final_score=Decimal('4.80'),
            performance_level=PeriodFinalGrade.PerformanceLevel.SUPERIOR,
            is_approved=True
        )
        PeriodFinalGrade.objects.create(
            student=self.student2,
            course_section=self.section,
            subject=self.subject,
            academic_period=self.period,
            final_score=Decimal('2.50'),
            performance_level=PeriodFinalGrade.PerformanceLevel.BAJO,
            is_approved=False
        )

    def test_ranking_and_bulletin_data(self):
        """Prueba cálculo de ranking y construcción del boletín."""
        ranking = calculate_section_ranking(self.section, self.period)
        self.assertEqual(ranking[self.student1.id]['rank'], 1)
        self.assertEqual(ranking[self.student2.id]['rank'], 2)

        bulletin = build_student_bulletin_data(self.student1, self.section, self.period)
        self.assertEqual(bulletin['student_rank'], 1)
        self.assertEqual(bulletin['period_average'], Decimal('4.80'))
        self.assertEqual(bulletin['total_failed_count'], 0)
        self.assertEqual(len(bulletin['bulletin_areas']), 1)

    def test_consolidated_and_csv_export(self):
        """Prueba sábana consolidada y exportación CSV."""
        cons = build_section_consolidated_data(self.section, self.period)
        self.assertEqual(cons['total_students'], 2)
        self.assertEqual(cons['rows'][0]['student'], self.student1)
        self.assertEqual(cons['rows'][1]['student'], self.student2)

        csv_text = export_consolidated_csv(self.section, self.period)
        self.assertTrue(csv_text.startswith('\ufeff'))
        self.assertIn("Puesto,Código Estudiantil", csv_text)
        self.assertIn("EST-001", csv_text)
        self.assertIn("4.80", csv_text)

    def test_honor_roll_data(self):
        """Prueba Cuadro de Honor con el mejor promedio."""
        hr = build_honor_roll_data(self.section, self.period)
        self.assertEqual(len(hr['honor_students']), 1)
        self.assertEqual(hr['honor_students'][0]['student'], self.student1)
        self.assertEqual(hr['passed_all_count'], 1)
        self.assertEqual(hr['approval_rate'], Decimal('50.0'))

    def test_student_forbidden_to_view_other_bulletin(self):
        """Prueba que un estudiante no pueda visualizar el boletín de otro compañero."""
        self.client.force_login(self.student_user1)
        # Intentar acceder al boletín del student2
        url = reverse('reports:student_bulletin', kwargs={'student_id': self.student2.id, 'period_id': self.period.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 403)

    def test_sabana_access_permissions(self):
        """Prueba permisos de acceso a la sábana de notas consolidada."""
        # 1. Estudiante no puede acceder a la sábana
        self.client.force_login(self.student_user1)
        res_est = self.client.get(reverse('reports:consolidated'))
        self.assertEqual(res_est.status_code, 302)  # Redirige a dashboard

        # 2. Docente normal (NO director de grupo) no puede acceder
        self.client.force_login(self.docente_user)
        res_doc = self.client.get(reverse('reports:consolidated'))
        self.assertEqual(res_doc.status_code, 302)

        # 3. Docente cuando es asignado como Director de Grupo de la sección 6-A
        self.assignment.is_group_director = True
        self.assignment.save()
        res_director = self.client.get(reverse('reports:consolidated'), {
            'section_id': self.section.id,
            'period_id': self.period.id
        })
        self.assertEqual(res_director.status_code, 200)

        # 4. Secretaría puede ver la sábana
        sec_user = CustomUser.objects.create_user('sec_test', 'sec@test.com', 'Pass123*', role=CustomUser.Role.SECRETARIA)
        self.client.force_login(sec_user)
        res_sec = self.client.get(reverse('reports:consolidated'), {
            'section_id': self.section.id,
            'period_id': self.period.id
        })
        self.assertEqual(res_sec.status_code, 200)

        # 5. Rector puede ver la sábana
        rec_user = CustomUser.objects.create_user('rec_test', 'rec@test.com', 'Pass123*', role=CustomUser.Role.RECTOR)
        self.client.force_login(rec_user)
        res_rec = self.client.get(reverse('reports:consolidated'), {
            'section_id': self.section.id,
            'period_id': self.period.id
        })
        self.assertEqual(res_rec.status_code, 200)

    def test_honor_roll_disabled_redirects(self):
        """Prueba que la vista de Cuadro de Honor redirige al índice al haber sido deshabilitada."""
        self.client.force_login(self.admin)
        res = self.client.get(reverse('reports:honor_roll'))
        self.assertRedirects(res, reverse('reports:index'))
