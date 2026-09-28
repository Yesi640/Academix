from django.db import models
from django.conf import settings

class TeacherProfile(models.Model):
    """
    Ficha y perfil profesional de un docente institucional en ACADEMIX.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='teacher_profile',
        limit_choices_to={'role': 'TEACHER'},
        verbose_name='Usuario Institucional'
    )
    specialty = models.CharField(max_length=120, verbose_name='Especialidad o Titulación Principal')
    escalafon_grade = models.CharField(max_length=30, blank=True, null=True, verbose_name='Categoría / Escalafón')
    hire_date = models.DateField(blank=True, null=True, verbose_name='Fecha de Ingreso')

    class Meta:
        verbose_name = 'Perfil Docente'
        verbose_name_plural = 'Perfiles Docentes'
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"Prof. {self.user.get_full_name() or self.user.username} - {self.specialty}"


class TeachingAssignment(models.Model):
    """
    Asignación Académica: Vincula a un docente con una asignatura específica en un grupo escolar.
    Restricción estricta: Solo puede haber un docente asignado a la misma asignatura en el mismo grupo y año lectivo.
    """
    teacher = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name='assignments',
        verbose_name='Docente'
    )
    course_section = models.ForeignKey(
        'courses.CourseSection',
        on_delete=models.CASCADE,
        related_name='teacher_assignments',
        verbose_name='Curso / Sección'
    )
    subject = models.ForeignKey(
        'subjects.Subject',
        on_delete=models.CASCADE,
        related_name='teacher_assignments',
        verbose_name='Asignatura'
    )
    academic_year = models.ForeignKey(
        'courses.AcademicYear',
        on_delete=models.CASCADE,
        related_name='teacher_assignments',
        verbose_name='Año Lectivo'
    )
    is_active = models.BooleanField(default=True, verbose_name='¿Asignación Activa?')
    is_group_director = models.BooleanField(
        default=False,
        verbose_name='¿Director de Grupo?',
        help_text='Si está marcado, este docente es el director de grupo del curso y puede acceder a los boletines.'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Asignación Académica'
        verbose_name_plural = 'Asignaciones Académicas'
        unique_together = ('course_section', 'subject', 'academic_year')
        ordering = ['course_section__grade_level__order', 'course_section__name', 'subject__name']

    def __str__(self):
        return f"{self.teacher.user.last_name} -> {self.subject.name} ({self.course_section.name})"
