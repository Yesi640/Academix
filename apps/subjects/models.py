from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class KnowledgeArea(models.Model):
    """
    Área Fundamental u Optativa de Conocimiento (ej. Matemáticas, Ciencias Naturales, TIC, Idiomas).
    """
    institution_type = models.CharField(
        max_length=20,
        default='COLEGIO',
        db_index=True,
        verbose_name='Tipo de Institución'
    )
    name = models.CharField(max_length=100, verbose_name='Nombre del Área')
    order = models.PositiveSmallIntegerField(default=1, verbose_name='Orden en Boletines')

    class Meta:
        verbose_name = 'Área de Conocimiento'
        verbose_name_plural = 'Áreas de Conocimiento'
        unique_together = ('institution_type', 'name')
        ordering = ['institution_type', 'order', 'name']

    def __str__(self):
        return f"{self.name} ({self.institution_type})"


class Subject(models.Model):
    """
    Asignatura, Materia, Competencia o Módulo individual según el tipo de institución.
    """
    institution_type = models.CharField(
        max_length=20,
        default='COLEGIO',
        db_index=True,
        verbose_name='Tipo de Institución'
    )
    area = models.ForeignKey(
        KnowledgeArea,
        on_delete=models.PROTECT,
        related_name='subjects',
        verbose_name='Área Fundamental'
    )
    class Category(models.TextChoices):
        PRINCIPAL   = 'PRINCIPAL',   'Materia Principal'
        HUMANISTICA = 'HUMANISTICA', 'Materia Humanística'
        HISTORIA    = 'HISTORIA',    'Historia y Ciencias Sociales'
        ARTE        = 'ARTE',        'Arte y Cultura'
        DEPORTE     = 'DEPORTE',     'Deporte y Educación Física'

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.PRINCIPAL,
        verbose_name='Agrupación / Categoría'
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name='¿Es la asignatura principal de su categoría?',
        help_text='Marca la asignatura representativa de este grupo (Historia, Arte o Deporte).'
    )
    credits = models.PositiveSmallIntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        verbose_name='Créditos Académicos (Superior)'
    )
    name = models.CharField(max_length=120, verbose_name='Nombre de la Asignatura / Módulo')
    code = models.CharField(max_length=30, verbose_name='Código Abreviado')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción Curricular')

    class Meta:
        verbose_name = 'Asignatura / Módulo'
        verbose_name_plural = 'Asignaturas / Módulos'
        unique_together = ('institution_type', 'code')
        ordering = ['institution_type', 'category', 'area', 'name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class SubjectNorm(models.Model):
    """
    Norma, Estándar de Calidad o Competencia asociada a una Asignatura / Módulo.
    Permite parametrizar estándares MEN, competencias laborales SENA o competencias de curso.
    """
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='norms',
        verbose_name='Asignatura / Módulo'
    )
    code = models.CharField(max_length=50, verbose_name='Código de Norma / RAP')
    title = models.CharField(max_length=200, verbose_name='Título del RAP / Competencia')
    description = models.TextField(blank=True, default='', verbose_name='Descripción de la Competencia / Estándar')
    competency = models.CharField(max_length=255, blank=True, default='', verbose_name='Competencia General')
    domain = models.CharField(max_length=150, blank=True, default='', verbose_name='Dominio')
    dimension = models.CharField(max_length=150, blank=True, default='', verbose_name='Dimensión')
    indicator = models.TextField(blank=True, default='', verbose_name='Indicador de Logro / Desempeño')
    saber = models.TextField(blank=True, default='', verbose_name='Saber (Cognitivo / Conceptual)')
    hacer = models.TextField(blank=True, default='', verbose_name='Hacer (Procedimental / Desempeño)')
    ser = models.TextField(blank=True, default='', verbose_name='Ser (Actitudinal / Convivencial)')
    evidence = models.TextField(blank=True, default='', verbose_name='Elaborar (Evidencia de Aprendizaje / Producto)')
    order = models.PositiveSmallIntegerField(default=1, verbose_name='Orden')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Resultado de Aprendizaje (RAP)'
        verbose_name_plural = 'Resultados de Aprendizaje (RAPs)'
        ordering = ['subject', 'order', 'code']

    def __str__(self):
        return f"[RAP {self.order} - {self.code}] {self.title} ({self.subject.code})"

    @property
    def rap_label(self):
        return f"RAP {self.order}"


class GradeSubject(models.Model):
    """
    Malla Curricular: Configuración de Asignatura para un Grado Escolar específico.
    Define la intensidad horaria semanal y el peso porcentual dentro del área.
    """
    grade_level = models.ForeignKey(
        'courses.GradeLevel',
        on_delete=models.CASCADE,
        related_name='curriculum_subjects',
        verbose_name='Grado Escolar'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='curriculum_grades',
        verbose_name='Asignatura'
    )
    weekly_hours = models.PositiveSmallIntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        verbose_name='Horas Semanales (Intensidad)'
    )
    weight_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('100.00'),
        validators=[MinValueValidator(Decimal('0.01')), MaxValueValidator(Decimal('100.00'))],
        verbose_name='Peso en el Área (%)'
    )

    class Meta:
        verbose_name = 'Asignatura en Malla Curricular'
        verbose_name_plural = 'Malla Curricular por Grado'
        unique_together = ('grade_level', 'subject')
        ordering = ['grade_level__order', 'subject__area__order', 'subject__name']

    def __str__(self):
        return f"{self.subject.name} - Grado {self.grade_level.name} ({self.weekly_hours}h/sem)"
