from django.contrib import admin
from .models import TeacherProfile, TeachingAssignment

@admin.register(TeacherProfile)
class TeacherProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'specialty', 'escalafon_grade', 'hire_date')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'specialty')

@admin.register(TeachingAssignment)
class TeachingAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'subject', 'course_section', 'academic_year', 'is_active', 'is_group_director')
    list_filter = ('academic_year', 'is_active', 'is_group_director', 'course_section__grade_level')
    list_editable = ('is_active', 'is_group_director')
    search_fields = ('teacher__user__username', 'subject__name', 'course_section__name')
