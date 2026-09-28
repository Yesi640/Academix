from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('academic-structure/', views.academic_structure_view, name='academic_structure'),
    path('years/create/', views.create_academic_year_view, name='create_academic_year'),
    path('years/<int:year_id>/set-active/', views.set_active_year_view, name='set_active_year'),
    path('years/<int:year_id>/generate-sections/', views.generate_default_sections_view, name='generate_default_sections'),
    path('sections/partial/', views.sections_partial, name='sections_partial'),
    path('sections/create/', views.create_section_view, name='create_section'),
    path('institution-settings/', views.institution_settings_view, name='institution_settings'),
]
