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
    path('users/', views.users_management_view, name='users_list'),
    path('change-password/', views.change_password_view, name='change_password'),
    # Tema Global del Sistema (control exclusivo del Rector)
    path('theme/global/save/', views.rector_save_global_theme, name='rector_save_global_theme'),
    path('theme/global/', views.get_global_theme_api, name='get_global_theme'),
    # ── Recuperación de Contraseña ──
    path('password-reset/', views.password_reset_request_view, name='password_reset'),
    path('password-reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    path('password-reset/complete/', views.password_reset_complete_view, name='password_reset_complete'),
    # ── Gestión de Escuelas (Administrador de la Plataforma) ──
    path('schools/', views.schools_list_view, name='schools_list'),
    path('schools/new/', views.school_create_edit_view, name='school_create'),
    path('schools/<int:school_id>/edit/', views.school_create_edit_view, name='school_edit'),
    path('schools/<int:school_id>/toggle/', views.school_toggle_active_view, name='school_toggle'),
    path('api/schools/', views.school_api_list, name='schools_api'),
]
