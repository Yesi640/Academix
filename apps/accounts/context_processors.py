from .models import SystemThemeSettings


def global_theme(request):
    """
    Context processor que inyecta el tema global definido por el Rector.
    Disponible en todos los templates como {{ global_theme_json }}.
    """
    try:
        theme = SystemThemeSettings.get_global_theme()
        if theme:
            import json
            return {'global_theme_json': json.dumps(theme)}
    except Exception:
        pass
    return {'global_theme_json': 'null'}
