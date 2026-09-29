from decimal import Decimal
from datetime import date
from django.test import TestCase
from django.core.exceptions import PermissionDenied, ValidationError
from apps.accounts.models import CustomUser
from apps.accounts.services import create_institutional_user
from apps.courses.models import AcademicYear, GradeLevel, CourseSection
from apps.subjects.models import KnowledgeArea, Subject
from apps.periods.models import AcademicPeriod
from apps.students.models import StudentProfile
from apps.students.services import get_or_create_student_profile, enroll_student_in_section
from .models import EvaluationCriterion, GradeRecord, PeriodFinalGrade
from .services import (
    get_or_create_default_criteria,
    calculate_period_final_grade,
    save_or_update_grade
)

class GradesTests(TestCase):
    def setUp(self):
        self.year = AcademicYear.objects.create(
            year=2026,
            name='Año 2026',
            start_date=date(2026, 1, 15),
            end_date=date(2026, 11, 30),
            status=AcademicYear.Status.ACTIVE,
            is_current=True
        )
        self.period = AcademicPeriod.objects.create(
            academic_year=self.year,
            number=1,
            name='Periodo 1',
            start_date=date(2026, 1, 15),
            end_date=date(2026, 4, 1),
            percentage=Decimal('25.00'),
            status=AcademicPeriod.Status.ACTIVE
        )
        self.grade = GradeLevel.objects.create(name='Sexto', code='06', order=6)
        self.section = CourseSection.objects.create(academic_year=self.year, grade_level=self.grade, name='6-A')
        self.area = KnowledgeArea.objects.create(name='Matemáticas', order=1)
        self.subject = Subject.objects.create(area=self.area, name='Matemáticas Fundamentales', code='MAT-01')

        self.student_user = create_institutional_user(
            username='estudiante_notas',
            email='notas@academix.edu.co',
            password='Password123*',
            role=CustomUser.Role.STUDENT
        )
        self.student_profile = get_or_create_student_profile(self.student_user, student_code='EST-GRADES-01')
        enroll_student_in_section(self.student_profile, self.section, self.year)

        self.criteria = get_or_create_default_criteria(self.section, self.subject, self.period)

    def test_default_criteria_sum_100_percent(self):
        total_percentage = sum(c.percentage for c in self.criteria)
        self.assertEqual(total_percentage, Decimal('100.00'))

    def test_grade_calculation_and_decimal_precision(self):
        # 5 Criterios de 20% cada uno (Evaluación 1 y 2, Taller 1 y 2, Actitudinal):
        # Criterio 0 (20%): 4.50 -> 0.90
        # Criterio 1 (20%): 4.50 -> 0.90
        # Criterio 2 (20%): 3.50 -> 0.70
        # Criterio 3 (20%): 3.50 -> 0.70
        # Criterio 4 (20%): 5.00 -> 1.00
        # Definitiva esperada = 0.90 + 0.90 + 0.70 + 0.70 + 1.00 = 4.20 (Desempeño ALTO)
        save_or_update_grade(self.student_profile, self.section, self.subject, self.period, self.criteria[0], '4.50')
        save_or_update_grade(self.student_profile, self.section, self.subject, self.period, self.criteria[1], '4.50')
        save_or_update_grade(self.student_profile, self.section, self.subject, self.period, self.criteria[2], '3.50')
        save_or_update_grade(self.student_profile, self.section, self.subject, self.period, self.criteria[3], '3.50')
        record, final_grade = save_or_update_grade(self.student_profile, self.section, self.subject, self.period, self.criteria[4], '5.00')

        self.assertEqual(final_grade.final_score, Decimal('4.20'))
        self.assertEqual(final_grade.performance_level, PeriodFinalGrade.PerformanceLevel.ALTO)
        self.assertTrue(final_grade.is_approved)

    def test_reprobation_bajo_performance(self):
        # 3 notas de 2.00 -> Definitiva 2.00 (BAJO, no aprobado)
        for c in self.criteria:
            save_or_update_grade(self.student_profile, self.section, self.subject, self.period, c, '2.00')

        final_grade = PeriodFinalGrade.objects.get(
            student=self.student_profile,
            course_section=self.section,
            subject=self.subject,
            academic_period=self.period
        )
        self.assertEqual(final_grade.final_score, Decimal('2.00'))
        self.assertEqual(final_grade.performance_level, PeriodFinalGrade.PerformanceLevel.BAJO)
        self.assertFalse(final_grade.is_approved)

    def test_score_range_validation(self):
        with self.assertRaises(ValidationError):
            save_or_update_grade(self.student_profile, self.section, self.subject, self.period, self.criteria[0], '10.50')

    def test_closed_period_blocks_grading(self):
        self.period.status = AcademicPeriod.Status.CLOSED
        self.period.save()

        with self.assertRaises(PermissionDenied):
            save_or_update_grade(self.student_profile, self.section, self.subject, self.period, self.criteria[0], '4.00')
