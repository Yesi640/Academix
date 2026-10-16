"""
URL configuration for ACADEMIX project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from apps.accounts.views import dashboard_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False), name='root_redirect'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('accounts/', include('apps.accounts.urls', namespace='accounts')),
    path('audit/', include('apps.audit.urls', namespace='audit')),
    path('alerts/', include('apps.alerts.urls', namespace='alerts')),
    # Módulos del Sprint 2
    path('courses/', include('apps.courses.urls', namespace='courses')),
    path('subjects/', include('apps.subjects.urls', namespace='subjects')),
    path('periods/', include('apps.periods.urls', namespace='periods')),
    path('teachers/', include('apps.teachers.urls', namespace='teachers')),
    path('students/', include('apps.students.urls', namespace='students')),
    # Módulo del Sprint 3
    path('attendance/', include('apps.attendance.urls', namespace='attendance')),
    # Módulos del Sprint 4
    path('grades/', include('apps.grades.urls', namespace='grades')),
    path('homework/', include('apps.homework.urls', namespace='homework')),
    # Módulos del Sprint 5
    path('rules/', include('apps.rules.urls', namespace='rules')),
    path('reports/', include('apps.reports.urls', namespace='reports')),
    path('discipline/', include('apps.discipline.urls', namespace='discipline')),
    path('finance/', include('apps.finance.urls', namespace='finance')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
