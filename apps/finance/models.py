from decimal import Decimal
from django.db import models
from django.utils import timezone
from apps.accounts.models import CustomUser
from apps.students.models import StudentProfile
from apps.courses.models import AcademicYear, GradeLevel


class FeeConcept(models.Model):
    """
    Conceptos de cobro institucional (Pensión, Matrícula, Sistematización, Seguro, etc.)
    """
    class Recurrence(models.TextChoices):
        MONTHLY = 'MONTHLY', 'Mensual (Pensión recurrente)'
        ANNUAL = 'ANNUAL', 'Anual (Matrícula / Seguro)'
        ONE_TIME = 'ONE_TIME', 'Única Vez / Eventual'

    name = models.CharField(max_length=150, verbose_name='Nombre del Concepto')
    code = models.CharField(max_length=30, unique=True, verbose_name='Código')
    recurrence = models.CharField(max_length=20, choices=Recurrence.choices, default=Recurrence.MONTHLY)
    default_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Valor Predeterminado')
    is_active = models.BooleanField(default=True, verbose_name='Activo')

    class Meta:
        verbose_name = 'Concepto de Cobro'
        verbose_name_plural = 'Conceptos de Cobro'
        ordering = ['name']

    def __str__(self):
        return f"{self.name} (${self.default_amount:,.0f})"


class StudentFeeObligation(models.Model):
    """
    Obligación o factura individual asociada a un estudiante y año escolar.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pendiente de Pago'
        PAID = 'PAID', 'Pagada / Paz y Salvo'
        OVERDUE = 'OVERDUE', 'Vencida / En Mora'
        WAIVED = 'WAIVED', 'Exonerada / Beca'

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='obligaciones_financieras',
        verbose_name='Estudiante'
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name='obligaciones_financieras',
        verbose_name='Año Lectivo'
    )
    concept = models.ForeignKey(
        FeeConcept,
        on_delete=models.PROTECT,
        related_name='obligaciones',
        verbose_name='Concepto de Cobro'
    )
    month = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        verbose_name='Mes correspondiente (1-12)'
    )
    due_date = models.DateField(verbose_name='Fecha Límite de Pago')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto a Pagar')
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Monto Abonado')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, verbose_name='Estado')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Obligación Financiera'
        verbose_name_plural = 'Obligaciones Financieras'
        ordering = ['due_date', 'student__user__last_name']
        unique_together = ('student', 'academic_year', 'concept', 'month')

    def __str__(self):
        return f"{self.student.user.get_full_name()} - {self.concept.name} (Mes {self.month or 'N/A'}) - {self.get_status_display()}"

    @property
    def balance(self):
        return max(Decimal('0.00'), self.amount - self.paid_amount)

    @property
    def is_overdue(self):
        if self.status in [self.Status.PAID, self.Status.WAIVED]:
            return False
        return self.due_date < timezone.now().date()


class FeePayment(models.Model):
    """
    Registro individual de recaudo/pago de pensión o matrícula.
    """
    class PaymentMethod(models.TextChoices):
        CASH = 'CASH', 'Efectivo / Caja'
        TRANSFER = 'TRANSFER', 'Transferencia Bancaria'
        CARD = 'CARD', 'Tarjeta Débito / Crédito'
        PSE = 'PSE', 'Pasarela Online / PSE'

    obligation = models.ForeignKey(
        StudentFeeObligation,
        on_delete=models.CASCADE,
        related_name='pagos',
        verbose_name='Obligación Pagada'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Monto Recaudado')
    payment_date = models.DateField(default=timezone.now, verbose_name='Fecha de Pago')
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH, verbose_name='Medio de Pago')
    receipt_number = models.CharField(max_length=50, unique=True, verbose_name='Número de Recibo / Factura')
    registered_by = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='pagos_registrados',
        verbose_name='Secretaría / Cajero'
    )
    notes = models.CharField(max_length=250, blank=True, null=True, verbose_name='Observaciones')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Recibo de Pago'
        verbose_name_plural = 'Recibos de Pago'
        ordering = ['-payment_date', '-created_at']

    def __str__(self):
        return f"Recibo #{self.receipt_number} - ${self.amount:,.0f} ({self.obligation.student.user.get_full_name()})"
