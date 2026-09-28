from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('', views.teachers_list_view, name='list'),
    path('my-courses/', views.teacher_courses_view, name='my_courses'),
    path('course/<int:section_id>/', views.course_workspace_view, name='course_workspace'),
    path('subject/<int:subject_id>/norm/add/', views.add_subject_norm_view, name='add_norm'),
    path('assign/', views.assign_teacher_view, name='assign'),
    path('create/', views.create_teacher_view, name='create'),
    path('api/section/<int:section_id>/subjects/', views.api_subjects_for_section, name='api_subjects_for_section'),
]

