from django.db import models
from django.utils import timezone
from apps.accounts.models import CustomUser
from apps.students.models import StudentProfile
from apps.courses.models import AcademicYear
from apps.periods.models import AcademicPeriod


class AnotacionDisciplinaria(models.Model):
    """
    Registro inmutable y verificable del Observador del Estudiante
    conforme a la Ley 1620 de Convivencia Escolar y el Manual de Convivencia.
    """
    class FaultType(models.TextChoices):
        TIPO_I = 'TIPO_I', 'Situación Tipo I (Falta Leve / Formativa)'
        TIPO_II = 'TIPO_II', 'Situación Tipo II (Falta Grave / Afectación Convivencial)'
        TIPO_III = 'TIPO_III', 'Situación Tipo III (Falta Gravísima / Delito o Violencia)'
        POSITIVA = 'POSITIVA', 'Reconocimiento Convivencial (Mérito / Felicitación)'

    class Status(models.TextChoices):
        ABIERTA = 'ABIERTA', 'Abierta (Pendiente de descargos o firma)'
        SEGUIMIENTO = 'SEGUIMIENTO', 'En Seguimiento Pedagógico'
        CERRADA = 'CERRADA', 'Cerrada (Compromisos cumplidos)'
        ANULADA = 'ANULADA', 'Anulada'

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='anotaciones_disciplinarias',
        verbose_name='Estudiante'
    )
    author = models.ForeignKey(
        CustomUser,
        on_delete=models.PROTECT,
        related_name='anotaciones_creadas',
        verbose_name='Docente / Directivo que registra'
    )
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.CASCADE,
        related_name='anotaciones_disciplinarias',
        verbose_name='Año Lectivo'
    )
    period = models.ForeignKey(
        AcademicPeriod,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='anotaciones_disciplinarias',
        verbose_name='Periodo Lectivo'
    )

    fault_type = models.CharField(
        max_length=20,
        choices=FaultType.choices,
        default=FaultType.TIPO_I,
        verbose_name='Tipificación de la Situación'
    )
    date = models.DateField(
        default=timezone.now,
        verbose_name='Fecha de los Hechos'
    )
    time = models.TimeField(
        null=True,
        blank=True,
        verbose_name='Hora aproximada'
    )
    location = models.CharField(
        max_length=150,
        default='Aula de Clase',
        verbose_name='Lugar / Contexto de los hechos'
    )
    title = models.CharField(
        max_length=200,
        verbose_name='Título o Resumen de la Situación'
    )
    description = models.TextField(
        verbose_name='Descripción Detallada de los Hechos'
    )

    # Debido Proceso y Descargos del Estudiante (Ley 1620)
    student_disclaimer = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descargos / Versión del Estudiante'
    )
    pedagogical_commitment = models.TextField(
        blank=True,
        null=True,
        verbose_name='Acción Restaurativa y Compromiso Pedagógico'
    )

    # Notificación y Conformidad del Acudiente / Familia
    parent_notified = models.BooleanField(
        default=False,
        verbose_name='Notificado al Acudiente'
    )
    parent_acknowledged_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha y Hora de Firma del Acudiente'
    )
    parent_signature_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='Nombre de quien firma como Acudiente'
    )
    parent_comments = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones o Compromiso del Acudiente'
    )

    # Cierre de la situación
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ABIERTA,
        verbose_name='Estado de la Anotación'
    )
    closed_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de Cierre'
    )
    closed_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='anotaciones_cerradas',
        verbose_name='Cerrada por'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Creación')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Modificación')

    class Meta:
        verbose_name = 'Anotación del Observador'
        verbose_name_plural = 'Anotaciones del Observador'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.get_fault_type_display()} - {self.student.user.get_full_name()} ({self.date})"

    @property
    def badge_class(self):
        if self.fault_type == self.FaultType.POSITIVA:
            return 'bg-success text-white'
        elif self.fault_type == self.FaultType.TIPO_I:
            return 'bg-warning text-dark'
        elif self.fault_type == self.FaultType.TIPO_II:
            return 'bg-orange text-white'
        elif self.fault_type == self.FaultType.TIPO_III:
            return 'bg-danger text-white'
        return 'bg-secondary text-white'

    @property
    def is_signed_by_parent(self):
        return bool(self.parent_acknowledged_at)
