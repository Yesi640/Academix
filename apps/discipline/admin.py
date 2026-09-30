from django.contrib import admin
from .models import AnotacionDisciplinaria


@admin.register(AnotacionDisciplinaria)
class AnotacionDisciplinariaAdmin(admin.ModelAdmin):
    list_display = ('title', 'student', 'fault_type', 'date', 'author', 'status', 'parent_notified', 'is_signed_by_parent')
    list_filter = ('fault_type', 'status', 'parent_notified', 'academic_year')
    search_fields = ('title', 'description', 'student__user__first_name', 'student__user__last_name', 'student__student_code')
    date_hierarchy = 'date'
    ordering = ('-date', '-created_at')
