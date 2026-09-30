from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'action', 'table_name', 'record_id', 'user', 'ip_address', 'user_agent')
    list_filter = ('action', 'table_name', 'timestamp')
    search_fields = ('record_id', 'reason', 'user__username', 'table_name', 'ip_address', 'user_agent')
    readonly_fields = ('user', 'timestamp', 'action', 'table_name', 'record_id', 'old_values', 'new_values', 'ip_address', 'user_agent', 'reason')
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        """Los registros de auditoría solo se crean programáticamente mediante el servicio."""
        return False

    def has_change_permission(self, request, obj=None):
        """Los registros de auditoría son inmutables."""
        return False

    def has_delete_permission(self, request, obj=None):
        """Los registros de auditoría no pueden eliminarse."""
        return False
