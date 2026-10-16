from django.urls import path
from . import views

app_name = 'alerts'

urlpatterns = [
    path('active/', views.active_alerts_partial, name='active_partial'),
    path('dismiss/<int:alert_id>/', views.dismiss_alert, name='dismiss'),
    path('activities/', views.activities_list_view, name='activities'),
    path('management/', views.alerts_management_view, name='management'),
]

