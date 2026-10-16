from django.db import models
from django.contrib.auth.models import AbstractUser


class School(models.Model):
    """
    Institución Educativa registrada en la plataforma ACADEMIX.
    Permite a un solo software servir a múltiples colegios/escuelas (SaaS Multi-Escuela).
    Cada usuario pertenece a una escuela; el Administrador de la plataforma gestiona todas.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Nombre de la Institución',
        help_text='Nombre oficial del colegio tal como aparece en la resolución.'
    )
    code = models.CharField(
        max_length=30,
        unique=True,
        verbose_name='Código Interno / Slug',
        help_text='Código corto único para identificar la escuela (ej: COL-BUGA-01).'
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        default='',
        verbose_name='Ciudad / Municipio'
    )
    dane_code = models.CharField(
        max_length=25,
        blank=True,
        default='',
        verbose_name='Código DANE'
    )
    logo = models.ImageField(
        upload_to='schools/logos/',
        blank=True,
        null=True,
        verbose_name='Logo de la Escuela'
    )
    primary_color = models.CharField(
        max_length=7,
        default='#7c3aed',
        verbose_name='Color Primario (hex)'
    )
    secondary_color = models.CharField(
        max_length=7,
        default='#c4b5fd',
        verbose_name='Color Secundario (hex)'
    )
    contact_email = models.EmailField(
        blank=True,
        default='',
        verbose_name='Correo Institucional'
    )
    contact_phone = models.CharField(
        max_length=30,
        blank=True,
        default='',
        verbose_name='Teléfono Institucional'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activa / Habilitada',
        help_text='Solo las escuelas activas aparecen en el login y registro.'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Escuela / Institución'
        verbose_name_plural = 'Escuelas / Instituciones'
        ordering = ['name']

    def __str__(self):
        city_part = f' — {self.city}' if self.city else ''
        return f'{self.name}{city_part}'

    @property
    def primary_color_rgb(self):
        c = self.primary_color.lstrip('#')
        if len(c) == 6:
            r, g, b = int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)
            return f'{r}, {g}, {b}'
        return '124, 58, 237'


class CustomUser(AbstractUser):
    """
    Modelo de Usuario Extendido para el Sistema ACADEMIX.
    Soporta los 6 roles clave institucionales y datos de identificación escolar.
    """
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        RECTOR = 'RECTOR', 'Directivo / Rector'
        SECRETARIA = 'SECRETARIA', 'Secretaría Académica'
        TEACHER = 'TEACHER', 'Docente'
        STUDENT = 'STUDENT', 'Estudiante'
        PARENT = 'PARENT', 'Padre de Familia / Acudiente'

    class DocumentType(models.TextChoices):
        CC = 'CC', 'Cédula de Ciudadanía'
        TI = 'TI', 'Tarjeta de Identidad'
        CE = 'CE', 'Cédula de Extranjería'
        PASSPORT = 'PASSPORT', 'Pasaporte'
        PEP = 'PEP', 'Permiso Especial de Permanencia'
        RC = 'RC', 'Registro Civil'

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STUDENT,
        db_index=True,
        verbose_name='Rol en el Sistema'
    )
    document_type = models.CharField(
        max_length=10,
        choices=DocumentType.choices,
        default=DocumentType.CC,
        verbose_name='Tipo de Documento'
    )
    document_number = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True,
        db_index=True,
        verbose_name='Número de Documento'
    )
    phone = models.CharField(
        max_length=25,
        blank=True,
        null=True,
        verbose_name='Teléfono de Contacto'
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Dirección de Residencia'
    )
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Foto de Perfil'
    )
    must_change_password = models.BooleanField(
        default=False,
        verbose_name='Debe Cambiar Contraseña'
    )
    school = models.ForeignKey(
        'School',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name='Escuela / Institución',
        help_text='Institución educativa a la que pertenece este usuario. Nulo = Super-Administrador de la plataforma.'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    class Meta:
        verbose_name = 'Usuario Institucional'
        verbose_name_plural = 'Usuarios Institucionales'
        ordering = ['last_name', 'first_name', 'username']

    def __str__(self):
        full_name = self.get_full_name()
        return f"{full_name} ({self.get_role_display()})" if full_name else f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin_role(self):
        return self.role == self.Role.ADMIN or self.is_superuser

    @property
    def is_rector(self):
        return self.role == self.Role.RECTOR

    @property
    def is_secretary(self):
        return self.role == self.Role.SECRETARIA

    @property
    def is_teacher(self):
        return self.role == self.Role.TEACHER

    @property
    def is_student(self):
        return self.role == self.Role.STUDENT

    @property
    def is_parent(self):
        return self.role == self.Role.PARENT

    @property
    def is_group_director(self):
        """Indica si el usuario es docente y director de grupo de al menos un curso activo."""
        if not self.is_teacher or not hasattr(self, 'teacher_profile'):
            return False
        return self.teacher_profile.assignments.filter(is_group_director=True, is_active=True).exists()

    @property
    def can_view_sabana(self):
        """
        Indica si el usuario tiene permiso para ver la sábana de notas:
        - Coordinador / Directivo / Rector
        - Administrador
        - Secretaría Académica
        - Docente Director de Grupo
        """
        if self.is_admin_role or self.is_rector or self.is_secretary:
            return True
        return self.is_group_director

    def get_role_badge_class(self):
        """Retorna la clase CSS de Bootstrap para badges según rol."""
        badge_map = {
            self.Role.ADMIN: 'bg-danger text-white',
            self.Role.RECTOR: 'bg-primary text-white',
            self.Role.SECRETARIA: 'bg-info text-dark',
            self.Role.TEACHER: 'bg-success text-white',
            self.Role.STUDENT: 'bg-warning text-dark',
            self.Role.PARENT: 'bg-secondary text-white',
        }
        return badge_map.get(self.role, 'bg-dark text-white')


class SystemThemeSettings(models.Model):
    """
    Configuración Global de Tema definida por el Rector.
    Singleton: Solo existe una fila. Cuando el Rector cambia el tema del sistema,
    todos los usuarios (excepto los que ya tienen un tema personal guardado) verán
    el nuevo tema institucional como base.
    """
    theme_data = models.JSONField(
        default=dict,
        verbose_name='Datos del Tema Global',
        help_text='JSON completo con los tokens de color y tipografía del tema institucional.'
    )
    updated_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='theme_updates',
        verbose_name='Actualizado Por'
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Última Actualización')

    class Meta:
        verbose_name = 'Configuración de Tema del Sistema'
        verbose_name_plural = 'Configuración de Tema del Sistema'

    def __str__(self):
        return f'Tema Global — actualizado {self.updated_at.strftime("%d/%m/%Y %H:%M")} por {self.updated_by}'

    @classmethod
    def get_global_theme(cls):
        """Retorna el tema global activo, o None si no ha sido configurado por el Rector."""
        obj = cls.objects.first()
        if obj and obj.theme_data:
            return obj.theme_data
        return None

    @classmethod
    def set_global_theme(cls, theme_data: dict, user):
        """Guarda o actualiza el tema global institucional definido por el Rector."""
        obj, _ = cls.objects.get_or_create(pk=1)
        obj.theme_data = theme_data
        obj.updated_by = user
        obj.save()
        return obj
