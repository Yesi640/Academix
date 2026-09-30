from decimal import Decimal
import uuid
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError, PermissionDenied
from .models import StudentFeeObligation, FeePayment, FeeConcept
from apps.audit.services import log_audit
from apps.audit.models import AuditLog


def get_student_financial_status(student_profile, academic_year=None):
    """
    Evalúa el estado de cuenta y cartera del estudiante.
    Retorna un diccionario estructurado indicando si tiene mora activa y el balance total adeudado.
    """
    qs = student_profile.obligaciones_financieras.all()
    if academic_year:
        qs = qs.filter(academic_year=academic_year)

    today = timezone.now().date()
    total_charged = Decimal('0.00')
    total_paid = Decimal('0.00')
    total_debt = Decimal('0.00')
    overdue_count = 0
    obligations_data = []

    for obl in qs:
        total_charged += obl.amount
        total_paid += obl.paid_amount
        balance = obl.balance
        
        # Verificar estado de mora
        is_overdue = (obl.status != StudentFeeObligation.Status.PAID and obl.status != StudentFeeObligation.Status.WAIVED and obl.due_date < today)
        if is_overdue and obl.status != StudentFeeObligation.Status.OVERDUE:
            obl.status = StudentFeeObligation.Status.OVERDUE
            obl.save(update_fields=['status', 'updated_at'])

        if balance > 0:
            total_debt += balance
            if is_overdue:
                overdue_count += 1

        obligations_data.append({
            'obligation': obl,
            'balance': balance,
            'is_overdue': is_overdue
        })

    is_in_debt = (total_debt > 0 and overdue_count > 0)

    return {
        'is_in_debt': is_in_debt,
        'is_paz_y_salvo': (total_debt == Decimal('0.00')),
        'total_charged': total_charged,
        'total_paid': total_paid,
        'total_debt': total_debt,
        'overdue_count': overdue_count,
        'obligations': obligations_data
    }


@transaction.atomic
def register_fee_payment(
    obligation_id,
    amount,
    payment_method,
    registered_by_user,
    receipt_number=None,
    payment_date=None,
    notes=None
):
    """
    Registra un pago sobre una obligación, actualiza su saldo y estado y genera trazabilidad inmutable.
    """
    obligation = StudentFeeObligation.objects.select_for_update().get(id=obligation_id)
    pay_amount = Decimal(str(amount))

    if pay_amount <= 0:
        raise ValidationError("El monto del pago debe ser mayor a cero.")

    if pay_amount > obligation.balance:
        raise ValidationError(f"El monto (${pay_amount:,.0f}) excede el saldo pendiente (${obligation.balance:,.0f}).")

    if not receipt_number:
        receipt_number = f"REC-{timezone.now().strftime('%Y%m')}-{uuid.uuid4().hex[:6].upper()}"

    payment = FeePayment.objects.create(
        obligation=obligation,
        amount=pay_amount,
        payment_date=payment_date or timezone.now().date(),
        payment_method=payment_method,
        receipt_number=receipt_number,
        registered_by=registered_by_user,
        notes=notes
    )

    obligation.paid_amount += pay_amount
    if obligation.paid_amount >= obligation.amount:
        obligation.status = StudentFeeObligation.Status.PAID
    elif obligation.paid_amount > 0:
        obligation.status = StudentFeeObligation.Status.PENDING
    obligation.save(update_fields=['paid_amount', 'status', 'updated_at'])

    log_audit(
        action=AuditLog.Action.CREATE,
        table_name='finance_feepayment',
        record_id=str(payment.id),
        new_values={
            'student_id': obligation.student.id,
            'receipt_number': receipt_number,
            'amount': str(pay_amount),
            'concept': obligation.concept.name
        },
        user=registered_by_user
    )
    return payment
