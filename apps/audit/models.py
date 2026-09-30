from django.db import models
from django.conf import settings
from django.core.exceptions import PermissionDenied


class ImmutableAuditQuerySet(models.QuerySet):
    """QuerySet blindado para prevenir alteraciones o borrados masivos de logs."""
    def delete(self):
        raise PermissionDenied("Los registros de auditoría son estrictamente inmutables y no pueden eliminarse en masa.")

    def update(self, **kwargs):
        raise PermissionDenied("Los registros de auditoría son inmutables y no pueden modificarse en masa.")


class AuditLogManager(models.Manager):
    def get_queryset(self):
        return ImmutableAuditQuerySet(self.model, using=self._db)


class AuditLog(models.Model):
    """
    Pilar 6: Registro inmutable de auditoría (AuditTrail) para trazabilidad estricta.
    Almacena quién, cuándo, qué afectó, valores anteriores y nuevos en JSON, IP, User-Agent y justificación.
    No permite modificaciones ni eliminaciones bajo ninguna circunstancia.
    """
    class Action(models.TextChoices):
        INSERT = 'INSERT', 'Creación (INSERT)'
        UPDATE = 'UPDATE', 'Modificación (UPDATE)'
        DELETE = 'DELETE', 'Eliminación (DELETE)'
        LOGIN = 'LOGIN', 'Inicio de Sesión'
        LOGOUT = 'LOGOUT', 'Cierre de Sesión'
        FAILED_LOGIN = 'FAILED_LOGIN', 'Intento Fallido de Inicio de Sesión'
        PERIOD_CLOSE = 'PERIOD_CLOSE', 'Cierre de Periodo Académico'
        GRADE_OVERRIDE = 'GRADE_OVERRIDE', 'Modificación Extraordinaria de Nota'
        OBSERVATION_DELETED = 'OBSERVATION_DELETED', 'Eliminación de Observador / Convivencia'
        ATTENDANCE_OVERRIDE = 'ATTENDANCE_OVERRIDE', 'Modificación de Asistencia Docente'
        ENROLLMENT_ALTERED = 'ENROLLMENT_ALTERED', 'Alteración de Matrícula o Estado de Alumno'
        OFFICIAL_REPORT_EXPORT = 'OFFICIAL_REPORT_EXPORT', 'Exportación de Reporte Oficial / SIMAT'
        SECURITY_ALERT = 'SECURITY_ALERT', 'Alerta Crítica de Seguridad'
        FINANCIAL_TRANSACTION = 'FINANCIAL_TRANSACTION', 'Transacción o Modificación Financiera'
        CONFIG_CHANGE = 'CONFIG_CHANGE', 'Cambio en Parametrización Institucional'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='audit_logs',
        verbose_name='Usuario Responsable'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        verbose_name='Fecha y Hora'
    )
    action = models.CharField(
        max_length=30,
        choices=Action.choices,
        db_index=True,
        verbose_name='Acción Realizada'
    )
    table_name = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name='Tabla / Entidad Afectada'
    )
    record_id = models.CharField(
        max_length=64,
        null=True,
        blank=True,
        db_index=True,
        verbose_name='ID de Registro Afectado'
    )
    old_values = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Valores Anteriores'
    )
    new_values = models.JSONField(
        null=True,
        blank=True,
        verbose_name='Valores Nuevos'
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
        verbose_name='Dirección IP'
    )
    user_agent = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='Navegador / Dispositivo (User Agent)'
    )
    reason = models.TextField(
        null=True,
        blank=True,
        verbose_name='Motivo / Justificación'
    )

    objects = AuditLogManager()

    class Meta:
        verbose_name = 'Registro de Auditoría'
        verbose_name_plural = 'Registros de Auditoría'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['table_name', 'record_id']),
            models.Index(fields=['action', 'timestamp']),
            models.Index(fields=['user', 'timestamp']),
        ]

    def __str__(self):
        user_name = self.user.username if self.user else 'Sistema/Anónimo'
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {self.action} en {self.table_name} (#{self.record_id}) por {user_name}"

    def save(self, *args, **kwargs):
        """Previene la modificación de registros ya existentes garantizando inmutabilidad estricta."""
        if self.pk is not None:
            raise PermissionDenied("Los registros de auditoría son estrictamente inmutables y no pueden modificarse.")
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Previene la eliminación individual de registros de auditoría."""
        raise PermissionDenied("Los registros de auditoría son inmutables y no pueden eliminarse.")


# Alias de clase para cumplir explícitamente con la nomenclatura de arquitectura de misión crítica
AuditTrail = AuditLog
