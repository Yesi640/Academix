from django.urls import path
from . import views

app_name = 'reports'

urlpatterns = [
    path('', views.reports_index_view, name='index'),
    path('bulletin/<int:student_id>/<int:period_id>/', views.student_bulletin_view, name='student_bulletin'),
    path('bulletin/<int:student_id>/<int:period_id>/pdf/', views.download_student_bulletin_pdf_view, name='download_student_bulletin_pdf'),
    path('verify/<str:token>/', views.verify_bulletin_view, name='verify_bulletin'),
    path('bulletins/bulk/<int:section_id>/<int:period_id>/', views.section_bulletins_bulk_view, name='section_bulletins_bulk'),
    path('consolidated/', views.section_consolidated_view, name='consolidated'),
    path('consolidated/export/<int:section_id>/<int:period_id>/', views.export_consolidated_csv_view, name='export_consolidated_csv'),
    path('honor-roll/', views.honor_roll_view, name='honor_roll'),
]
