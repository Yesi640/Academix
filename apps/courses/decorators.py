import functools
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseForbidden
from .services import (
    get_institution_settings,
    is_public_school_mode,
    is_private_school_mode,
    is_feature_active,
    can_download_report_card,
)


def require_sector_mode(allowed_mode):
    """
    Decorador para vistas que solo aplican a un modo específico del SaaS Híbrido (PUBLICO o PRIVADO).
    Ejemplo: Vistas del PAE o SIMAT (exclusivas de PUBLICO), o pasarelas de pago (exclusivas de PRIVADO).
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            setting = get_institution_settings()
            if setting.sector_mode != allowed_mode:
                error_msg = (
                    f"Esta funcionalidad está restringida a instituciones en modo "
                    f"'{setting.SectorMode(allowed_mode).label}'. "
                    f"El modo actual de la institución es '{setting.get_sector_mode_display()}'."
                )
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                    return JsonResponse({'status': 'forbidden', 'message': error_msg}, status=403)
                raise PermissionDenied(error_msg)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def require_public_school(view_func):
    """Decorador abreviado para vistas exclusivas de colegios públicos / oficiales (PAE, gratuidad, SIMAT)."""
    return require_sector_mode('PUBLICO')(view_func)


def require_private_school(view_func):
    """Decorador abreviado para vistas exclusivas de colegios privados (facturación recurrente, cartera, admisiones comerciales)."""
    return require_sector_mode('PRIVADO')(view_func)


def require_institution_feature(feature_flag_name):
    """
    Decorador que valida si una bandera específica está activada en la parametrización institucional.
    Ej: @require_institution_feature('enable_pae_module')
        @require_institution_feature('enable_tuition_billing')
        @require_institution_feature('enable_payment_gateway')
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not is_feature_active(feature_flag_name):
                error_msg = f"El módulo '{feature_flag_name}' no se encuentra habilitado para esta institución."
                if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                    return JsonResponse({'status': 'forbidden', 'message': error_msg}, status=403)
                raise PermissionDenied(error_msg)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def enforce_report_card_clearance(student_param_name='student_id'):
    """
    Decorador de control de acceso para generación/descarga de boletines.
    En Colegios Oficiales: Siempre permite la descarga sin restricción económica por mandato constitucional.
    En Colegios Privados: Valida si la institución bloquea por morosidad y verifica si el estudiante tiene mora.
    """
    def decorator(view_func):
        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            student_id = kwargs.get(student_param_name) or request.GET.get(student_param_name) or request.POST.get(student_param_name)
            
            student_profile = None
            if student_id:
                try:
                    from apps.students.models import StudentProfile
                    student_profile = StudentProfile.objects.filter(id=student_id).first()
                except Exception:
                    pass
            elif hasattr(request.user, 'student_profile'):
                student_profile = request.user.student_profile

            if student_profile:
                can_download, reason = can_download_report_card(student_profile)
                if not can_download:
                    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
                        return JsonResponse({'status': 'blocked', 'message': reason}, status=403)
                    raise PermissionDenied(f"Acceso restringido al boletín: {reason}")

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
