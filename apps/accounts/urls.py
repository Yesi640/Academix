from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('switch-model/', views.switch_institution_model_view, name='switch_model'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('change-password/', views.change_password_view, name='change_password'),
    # Tema Global del Sistema (control exclusivo del Rector)
    path('theme/global/save/', views.rector_save_global_theme, name='rector_save_global_theme'),
    path('theme/global/', views.get_global_theme_api, name='get_global_theme'),
]
