from decimal import Decimal
from datetime import date, timedelta
from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import CustomUser
from apps.accounts.services import create_institutional_user
from apps.courses.models import AcademicYear, GradeLevel, CourseSection
from apps.students.models import StudentProfile
from apps.students.services import get_or_create_student_profile
from .models import FeeConcept, StudentFeeObligation, FeePayment
from .services import get_student_financial_status, register_fee_payment


class FinanceModuleTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.year = AcademicYear.objects.create(
            year=2026, name='Año 2026', start_date=date(2026, 1, 15), end_date=date(2026, 11, 30),
            status=AcademicYear.Status.ACTIVE, is_current=True
        )
        self.secretaria = create_institutional_user(
            username='tesorera_ana', email='ana@academix.edu.co', password='Password123*',
            role=CustomUser.Role.SECRETARIA
        )
        self.padre = create_institutional_user(
            username='padre_juan', email='juan@academix.edu.co', password='Password123*',
            role=CustomUser.Role.PARENT
        )
        self.estudiante_user = create_institutional_user(
            username='estudiante_pedro', email='pedro@academix.edu.co', password='Password123*',
            role=CustomUser.Role.STUDENT
        )
        self.estudiante = get_or_create_student_profile(self.estudiante_user, student_code='EST-PEDRO', parent=self.padre)

        self.concept_pension = FeeConcept.objects.create(
            name='Pensión Mensual', code='PENSION-REG', recurrence=FeeConcept.Recurrence.MONTHLY,
            default_amount=Decimal('350000.00')
        )

    def test_fee_obligation_and_payment_flow(self):
        # Crear cuota
        obl = StudentFeeObligation.objects.create(
            student=self.estudiante,
            academic_year=self.year,
            concept=self.concept_pension,
            month=2,
            due_date=date(2026, 2, 10),
            amount=Decimal('350000.00')
        )
        self.assertEqual(obl.balance, Decimal('350000.00'))

        # Registrar abono parcial de 200,000
        p1 = register_fee_payment(
            obligation_id=obl.id,
            amount=Decimal('200000.00'),
            payment_method=FeePayment.PaymentMethod.CASH,
            registered_by_user=self.secretaria
        )
        obl.refresh_from_db()
        self.assertEqual(obl.paid_amount, Decimal('200000.00'))
        self.assertEqual(obl.balance, Decimal('150000.00'))
        self.assertEqual(obl.status, StudentFeeObligation.Status.PENDING)

        # Saldar el restante 150,000
        p2 = register_fee_payment(
            obligation_id=obl.id,
            amount=Decimal('150000.00'),
            payment_method=FeePayment.PaymentMethod.TRANSFER,
            registered_by_user=self.secretaria
        )
        obl.refresh_from_db()
        self.assertEqual(obl.paid_amount, Decimal('350000.00'))
        self.assertEqual(obl.balance, Decimal('0.00'))
        self.assertEqual(obl.status, StudentFeeObligation.Status.PAID)

    def test_financial_status_calculation(self):
        # Cuota vencida
        StudentFeeObligation.objects.create(
            student=self.estudiante,
            academic_year=self.year,
            concept=self.concept_pension,
            month=1,
            due_date=date.today() - timedelta(days=5),
            amount=Decimal('350000.00')
        )

        status = get_student_financial_status(self.estudiante, self.year)
        self.assertTrue(status['is_in_debt'])
        self.assertFalse(status['is_paz_y_salvo'])
        self.assertEqual(status['total_debt'], Decimal('350000.00'))
        self.assertEqual(status['overdue_count'], 1)
