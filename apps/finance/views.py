from decimal import Decimal
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, ValidationError
from django.contrib import messages
from apps.students.models import StudentProfile
from apps.courses.models import AcademicYear, CourseSection
from apps.courses.services import get_current_academic_year
from .models import StudentFeeObligation, FeePayment, FeeConcept
from .services import get_student_financial_status, register_fee_payment


@login_required
def student_account_statement_view(request, student_id):
    """
    Estado de cuenta y estado de cartera de pensiones del estudiante.
    """
    user = request.user
    student = get_object_or_404(StudentProfile.objects.select_related('user', 'parent'), id=student_id)
    current_year = get_current_academic_year()

    # Validar permisos
    is_staff = user.is_superuser or user.is_admin_role or user.is_rector or user.is_secretary
    is_parent = (user.is_parent and student.parent == user)
    is_student_self = (user.is_student and student.user == user)

    if not (is_staff or is_parent or is_student_self):
        raise PermissionDenied("No tienes autorización para consultar el estado financiero de este estudiante.")

    status_data = get_student_financial_status(student, current_year)
    payment_methods = FeePayment.PaymentMethod.choices

    context = {
        'student': student,
        'current_year': current_year,
        'status_data': status_data,
        'is_staff': is_staff,
        'payment_methods': payment_methods,
    }
    return render(request, 'finance/statement.html', context)


@login_required
def register_payment_view(request, obligation_id):
    """
    Registra el recaudo de una cuota de pensión o matrícula.
    """
    user = request.user
    if not (user.is_superuser or user.is_admin_role or user.is_rector or user.is_secretary):
        raise PermissionDenied("Solo el personal de Secretaría y Tesorería puede registrar recaudos.")

    obligation = get_object_or_404(StudentFeeObligation.objects.select_related('student'), id=obligation_id)

    if request.method == 'POST':
        amount = request.POST.get('amount', '0')
        payment_method = request.POST.get('payment_method', FeePayment.PaymentMethod.CASH)
        notes = request.POST.get('notes', '').strip()

        try:
            payment = register_fee_payment(
                obligation_id=obligation.id,
                amount=amount,
                payment_method=payment_method,
                registered_by_user=user,
                notes=notes
            )
            messages.success(request, f'Pago registrado exitosamente. Recibo #{payment.receipt_number} por ${payment.amount:,.0f}')
        except Exception as e:
            messages.error(request, f'Error al procesar el pago: {str(e)}')

    return redirect('finance:statement', student_id=obligation.student.id)


@login_required
def finance_dashboard_view(request):
    """
    Panel general de Cartera y Tesorería para Secretaría y Administración.
    """
    user = request.user
    if not (user.is_superuser or user.is_admin_role or user.is_rector or user.is_secretary):
        raise PermissionDenied("Acceso exclusivo para Secretaría y Directivas.")

    current_year = get_current_academic_year()
    obligations = StudentFeeObligation.objects.filter(academic_year=current_year).select_related('student__user', 'concept') if current_year else []

    total_charged = sum(o.amount for o in obligations)
    total_paid = sum(o.paid_amount for o in obligations)
    total_pending = total_charged - total_paid

    recent_payments = FeePayment.objects.filter(obligation__academic_year=current_year).select_related('obligation__student__user', 'obligation__concept', 'registered_by')[:20] if current_year else []

    context = {
        'current_year': current_year,
        'total_charged': total_charged,
        'total_paid': total_paid,
        'total_pending': total_pending,
        'recent_payments': recent_payments,
        'obligations': obligations[:50],
    }
    return render(request, 'finance/dashboard.html', context)
