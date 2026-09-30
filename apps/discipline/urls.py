from django.urls import path
from . import views

app_name = 'discipline'

urlpatterns = [
    path('student/<int:student_id>/', views.student_observer_view, name='observer'),
    path('student/<int:student_id>/create/', views.create_anotacion_view, name='create_anotacion'),
    path('anotacion/<int:record_id>/sign/', views.sign_anotacion_view, name='sign_anotacion'),
    path('anotacion/<int:record_id>/close/', views.close_anotacion_view, name='close_anotacion'),
]
