from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class AcademicYear(models.Model):
    """
    Año Lectivo escolar (ej. 2026).
    Solo un año lectivo puede ser el año activo (is_current=True).
    """
    class Status(models.TextChoices):
        PLANNING = 'PLANNING', 'En Planificación'
        ACTIVE = 'ACTIVE', 'En Curso (Activo)'
        CLOSED = 'CLOSED', 'Cerrado / Concluido'

    year = models.PositiveSmallIntegerField(unique=True, verbose_name='Año Calendario')
    name = models.CharField(max_length=60, verbose_name='Nombre Descriptivo')
    start_date = models.DateField(verbose_name='Fecha de Inicio')
    end_date = models.DateField(verbose_name='Fecha de Finalización')
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PLANNING,
        db_index=True,
        verbose_name='Estado'
    )
    is_current = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='¿Es el Año Vigente Actual?'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Año Lectivo'
        verbose_name_plural = 'Años Lectivos'
        ordering = ['-year']

    def __str__(self):
        current_badge = " [VIGENTE]" if self.is_current else ""
        return f"{self.name} ({self.get_status_display()}){current_badge}"


class GradeLevel(models.Model):
    """
    Grado, Nivel, Trimestre o Semestre Escolar según el tipo de institución.
    """
    class LevelStage(models.TextChoices):
        PREESCOLAR = 'PREESCOLAR', 'Educación Preescolar'
        PRIMARIA = 'PRIMARIA', 'Básica Primaria'
        SECUNDARIA = 'SECUNDARIA', 'Básica Secundaria'
        MEDIA = 'MEDIA', 'Educación Media'
        SUPERIOR = 'SUPERIOR', 'Educación Superior'
        TECNICO = 'TECNICO', 'Formación Técnica / Tecnológica'
        CONTINUA = 'CONTINUA', 'Educación Continua / Cursos'

    institution_type = models.CharField(
        max_length=20,
        default='COLEGIO',
        db_index=True,
        verbose_name='Tipo de Institución'
    )
    name = models.CharField(max_length=60, verbose_name='Nombre del Grado / Nivel')
    code = models.CharField(max_length=25, verbose_name='Código de Grado')
    level_stage = models.CharField(
        max_length=20,
        choices=LevelStage.choices,
        default=LevelStage.SECUNDARIA,
        verbose_name='Nivel Académico'
    )
    order = models.PositiveSmallIntegerField(default=1, verbose_name='Orden Numérico')

    class Meta:
        verbose_name = 'Grado / Nivel'
        verbose_name_plural = 'Grados / Niveles'
        unique_together = ('institution_type', 'code')
        ordering = ['institution_type', 'order']

    def __str__(self):
        return f"{self.name} ({self.code})"


class CourseSection(models.Model):
    """
    Curso, Grupo o Sección Escolar (ej. 6-A, 10-1) dentro de un año lectivo.
    """
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name='sections',
        verbose_name='Año Lectivo'
    )
    grade_level = models.ForeignKey(
        GradeLevel,
        on_delete=models.PROTECT,
        related_name='sections',
        verbose_name='Grado Escolar'
    )
    name = models.CharField(max_length=25, verbose_name='Identificador del Grupo (ej. 6-A)')
    classroom = models.CharField(max_length=50, blank=True, null=True, verbose_name='Aula Asignada')
    homeroom_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='homeroom_sections',
        limit_choices_to={'role': 'TEACHER'},
        verbose_name='Director de Grupo'
    )
    capacity = models.PositiveSmallIntegerField(default=35, verbose_name='Cupo Máximo')
    is_active = models.BooleanField(default=True, verbose_name='¿Grupo Activo?')

    class Meta:
        verbose_name = 'Curso / Grupo'
        verbose_name_plural = 'Cursos / Grupos'
        unique_together = ('academic_year', 'grade_level', 'name')
        ordering = ['academic_year', 'grade_level__order', 'name']

    def __str__(self):
        return f"{self.name} - {self.academic_year.year}"

    @property
    def enrolled_count(self):
        return self.enrollments.filter(status='ACTIVE').count()


class InstitutionSetting(models.Model):
    """
    Configuración adaptable de la institución educativa.
    Permite que ACADEMIX funcione para Colegios, Universidades, Institutos Técnicos (SENA) o Academias.
    """
    class InstitutionType(models.TextChoices):
        COLEGIO = 'COLEGIO', 'Colegio / Escuela (Básica y Media)'
        UNIVERSIDAD = 'UNIVERSIDAD', 'Universidad / Educación Superior'
        SENA_TECNICO = 'SENA_TECNICO', 'Instituto Técnico / Tecnológico / SENA'
        ACADEMIA = 'ACADEMIA', 'Academia / Educación Continua'
        OTRO = 'OTRO', 'Institución Personalizada'

    class SchoolLevelScope(models.TextChoices):
        COMPLETA = 'COMPLETA', 'Colegio Completo (Transición, Primaria y Secundaria/Media)'
        PRIMARIA = 'PRIMARIA', 'Solo Primaria (Transición, 1° a 5°)'
        SECUNDARIA = 'SECUNDARIA', 'Solo Secundaria y Media (6° a 11°)'

    class SectorMode(models.TextChoices):
        PUBLIC = 'PUBLICO', 'Colegio Oficial / Público (Estatal - Gratuidad)'
        PRIVATE = 'PRIVADO', 'Colegio Privado / No Oficial'

    class GradingScaleType(models.TextChoices):
        NUMERIC_5 = 'NUMERIC_5', 'Cuantitativa Tradicional (1.00 - 5.00)'
        NUMERIC_100 = 'NUMERIC_100', 'Cuantitativa Centesimal (0.00 - 100.00)'
        NUMERIC_10 = 'NUMERIC_10', 'Cuantitativa Decimal (1.00 - 10.00)'
        CONCEPTUAL_MEN = 'CONCEPTUAL_MEN', 'Conceptual Oficial MEN (Superior, Alto, Básico, Bajo)'

    class PeriodStructure(models.TextChoices):
        PERIODS_4 = 'PERIODS_4', '4 Periodos Académicos (25% c/u - Estándar Oficial)'
        TRIMESTERS_3 = 'TRIMESTERS_3', '3 Trimestres (33.33% c/u)'
        SEMESTERS_2 = 'SEMESTERS_2', '2 Semestres (50% c/u)'

    institution_type = models.CharField(
        max_length=20,
        choices=InstitutionType.choices,
        default=InstitutionType.COLEGIO,
        verbose_name='Tipo de Institución'
    )
    sector_mode = models.CharField(
        max_length=15,
        choices=SectorMode.choices,
        default=SectorMode.PRIVATE,
        db_index=True,
        verbose_name='Sector Institucional',
        help_text='Pilar 1 SaaS Híbrido: Determina si rigen normas estatales (gratuidad, SIMAT, PAE) o comerciales (facturación, admisiones).'
    )
    school_scope = models.CharField(
        max_length=20,
        choices=SchoolLevelScope.choices,
        default=SchoolLevelScope.COMPLETA,
        verbose_name='Enfoque del Colegio',
        help_text='Aplica para Colegios: Define si ofrece Primaria, Secundaria o Ambos niveles.'
    )

    # ── Parametrización Académica y Evaluación ──────────────────────────────
    grading_scale_type = models.CharField(
        max_length=20,
        choices=GradingScaleType.choices,
        default=GradingScaleType.NUMERIC_5,
        verbose_name='Escala de Calificación Activa'
    )
    min_grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('1.00'),
        verbose_name='Nota Mínima Posible'
    )
    max_grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('5.00'),
        verbose_name='Nota Máxima Posible'
    )
    passing_grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('3.00'),
        verbose_name='Nota Mínima Aprobatoria'
    )
    grade_decimal_places = models.PositiveSmallIntegerField(
        default=2,
        verbose_name='Cifras Decimales en Notas'
    )
    period_structure = models.CharField(
        max_length=20,
        choices=PeriodStructure.choices,
        default=PeriodStructure.PERIODS_4,
        verbose_name='Estructura de Periodos del Año'
    )

    # ── Parametrización Privada: Financiero, Pasarelas y Cobros ──────────────
    enable_tuition_billing = models.BooleanField(
        default=True,
        verbose_name='Habilitar Facturación de Matrículas y Pensiones',
        help_text='Habilita el módulo de cobro recurrente para instituciones privadas.'
    )
    block_report_cards_on_debt = models.BooleanField(
        default=False,
        verbose_name='Bloqueo de Boletines por Morosidad Económica',
        help_text='Bloquea la descarga de boletines a familias con saldo pendiente. En colegios oficiales se fuerza a inactivo por ley.'
    )
    enable_payment_gateway = models.BooleanField(
        default=False,
        verbose_name='Habilitar Pasarela de Pagos en Línea (PSE/Wompi/Stripe)'
    )
    enable_online_admissions = models.BooleanField(
        default=True,
        verbose_name='Habilitar Admisiones en Línea y Contratos'
    )

    # ── Parametrización Pública: Gratuidad, PAE y SIMAT Oficial ──────────────
    enable_gratuity_control = models.BooleanField(
        default=False,
        verbose_name='Control de Gratuidad Estatal',
        help_text='Aplica para Colegios Públicos: Garantiza gratuidad universal en matrículas y certificados.'
    )
    enable_pae_module = models.BooleanField(
        default=False,
        verbose_name='Módulo de Alimentación Escolar (PAE / Refrigerios)',
        help_text='Control diario de cupos, entregas de refrigerios y beneficiarios PAE.'
    )
    enable_simat_integration = models.BooleanField(
        default=False,
        verbose_name='Integración y Exportación de Archivos Oficiales SIMAT (MEN)'
    )
    dane_code = models.CharField(
        max_length=25,
        blank=True,
        default='',
        verbose_name='Código DANE de la Sede Educativa'
    )
    consecutive_resolution = models.CharField(
        max_length=150,
        blank=True,
        default='',
        verbose_name='Resolución de Reconocimiento Oficial / NIT'
    )

    institution_name = models.CharField(
        max_length=150,
        default='ACADEMIX',
        verbose_name='Nombre de la Institución'
    )
    slogan = models.CharField(
        max_length=255,
        blank=True,
        default='Sistema Integral de Gestión Académica y Control Escolar',
        verbose_name='Lema o Subtítulo'
    )

    # ── Branding e Identidad Visual ──────────────────────────────────────────
    logo = models.ImageField(
        upload_to='institution/logos/',
        blank=True,
        null=True,
        verbose_name='Logo Institucional (PNG/SVG recomendado)',
        help_text='Logo que aparecerá en el login y la barra lateral.'
    )
    primary_color = models.CharField(
        max_length=7,
        default='#7c3aed',
        verbose_name='Color Primario (hex)',
        help_text='Color principal de la institución. Ej: #7c3aed (morado ACADEMIX), #1b4332 (verde), #1e3a8a (azul).'
    )
    secondary_color = models.CharField(
        max_length=7,
        default='#c4b5fd',
        verbose_name='Color Secundario / Pastel (hex)',
        help_text='Color de acentos y fondos claros. Suele ser una versión más clara del color primario.'
    )
    hero_image = models.ImageField(
        upload_to='institution/hero/',
        blank=True,
        null=True,
        verbose_name='Imagen Hero de la Página de Login',
        help_text='Foto del colegio o estudiantes que aparece en el fondo del login.'
    )
    contact_email = models.EmailField(
        blank=True,
        default='',
        verbose_name='Correo de Contacto Institucional'
    )
    contact_phone = models.CharField(
        max_length=30,
        blank=True,
        default='',
        verbose_name='Teléfono de Contacto'
    )
    website_url = models.URLField(
        blank=True,
        default='',
        verbose_name='Sitio Web Oficial'
    )

    # Terminología Adaptable
    term_student = models.CharField(max_length=30, default='Estudiante', verbose_name='Término Alumno (Singular)')
    term_students = models.CharField(max_length=30, default='Estudiantes', verbose_name='Término Alumnos (Plural)')
    term_teacher = models.CharField(max_length=30, default='Docente', verbose_name='Término Profesor (Singular)')
    term_teachers = models.CharField(max_length=30, default='Docentes', verbose_name='Término Profesores (Plural)')
    term_grade = models.CharField(max_length=30, default='Grado', verbose_name='Término Nivel/Grado (ej. Semestre/Grado/Ciclo)')
    term_section = models.CharField(max_length=30, default='Curso', verbose_name='Término Grupo/Curso (ej. Ficha/Curso/Grupo)')
    term_sections = models.CharField(max_length=30, default='Cursos', verbose_name='Término Grupos/Cursos (Plural)')
    term_subject = models.CharField(max_length=30, default='Asignatura', verbose_name='Término Materia (ej. Módulo/Competencia)')
    term_subjects = models.CharField(max_length=30, default='Asignaturas', verbose_name='Término Materias (Plural)')
    term_director = models.CharField(max_length=30, default='Rector(a)', verbose_name='Término Director(a)/Decano(a)')

    updated_at = models.DateTimeField(auto_now=True)

    @property
    def primary_color_rgb(self):
        """Convierte el color hex primario a formato RGB para CSS."""
        c = self.primary_color.lstrip('#')
        if len(c) == 6:
            r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
            return f"{r}, {g}, {b}"
        return "124, 58, 237"

    @property
    def secondary_color_rgb(self):
        """Convierte el color hex secundario a formato RGB para CSS."""
        c = self.secondary_color.lstrip('#')
        if len(c) == 6:
            r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
            return f"{r}, {g}, {b}"
        return "196, 181, 253"


    class Meta:
        verbose_name = 'Configuración Institucional'
        verbose_name_plural = 'Configuración Institucional'

    def __str__(self):
        return f"{self.institution_name} ({self.get_institution_type_display()})"

    @classmethod
    def get_settings(cls):
        """Retorna la configuración activa o crea una por defecto."""
        setting, _ = cls.objects.get_or_create(id=1)
        return setting

    @property
    def has_parents(self):
        """
        Indica si este modelo institucional maneja acudientes / padres de familia.
        Exclusivo para Colegios / Escuelas (Básica y Media).
        En Universidad, SENA / Técnico y Academia los alumnos son independientes.
        """
        return self.institution_type == self.InstitutionType.COLEGIO

    @property
    def is_public_institution(self):
        """Indica si la institución educativa es oficial/pública (gratuidad, SIMAT, PAE)."""
        return self.sector_mode == self.SectorMode.PUBLIC

    @property
    def is_private_institution(self):
        """Indica si la institución es privada / no oficial (facturación, pasarelas, admisiones)."""
        return self.sector_mode == self.SectorMode.PRIVATE

    @property
    def allows_report_card_debt_blocking(self):
        """
        Regla de negocio crítica: Un colegio público NO puede retener boletines por morosidad
        financiera por prohibición legal y constitucional de gratuidad universal.
        Solo se permite si la institución es privada Y tiene la bandera encendida.
        """
        return self.is_private_institution and self.block_report_cards_on_debt

    def clean(self):
        super().clean()
        if self.is_public_institution and self.block_report_cards_on_debt:
            # Corrección automática para asegurar cumplimiento legal
            self.block_report_cards_on_debt = False

        if self.min_grade >= self.max_grade:
            raise ValidationError({'min_grade': 'La nota mínima debe ser estrictamente menor a la nota máxima.'})

        if not (self.min_grade <= self.passing_grade <= self.max_grade):
            raise ValidationError({'passing_grade': 'La nota aprobatoria debe encontrarse entre la nota mínima y máxima.'})

    def apply_sector_preset(self, sector):
        """
        Aprovisiona y conmuta en caliente todas las reglas del SaaS Híbrido:
        - Modo Público: Gratuidad activa, PAE activo, SIMAT activo, 4 periodos estándar,
          retención de boletines bloqueada por ley.
        - Modo Privado: Facturación activa, admisiones activas, pasarela de pagos activa,
          bloqueo de boletines por morosidad disponible.
        """
        self.sector_mode = sector
        if sector == self.SectorMode.PUBLIC:
            self.enable_tuition_billing = False
            self.block_report_cards_on_debt = False
            self.enable_payment_gateway = False
            self.enable_online_admissions = False
            self.enable_gratuity_control = True
            self.enable_pae_module = True
            self.enable_simat_integration = True
            self.period_structure = self.PeriodStructure.PERIODS_4
            self.grading_scale_type = self.GradingScaleType.NUMERIC_5
            self.min_grade = Decimal('1.00')
            self.max_grade = Decimal('5.00')
            self.passing_grade = Decimal('3.00')
            self.grade_decimal_places = 2
        else: # PRIVADO
            self.enable_tuition_billing = True
            self.block_report_cards_on_debt = True
            self.enable_payment_gateway = True
            self.enable_online_admissions = True
            self.enable_gratuity_control = False
            self.enable_pae_module = False
            self.enable_simat_integration = False
        self.save()

    def apply_preset(self, preset_type):
        """Aplica terminología estándar según el tipo de entidad educativa."""
        self.institution_type = preset_type
        if preset_type == self.InstitutionType.UNIVERSIDAD:
            self.term_student = 'Estudiante'
            self.term_students = 'Estudiantes'
            self.term_teacher = 'Profesor(a)'
            self.term_teachers = 'Profesores'
            self.term_grade = 'Semestre'
            self.term_section = 'Grupo'
            self.term_sections = 'Grupos'
            self.term_subject = 'Materia'
            self.term_subjects = 'Materias'
            self.term_director = 'Decano(a)'
        elif preset_type == self.InstitutionType.SENA_TECNICO:
            self.term_student = 'Aprendiz'
            self.term_students = 'Aprendices'
            self.term_teacher = 'Instructor(a)'
            self.term_teachers = 'Instructores'
            self.term_grade = 'Trimestre'
            self.term_section = 'Ficha'
            self.term_sections = 'Fichas'
            self.term_subject = 'Competencia / Módulo'
            self.term_subjects = 'Competencias / Módulos'
            self.term_director = 'Subdirector(a)'
        elif preset_type == self.InstitutionType.ACADEMIA:
            self.term_student = 'Alumno(a)'
            self.term_students = 'Alumnos'
            self.term_teacher = 'Tutor(a)'
            self.term_teachers = 'Tutores'
            self.term_grade = 'Nivel'
            self.term_section = 'Grupo / Clase'
            self.term_sections = 'Grupos / Clases'
            self.term_subject = 'Módulo / Taller'
            self.term_subjects = 'Módulos / Talleres'
            self.term_director = 'Director(a)'
        else: # COLEGIO
            self.term_student = 'Estudiante'
            self.term_students = 'Estudiantes'
            self.term_teacher = 'Docente'
            self.term_teachers = 'Docentes'
            self.term_grade = 'Grado'
            self.term_section = 'Curso'
            self.term_sections = 'Cursos'
            self.term_subject = 'Asignatura'
            self.term_subjects = 'Asignaturas'
            self.term_director = 'Rector(a)'
        self.save()
        try:
            from .environment_provisioner import provision_institution_environment
            provision_institution_environment(preset_type)
        except Exception as e:
            import logging
            logging.getLogger(__name__).warning(f"Error al aprovisionar entorno {preset_type}: {e}")


# Alias solicitado en la arquitectura para acceso semántico
InstitutionSettings = InstitutionSetting

