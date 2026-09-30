from django.urls import path
from . import views

app_name = 'finance'

urlpatterns = [
    path('dashboard/', views.finance_dashboard_view, name='dashboard'),
    path('student/<int:student_id>/statement/', views.student_account_statement_view, name='statement'),
    path('obligation/<int:obligation_id>/pay/', views.register_payment_view, name='pay_obligation'),
]
