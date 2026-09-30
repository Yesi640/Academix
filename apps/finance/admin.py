from django.contrib import admin
from .models import FeeConcept, StudentFeeObligation, FeePayment


@admin.register(FeeConcept)
class FeeConceptAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'recurrence', 'default_amount', 'is_active')
    search_fields = ('name', 'code')


@admin.register(StudentFeeObligation)
class StudentFeeObligationAdmin(admin.ModelAdmin):
    list_display = ('student', 'concept', 'month', 'amount', 'paid_amount', 'status', 'due_date')
    list_filter = ('status', 'academic_year', 'concept')
    search_fields = ('student__user__first_name', 'student__user__last_name', 'student__student_code')


@admin.register(FeePayment)
class FeePaymentAdmin(admin.ModelAdmin):
    list_display = ('receipt_number', 'obligation', 'amount', 'payment_date', 'payment_method', 'registered_by')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('receipt_number', 'obligation__student__user__first_name', 'obligation__student__user__last_name')
