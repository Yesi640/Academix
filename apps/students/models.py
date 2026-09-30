import os
from django.db import models
from django.conf import settings
from django.utils import timezone

class StudentProfile(models.Model):
    """
    Expediente escolar único del estudiante.
    Vincula su usuario de acceso con acudiente, código de matrícula y ficha médica.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
        limit_choices_to={'role': 'STUDENT'},
        verbose_name='Usuario Institucional'
    )
    student_code = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        verbose_name='Código Estudiantil / Folio'
    )
    blood_type = models.CharField(
        max_length=5,
        default='O+',
        verbose_name='Grupo y Factor RH'
    )
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dependent_students',
        limit_choices_to={'role': 'PARENT'},
        verbose_name='Padre de Familia / Acudiente'
    )
    eps = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        verbose_name='Entidad Promotora de Salud (EPS)'
    )
    medical_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones Médicas / Alergias'
    )

    class Meta:
        verbose_name = 'Expediente Estudiantil'
        verbose_name_plural = 'Expedientes Estudiantiles'
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} (Cód: {self.student_code})"

    @property
    def current_enrollment(self):
        """Retorna la matrícula activa en el año lectivo vigente."""
        return self.enrollments.filter(status=Enrollment.Status.ACTIVE, academic_year__is_current=True).first()


class Enrollment(models.Model):
    """
    Matrícula escolar: Vincula formalmente a un estudiante con un grupo/curso específico para un año lectivo.
    Restricción estricta: Un estudiante solo puede tener una matrícula activa por año escolar.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', '🟡 Pendiente de Aprobación'
        ACTIVE = 'ACTIVE', '🟢 Matriculado / Activo'
        TRANSFERRED = 'TRANSFERRED', '🔵 Trasladado de Grupo'
        WITHDRAWN = 'WITHDRAWN', '🔴 Retirado / Desertor'
        PROMOTED = 'PROMOTED', '🎓 Promovido de Grado'
        FAILED = 'FAILED', '❌ No Promovido'

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Estudiante'
    )
    course_section = models.ForeignKey(
        'courses.CourseSection',
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Grupo / Sección'
    )
    academic_year = models.ForeignKey(
        'courses.AcademicYear',
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Año Lectivo'
    )
    enrollment_date = models.DateField(auto_now_add=True, verbose_name='Fecha de Matrícula')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
        verbose_name='Estado de Matrícula'
    )

    FINANCIAL_STATUS_CHOICES = [
        ('PAZ_Y_SALVO', '🟢 Paz y Salvo'),
        ('PENDIENTE', '🟡 Pendiente de Pago'),
        ('MORA', '🔴 En Mora'),
    ]
    financial_status = models.CharField(
        max_length=20,
        choices=FINANCIAL_STATUS_CHOICES,
        default='PAZ_Y_SALVO',
        verbose_name='Estado Financiero / Tesorería'
    )
    admission_requirement_info = models.CharField(
        max_length=150,
        blank=True,
        default='Requisitos de Admisión al día',
        verbose_name='Requisito de Admisión (Saber 11 / Prueba Aptitud / Paz y Salvo)'
    )

    class Meta:
        verbose_name = 'Matrícula Escolar'
        verbose_name_plural = 'Matrículas Escolares'
        unique_together = ('student', 'academic_year')
        ordering = ['course_section__grade_level__order', 'student__user__last_name']

    def __str__(self):
        return f"{self.student.user.get_full_name() or self.student.user.username} -> {self.course_section.name} ({self.academic_year.year})"


class StudentObservation(models.Model):
    """
    Observador del Estudiante / Bitácora de Seguimiento Convivencial y Académico.
    Permite registrar anotaciones, llamados de atención, compromisos y reconocimientos
    por parte de: Rector, Secretaría y Docentes.
    Visible para acudientes y alumnos en modo solo lectura.
    """
    class Category(models.TextChoices):
        ACADEMIC = 'ACADEMIC', '📚 Seguimiento Académico'
        DISCIPLINARY = 'DISCIPLINARY', '⚠️ Convivencial / Disciplinario'
        ATTENDANCE = 'ATTENDANCE', '⏰ Asistencia / Puntualidad'
        CITATION = 'CITATION', '📢 Citación a Acudiente'
        RECOGNITION = 'RECOGNITION', '⭐ Felicitación / Mérito'

    class Severity(models.TextChoices):
        INFO = 'INFO', 'Informativa / Positiva'
        WARNING = 'WARNING', 'Llamado de Atención'
        CRITICAL = 'CRITICAL', 'Falta Grave / Citación Urgente'

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='observations',
        verbose_name='Estudiante'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='authored_observations',
        verbose_name='Registrado por'
    )
    academic_year = models.ForeignKey(
        'courses.AcademicYear',
        on_delete=models.CASCADE,
        related_name='student_observations',
        verbose_name='Año Lectivo'
    )
    academic_period = models.ForeignKey(
        'periods.AcademicPeriod',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_observations',
        verbose_name='Periodo Lectivo'
    )
    category = models.CharField(
        max_length=25,
        choices=Category.choices,
        default=Category.ACADEMIC,
        verbose_name='Categoría'
    )
    severity = models.CharField(
        max_length=15,
        choices=Severity.choices,
        default=Severity.INFO,
        verbose_name='Nivel / Severidad'
    )
    title = models.CharField(max_length=150, verbose_name='Título de la Observación')
    description = models.TextField(verbose_name='Descripción de los Hechos')
    commitments = models.TextField(
        blank=True,
        null=True,
        verbose_name='Compromisos del Estudiante / Acuerdos'
    )
    parent_notified = models.BooleanField(
        default=False,
        verbose_name='¿Acudiente Notificado?'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')

    class Meta:
        verbose_name = 'Observación de Estudiante'
        verbose_name_plural = 'Observador de Estudiantes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.student.user.get_full_name()} ({self.get_category_display()})"

    @property
    def badge_class(self):
        mapping = {
            self.Severity.INFO: 'bg-info-subtle text-info-emphasis border-info-subtle',
            self.Severity.WARNING: 'bg-warning-subtle text-warning-emphasis border-warning-subtle',
            self.Severity.CRITICAL: 'bg-danger-subtle text-danger-emphasis border-danger-subtle',
        }
        return mapping.get(self.severity, 'bg-secondary text-white')


def expediente_upload_path(instance, filename):
    """
    Ruta dinámica y organizada en el servidor para el Expediente Digital Perpetuo:
    media/expedientes/student_<id>/<category>/<document_type>_<timestamp>.<ext>
    """
    ext = os.path.splitext(filename)[1].lower()
    timestamp = timezone.now().strftime('%Y%m%d_%H%M%S')
    doc_type = instance.document_type.lower() if instance.document_type else 'doc'
    clean_filename = f"{doc_type}_{timestamp}{ext}"
    return f"expedientes/student_{instance.student_id}/{instance.category.lower()}/{clean_filename}"


class ExpedienteDocumento(models.Model):
    """
    Módulo 2: Carpeta Perpetua y Expediente Digital del Estudiante.
    Almacena de forma inmutable, categorizada y verificable todos los soportes
    académicos, de admisión, convivenciales y administrativos a lo largo de la vida escolar del alumno.
    """
    class Category(models.TextChoices):
        ADMISSION = 'ADMISSION', '1. Admisión e Ingreso'
        ACADEMIC = 'ACADEMIC', '2. Académico'
        CONVIVENCIA = 'CONVIVENCIA', '3. Convivencia y Disciplina'
        ADMINISTRATIVE = 'ADMINISTRATIVE', '4. Administrativo y Financiero'

    class DocumentType(models.TextChoices):
        # 1. Admisión
        REGISTRO_CIVIL = 'REGISTRO_CIVIL', 'Registro Civil de Nacimiento'
        TARJETA_IDENTIDAD = 'TARJETA_IDENTIDAD', 'Tarjeta de Identidad / Cédula / DNI'
        CARNET_VACUNAS = 'CARNET_VACUNAS', 'Carnet de Vacunación'
        CERTIFICADO_EPS = 'CERTIFICADO_EPS', 'Certificado de Afiliación a EPS'
        CERTIFICADO_ESTUDIO_ANT = 'CERTIFICADO_ESTUDIO_ANT', 'Certificado de Estudios de Años Anteriores'
        FOTO_DOCUMENTO = 'FOTO_DOCUMENTO', 'Fotografía Digital Tipo Documento'
        
        # 2. Académico
        BOLETIN_OFICIAL = 'BOLETIN_OFICIAL', 'Boletín Oficial de Calificaciones'
        CERTIFICADO_ESTUDIO = 'CERTIFICADO_ESTUDIO', 'Certificado Oficial de Estudios'
        ACTA_GRADO = 'ACTA_GRADO', 'Acta de Grado / Diploma'
        INFORME_PEDAGOGICO = 'INFORME_PEDAGOGICO', 'Informe Psicopedagógico / Inclusión (PIAR)'
        
        # 3. Convivencia
        ACTA_COMPROMISO = 'ACTA_COMPROMISO', 'Acta de Compromiso Convivencial'
        DESCARGOS_DISCIPLINA = 'DESCARGOS_DISCIPLINA', 'Formato de Descargos Disciplinarios'
        CITACION_ACUDIENTE = 'CITACION_ACUDIENTE', 'Citación Formal a Acudiente'
        EXCUSA_MEDICA = 'EXCUSA_MEDICA', 'Incapacidad / Excusa Médica Validada'
        
        # 4. Administrativo
        CONTRATO_MATRICULA = 'CONTRATO_MATRICULA', 'Contrato de Matrícula y Prestación de Servicios'
        PAGARE = 'PAGARE', 'Pagaré y Carta de Instrucciones'
        PAZ_Y_SALVO = 'PAZ_Y_SALVO', 'Paz y Salvo Institucional'
        AUTORIZACION_DATOS = 'AUTORIZACION_DATOS', 'Autorización de Tratamiento de Datos (Habeas Data)'
        OTRO = 'OTRO', 'Otro Documento Institucional'

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='expediente_documentos',
        verbose_name='Estudiante'
    )
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        db_index=True,
        verbose_name='Categoría del Expediente'
    )
    document_type = models.CharField(
        max_length=30,
        choices=DocumentType.choices,
        default=DocumentType.OTRO,
        db_index=True,
        verbose_name='Tipo de Documento'
    )
    title = models.CharField(
        max_length=150,
        verbose_name='Título Descriptivo del Documento'
    )
    file = models.FileField(
        upload_to=expediente_upload_path,
        verbose_name='Archivo Digital (PDF, JPG, PNG)'
    )
    academic_year = models.ForeignKey(
        'courses.AcademicYear',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='expediente_documentos',
        verbose_name='Año Lectivo Asociado'
    )
    is_verified = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='¿Verificado Oficialmente por Secretaría?'
    )
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_expediente_docs',
        verbose_name='Funcionario que Verificó'
    )
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha y Hora de Verificación'
    )
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='uploaded_expediente_docs',
        verbose_name='Subido por'
    )
    uploaded_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha y Hora de Subida'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones / Número de Folio Físico'
    )

    class Meta:
        verbose_name = 'Documento del Expediente'
        verbose_name_plural = 'Documentos del Expediente (Carpeta Perpetua)'
        ordering = ['category', '-uploaded_at']
        indexes = [
            models.Index(fields=['student', 'category']),
            models.Index(fields=['student', 'document_type']),
        ]

    def __str__(self):
        status = " [VERIFICADO]" if self.is_verified else " [PENDIENTE]"
        return f"{self.get_category_display()} - {self.title}{status}"

    def verify(self, user):
        """Marca formalmente el documento como verificado por secretaría."""
        self.is_verified = True
        self.verified_by = user
        self.verified_at = timezone.now()
        self.save(update_fields=['is_verified', 'verified_by', 'verified_at'])

    @property
    def file_extension(self):
        if self.file and self.file.name:
            return os.path.splitext(self.file.name)[1].lower().replace('.', '')
        return ''

    @property
    def is_pdf(self):
        return self.file_extension == 'pdf'

    @property
    def is_image(self):
        return self.file_extension in ['jpg', 'jpeg', 'png', 'webp']

    @property
    def category_badge_class(self):
        mapping = {
            self.Category.ADMISSION: 'bg-primary-subtle text-primary border border-primary-subtle',
            self.Category.ACADEMIC: 'bg-success-subtle text-success border border-success-subtle',
            self.Category.CONVIVENCIA: 'bg-warning-subtle text-warning-emphasis border border-warning-subtle',
            self.Category.ADMINISTRATIVE: 'bg-info-subtle text-info-emphasis border border-info-subtle',
        }
        return mapping.get(self.category, 'bg-secondary-subtle text-secondary')


