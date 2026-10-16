from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .services import get_active_alerts_for_user
from .models import SystemAlert

@login_required
def active_alerts_partial(request):
    """
    Retorna el fragmento HTML con las alertas activas del usuario (para consumo HTMX).
    """
    alerts = get_active_alerts_for_user(request.user)
    return render(request, 'alerts/partials/alert_list.html', {'alerts': alerts})

@login_required
def dismiss_alert(request, alert_id):
    """
    Descarta una alerta permitida para el usuario actual.
    """
    alert = get_object_or_404(SystemAlert, id=alert_id, is_active=True)
    if alert.is_dismissible and alert.level != SystemAlert.Level.BLOCK:
        alert.is_active = False
        alert.save(update_fields=['is_active'])

    # Retorna lista actualizada
    alerts = get_active_alerts_for_user(request.user)
    return render(request, 'alerts/partials/alert_list.html', {'alerts': alerts})

@login_required
def activities_list_view(request):
    """
    Agenda de actividades institucionales del colegio.
    Permite a Directivos y Secretaría programar eventos y notificar a los alumnos.
    """
    from .models import InstitutionalActivity
    from .services import schedule_institutional_activity
    from django.contrib import messages
    from datetime import date

    if request.method == 'POST' and (request.user.is_admin_role or request.user.is_rector or request.user.is_secretary):
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        event_date_str = request.POST.get('event_date')
        event_time_str = request.POST.get('event_time')
        location = request.POST.get('location', '').strip() or 'Instalaciones del Colegio'
        target_audience = request.POST.get('target_audience', 'ALL')

        if title and event_date_str:
            try:
                from datetime import datetime
                event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
                event_time = datetime.strptime(event_time_str, '%H:%M').time() if event_time_str else None

                activity = schedule_institutional_activity(
                    title=title,
                    description=description,
                    event_date=event_date,
                    event_time=event_time,
                    location=location,
                    target_audience=target_audience,
                    created_by=request.user
                )
                messages.success(request, f'Actividad "{title}" programada y notificada a los estudiantes con éxito.')
            except Exception as e:
                messages.error(request, f'Error al programar actividad: {str(e)}')
        else:
            messages.warning(request, 'Por favor ingrese el título y la fecha de la actividad.')

    # Listar actividades vigentes
    activities = InstitutionalActivity.objects.filter(is_active=True).order_by('event_date', 'event_time')
    
    # Filtrar según audiencia si es estudiante
    if request.user.is_student:
        activities = activities.filter(target_audience__in=['ALL', 'STUDENTS'])
    elif request.user.is_teacher:
        activities = activities.filter(target_audience__in=['ALL', 'TEACHERS'])
    elif request.user.is_parent:
        activities = activities.filter(target_audience__in=['ALL', 'PARENTS'])

    context = {
        'activities': activities,
        'today': date.today(),
        'can_schedule': request.user.is_admin_role or request.user.is_rector or request.user.is_secretary,
    }
    return render(request, 'alerts/activities_list.html', context)


@login_required
def alerts_management_view(request):
    """
    Panel de Control y Emisión de Semáforos y Alertas Institucionales.
    Permite al Administrador y Rector emitir avisos (🔴 Bloqueo, 🟡 Advertencia, 🔵 Informativo),
    ver las alertas del sistema y desactivar alertas vigentes.
    """
    from django.contrib import messages
    if not (request.user.is_admin_role or request.user.is_rector):
        messages.error(request, 'No tiene permisos para administrar las alertas del sistema.')
        return redirect('dashboard')

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'create':
            title = request.POST.get('title', '').strip()
            message = request.POST.get('message', '').strip()
            level = request.POST.get('level', SystemAlert.Level.INFO)
            target_role = request.POST.get('target_role', '').strip()
            if target_role == 'ALL':
                target_role = ''
            is_dismissible = request.POST.get('is_dismissible') == '1'

            if title and message:
                SystemAlert.objects.create(
                    title=title,
                    message=message,
                    level=level,
                    target_role=target_role or None,
                    is_dismissible=is_dismissible,
                    is_active=True
                )
                messages.success(request, f'Alerta institucional "{title}" emitida exitosamente.')
            else:
                messages.warning(request, 'El título y el mensaje son obligatorios.')
        elif action == 'toggle_active':
            alert_id = request.POST.get('alert_id')
            try:
                alert_obj = SystemAlert.objects.get(id=alert_id)
                alert_obj.is_active = not alert_obj.is_active
                alert_obj.save(update_fields=['is_active'])
                st = "reactivada" if alert_obj.is_active else "desactivada"
                messages.success(request, f'Alerta {st} correctamente.')
            except SystemAlert.DoesNotExist:
                messages.error(request, 'Alerta no encontrada.')
        return redirect('alerts:management')

    alerts_list = SystemAlert.objects.all().order_by('-created_at')[:100]
    context = {
        'alerts_list': alerts_list,
        'levels': SystemAlert.Level.choices,
        'roles': [
            ('ALL', 'Todos los Usuarios (Institucional)'),
            ('TEACHER', 'Docentes'),
            ('STUDENT', 'Estudiantes'),
            ('PARENT', 'Padres de Familia / Acudientes'),
            ('SECRETARIA', 'Secretaría Académica'),
            ('RECTOR', 'Directivos / Rectoría'),
        ]
    }
    return render(request, 'alerts/management.html', context)


