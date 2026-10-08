
"""
Servicio de notificaciones por correo electronico para ACADEMIX.
Envia credenciales de acceso automaticamente cuando se registra un alumno o docente.
"""
from django.core.mail import send_mail
from django.conf import settings


def send_registration_email(user, password, student_code=None, role_label=None):
    """
    Envia un correo de bienvenida con las credenciales de acceso.

    Args:
        user: instancia de CustomUser recien creado.
        password: contrasena en texto plano generada al registrar.
        student_code: ID unico del alumno (solo aplica para STUDENT).
        role_label: etiqueta legible del rol (ej. 'Estudiante', 'Docente').
    """
    if not user.email or '@academix.edu.co' in user.email:
        return  # No hay correo real, omitir

    nombre = user.get_full_name() or user.username
    rol = role_label or user.get_role_display()
    usuario = user.username

    if student_code:
        linea_id = f"Tu numero de registro / ID unico de Estudiante es: {student_code}"
    else:
        linea_id = f"Tu nombre de usuario para ingresar al sistema es: {usuario}"

    asunto = f"ACADEMIX - Bienvenido(a), {nombre}. Tus credenciales de acceso"

    cuerpo = f"""Hola {nombre},

Tu registro en el Sistema ACADEMIX ha sido completado exitosamente.

 Datos de Acceso:
-----------------------------------------
Rol asignado    : {rol}
{linea_id}
Usuario         : {usuario}
Contrasena      : {password}
-----------------------------------------

Por seguridad, el sistema te pedira cambiar tu contrasena en tu primer inicio de sesion.

Accede al sistema en: http://localhost:8000/

Si no solicitaste este registro o crees que es un error, por favor contacta a la secretaria academica.

ACADEMIX - Sistema Integral de Gestion Academica
"""

    try:
        send_mail(
            subject=asunto,
            message=cuerpo,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
    except Exception:
        pass
