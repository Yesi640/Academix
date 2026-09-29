from django.contrib import admin
from .models import AcademicYear, GradeLevel, CourseSection, InstitutionSetting

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'name', 'status', 'is_current', 'start_date', 'end_date')
    list_filter = ('status', 'is_current')
    search_fields = ('name', 'year')

@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'level_stage', 'order')
    list_filter = ('level_stage',)
    ordering = ('order',)

@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade_level', 'academic_year', 'homeroom_teacher', 'capacity', 'is_active')
    list_filter = ('academic_year', 'grade_level', 'is_active')
    search_fields = ('name', 'classroom', 'homeroom_teacher__username')


@admin.register(InstitutionSetting)
class InstitutionSettingAdmin(admin.ModelAdmin):
    """
    Panel de administración de la configuración institucional.
    Permite personalizar el branding, colores, logo y terminología
    sin necesidad de modificar código.
    """
    fieldsets = (
        ('🏛️ Identidad de la Institución', {
            'fields': ('institution_type', 'school_scope', 'institution_name', 'slogan'),
        }),
        ('🎨 Branding e Identidad Visual', {
            'fields': ('logo', 'hero_image', 'primary_color', 'secondary_color'),
            'description': (
                'Personaliza los colores de la plataforma para tu institución. '
                'primary_color: color principal (ej. #7c3aed morado, #1b4332 verde, #1e3a8a azul). '
                'secondary_color: acento/pastel (ej. #c4b5fd, #b7e4c7, #bfdbfe).'
            ),
        }),
        ('📞 Datos de Contacto', {
            'fields': ('contact_email', 'contact_phone', 'website_url'),
            'classes': ('collapse',),
        }),
        ('📝 Terminología Institucional', {
            'fields': (
                'term_student', 'term_students',
                'term_teacher', 'term_teachers',
                'term_grade', 'term_section', 'term_sections',
                'term_subject', 'term_subjects',
                'term_director',
            ),
            'classes': ('collapse',),
            'description': 'Adapta el vocabulario de la plataforma (ej. "Aprendiz" en vez de "Estudiante" para SENA).',
        }),
    )

    def has_add_permission(self, request):
        # Solo puede existir UNA configuración institucional
        return not InstitutionSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False  # No permitir borrar la única config

    list_display = ('institution_name', 'institution_type', 'primary_color', 'secondary_color', 'updated_at')
    readonly_fields = ('updated_at',)
