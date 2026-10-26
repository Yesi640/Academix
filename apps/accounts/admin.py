from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, School


@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'city', 'dane_code', 'is_active', 'created_at')
    list_filter = ('is_active', 'city')
    search_fields = ('name', 'code', 'dane_code', 'city')
    ordering = ('name',)


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = (
        'username',
        'document_number',
        'get_full_name_display',
        'role',
        'school',
        'email',
        'is_active',
        'is_staff'
    )
    list_filter = ('role', 'is_active', 'is_staff', 'document_type', 'school')
    search_fields = ('username', 'document_number', 'first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')

    @admin.display(description='Nombre Completo', ordering='last_name')
    def get_full_name_display(self, obj):
        return obj.get_full_name() or obj.username

    fieldsets = UserAdmin.fieldsets + (
        ('Datos Institucionales y Rol', {
            'fields': (
                'role',
                'school',
                'document_type',
                'document_number',
                'phone',
                'address',
                'avatar',
                'must_change_password'
            )
        }),
    )

    # Para add_fieldsets, no forzar campos de perfiles adicionales para no romper el formulario base de Django
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos Institucionales Básicos', {
            'fields': ('role', 'document_type', 'document_number', 'email')
        }),
    )
