from django.urls import path
from . import views

app_name = 'grades'

urlpatterns = [
    path('', views.grades_index_view, name='index'),
    path('matrix/', views.grades_matrix_view, name='matrix'),
    path('update-inline/', views.update_score_inline_view, name='update_inline'),
    path('update-criterion-topic/', views.update_criterion_topic_view, name='update_criterion_topic'),
    path('update-criterion/', views.update_criterion_view, name='update_criterion'),
    path('configure-criteria/', views.configure_criteria_view, name='configure_criteria'),
]

