import functools
from django.core.exceptions import ValidationError, PermissionDenied
from django.http import JsonResponse
from .services import log_audit

def audit_action(action, table_name, reason_required=False, get_record_id=None):
    """
    Decorator para vistas Django (FBVs) que registra automáticamente un evento de auditoría.
    Si `reason_required=True`, exige que la petición (POST o GET) incluya un parámetro 'reason' o 'justification'.
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            reason = request.POST.get('reason') or request.POST.get('justification') or request.GET.get('reason') or ''
            
            if reason_required and not reason.strip():
                error_msg = f"Se requiere obligatoriamente una justificación para la acción '{action}'."
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                    return JsonResponse({'status': 'error', 'message': error_msg}, status=400)
                raise ValidationError(error_msg)

            # Ejecutar la vista
            response = view_func(request, *args, **kwargs)

            # Si la respuesta fue exitosa (código 2xx o redirección 302 estándar tras POST)
            if response.status_code in [200, 201, 204, 302]:
                record_id = None
                if callable(get_record_id):
                    try:
                        record_id = get_record_id(request, *args, **kwargs)
                    except Exception:
                        pass
                elif 'pk' in kwargs:
                    record_id = kwargs['pk']
                elif 'id' in kwargs:
                    record_id = kwargs['id']

                log_audit(
                    action=action,
                    table_name=table_name,
                    record_id=record_id,
                    new_values={'method': request.method, 'path': request.path},
                    reason=reason or f"Ejecución de acción {action} vía vista {view_func.__name__}",
                    user=request.user if request.user.is_authenticated else None,
                    request=request
                )

            return response
        return _wrapped_view
    return decorator
