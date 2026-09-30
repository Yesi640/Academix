from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.students_list_view, name='list'),
    path('enroll/', views.enroll_student_view, name='enroll'),
    path('create/', views.create_student_view, name='create'),
    path('<int:student_id>/expediente/', views.student_expediente_view, name='expediente'),
    path('<int:student_id>/expediente/upload/', views.upload_expediente_document_view, name='upload_expediente_document'),
    path('expediente/document/<int:document_id>/verify/', views.verify_expediente_document_view, name='verify_expediente_document'),
    path('expediente/document/<int:document_id>/download/', views.download_expediente_document_view, name='download_expediente_document'),
    path('<int:student_id>/observations/', views.student_observations_view, name='observations'),
    path('<int:student_id>/observations/create/', views.create_observation_view, name='create_observation'),
    path('bulk-upload/', views.bulk_upload_students_view, name='bulk_upload'),
    path('download-template/', views.download_student_template_csv, name='download_template'),
    path('enrollment/<int:enrollment_id>/confirm/', views.confirm_enrollment_view, name='confirm_enrollment'),
    path('enrollment/<int:enrollment_id>/cancel/', views.cancel_enrollment_view, name='cancel_enrollment'),
]


