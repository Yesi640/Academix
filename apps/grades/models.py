from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class EvaluationCriterion(models.Model):
    """
    Criterio o Componente de Evaluación para una asignatura en un grupo y periodo lectivo.
    Ejemplo: Exámenes (40.00%), Talleres (40.00%), Actitudinal (20.00%).
    La suma de los criterios dentro del periodo debe totalizar 100.00%.
    """
    course_section = models.ForeignKey(
        'courses.CourseSection',
        on_delete=models.CASCADE,
        related_name='evaluation_criteria',
        verbose_name='Curso / Sección'
    )
    subject = models.ForeignKey(
        'subjects.Subject',
        on_delete=models.CASCADE,
        related_name='evaluation_criteria',
        verbose_name='Asignatura'
    )
    academic_period = models.ForeignKey(
        'periods.AcademicPeriod',
        on_delete=models.CASCADE,
        related_name='evaluation_criteria',
        verbose_name='Periodo Lectivo'
    )
    name = models.CharField(max_length=100, verbose_name='Nombre del Criterio')
    topic = models.CharField(
        max_length=200,
        blank=True,
        default='',
        verbose_name='Tema / Contenido de la Actividad',
        help_text='Ej: Fracciones y decimales, Cuento corto, Revolución Industrial...'
    )
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01')), MaxValueValidator(Decimal('100.00'))],
        verbose_name='Ponderación Porcentual (%)'
    )
    order = models.PositiveSmallIntegerField(default=1, verbose_name='Orden en Planilla')
    norm = models.ForeignKey(
        'subjects.SubjectNorm',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='evaluation_criteria',
        verbose_name='RAP Curricular Asociado'
    )

    class Meta:
        verbose_name = 'Criterio de Evaluación'
        verbose_name_plural = 'Criterios de Evaluación'
        unique_together = ('course_section', 'subject', 'academic_period', 'name')
        ordering = ['order', 'id']

    def __str__(self):
        return f"{self.name} ({self.percentage}%) - {self.subject.code}"


class GradeRecord(models.Model):
    """
    Calificación individual de un estudiante en un criterio específico.
    Uso obligatorio de Decimal(4,2) en rango de 1.00 a 5.00 (cero floats).
    """
    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE,
        related_name='grade_records',
        verbose_name='Estudiante'
    )
    course_section = models.ForeignKey(
        'courses.CourseSection',
        on_delete=models.CASCADE,
        related_name='grade_records',
        verbose_name='Curso'
    )
    subject = models.ForeignKey(
        'subjects.Subject',
        on_delete=models.CASCADE,
        related_name='grade_records',
        verbose_name='Asignatura'
    )
    academic_period = models.ForeignKey(
        'periods.AcademicPeriod',
        on_delete=models.CASCADE,
        related_name='grade_records',
        verbose_name='Periodo'
    )
    criterion = models.ForeignKey(
        EvaluationCriterion,
        on_delete=models.CASCADE,
        related_name='records',
        verbose_name='Criterio de Evaluación'
    )
    score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('10.00'))],
        verbose_name='Calificación (0.00 - 10.00)'
    )

    feedback = models.TextField(blank=True, null=True, verbose_name='Retroalimentación Docente')
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_grades',
        verbose_name='Calificado por'
    )
    is_locked = models.BooleanField(
        default=False,
        verbose_name='¿Nota Bloqueada / Inmutable?'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Calificación'
        verbose_name_plural = 'Calificaciones'
        unique_together = ('student', 'course_section', 'subject', 'academic_period', 'criterion')
        ordering = ['student__user__last_name', 'criterion__order']

    def __str__(self):
        return f"{self.student.user.last_name} - {self.criterion.name}: {self.score}"


class PeriodFinalGrade(models.Model):
    """
    Nota definitiva consolidada para el periodo lectivo.
    Calculada automáticamente a partir de la sumatoria ponderada de GradeRecords.
    """
    class PerformanceLevel(models.TextChoices):
        BAJO = 'BAJO', 'Bajo'
        BASICO = 'BASICO', 'Básico'
        ALTO = 'ALTO', 'Alto'
        SUPERIOR = 'SUPERIOR', 'Superior'

    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE,
        related_name='period_final_grades',
        verbose_name='Estudiante'
    )
    course_section = models.ForeignKey(
        'courses.CourseSection',
        on_delete=models.CASCADE,
        related_name='period_final_grades',
        verbose_name='Curso'
    )
    subject = models.ForeignKey(
        'subjects.Subject',
        on_delete=models.CASCADE,
        related_name='period_final_grades',
        verbose_name='Asignatura'
    )
    academic_period = models.ForeignKey(
        'periods.AcademicPeriod',
        on_delete=models.CASCADE,
        related_name='period_final_grades',
        verbose_name='Periodo'
    )
    final_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        verbose_name='Nota Definitiva Ponderada'
    )
    performance_level = models.CharField(
        max_length=15,
        choices=PerformanceLevel.choices,
        default=PerformanceLevel.BASICO,
        verbose_name='Nivel de Desempeño'
    )
    is_approved = models.BooleanField(default=True, verbose_name='¿Aprobado?')
    recalculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Nota Definitiva de Periodo'
        verbose_name_plural = 'Notas Definitivas de Periodo'
        unique_together = ('student', 'course_section', 'subject', 'academic_period')
        ordering = ['student__user__last_name']

    def __str__(self):
        return f"{self.student.user.last_name}: {self.final_score} ({self.get_performance_level_display()})"

    @property
    def badge_class(self):
        mapping = {
            self.PerformanceLevel.BAJO: 'bg-danger text-white',
            self.PerformanceLevel.BASICO: 'bg-warning text-dark',
            self.PerformanceLevel.ALTO: 'bg-primary text-white',
            self.PerformanceLevel.SUPERIOR: 'bg-success text-white',
        }
        return mapping.get(self.performance_level, 'bg-secondary text-white')
