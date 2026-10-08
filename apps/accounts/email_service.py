"""
Servicio de notificaciones por correo electronico institucional para ACADEMIX.
Envia credenciales de acceso automaticamente cuando se registra un estudiante o docente.
"""
import logging
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

logger = logging.getLogger(__name__)


def send_registration_email(user, password, student_code=None, role_label=None):
    """
    Envia un correo electronico de bienvenida con credenciales oficiales de acceso.

    Args:
        user: Instancia de CustomUser registrado.
        password: Clave temporal asignada.
        student_code: Codigo o ID unico (en caso de estudiantes).
        role_label: Etiqueta de rol legible (ej. 'Estudiante', 'Docente').
    """
    if not user.email:
        logger.info(f"Registro de usuario {user.username} sin correo electronico. No se envia email.")
        return False

    # Correo real destino
    destinatario = user.email.strip()

    nombre_completo = user.get_full_name() or user.username
    rol = role_label or user.get_role_display()
    usuario = user.username
    id_registro = student_code if student_code else usuario

    asunto = f"📋 Credenciales de Acceso al Sistema - ACADEMIX ({nombre_completo})"

    texto_plano = f"""Bienvenido(a) {nombre_completo} al Sistema Institucional ACADEMIX.

Tu cuenta institucional ha sido registrada exitosamente con el rol de {rol}.

📋 Su número de registro / ID único: {id_registro}
👤 Su nombre de usuario: {usuario}
🔐 Su contraseña inicial: {password}

Enlace de acceso a la plataforma:
http://localhost:8000/

Recomendación de Seguridad:
Por motivos de privacidad, la plataforma le solicitará cambiar su contraseña en el primer inicio de sesión.

ACADEMIX - Sistema de Gestión y Control Académico Escolar
"""

    texto_html = f"""
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; max-width: 560px; margin: 0 auto; padding: 25px; border: 1px solid #e2e8f0; border-radius: 12px; background: #ffffff;">
        <div style="text-align: center; margin-bottom: 22px;">
            <div style="display: inline-block; background: #1e3a8a; color: #ffffff; font-weight: 900; font-size: 20px; width: 44px; height: 44px; line-height: 44px; border-radius: 8px; margin-bottom: 8px;">A</div>
            <h2 style="color: #1e3a8a; margin: 0; font-size: 22px; letter-spacing: 0.5px;">ACADEMIX</h2>
            <p style="color: #64748b; font-size: 13px; margin: 4px 0 0 0;">Sistema Integral de Gestión y Control Académico</p>
        </div>

        <div style="background: #f8fafc; border-left: 4px solid #2563eb; padding: 14px 18px; border-radius: 6px; margin-bottom: 22px;">
            <h3 style="color: #0f172a; margin: 0 0 6px 0; font-size: 15px;">¡Bienvenido(a), {nombre_completo}!</h3>
            <p style="color: #475569; font-size: 13.5px; margin: 0; line-height: 1.4;">
                Tu cuenta ha sido creada exitosamente con el rol de <strong>{rol}</strong>. A continuación encontrarás tus credenciales oficiales de acceso:
            </p>
        </div>

        <table style="width: 100%; border-collapse: collapse; margin-bottom: 22px; font-size: 13.5px;">
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: 700; color: #334155;">
                    📋 Su número de registro / ID único:
                </td>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-family: monospace; font-size: 14px; font-weight: 700; color: #2563eb;">
                    {id_registro}
                </td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: 700; color: #334155;">
                    👤 Su nombre de usuario:
                </td>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-family: monospace; font-size: 14px; font-weight: 700; color: #0f172a;">
                    {usuario}
                </td>
            </tr>
            <tr>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-weight: 700; color: #334155;">
                    🔐 Su contraseña inicial:
                </td>
                <td style="padding: 10px; border-bottom: 1px solid #e2e8f0; font-family: monospace; font-size: 14px; font-weight: 700; color: #0f172a;">
                    {password}
                </td>
            </tr>
        </table>

        <div style="text-align: center; margin: 25px 0;">
            <a href="http://localhost:8000/" style="background: #2563eb; color: #ffffff; padding: 12px 30px; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 14px; display: inline-block;">
                Ingresar a ACADEMIX
            </a>
        </div>

        <div style="border-top: 1px solid #e2e8f0; padding-top: 14px; margin-top: 20px; font-size: 11.5px; color: #94a3b8; text-align: center; line-height: 1.4;">
            <p style="margin: 0 0 4px 0;">Por motivos de seguridad institucional, se te solicitará cambiar esta contraseña en tu primer inicio de sesión.</p>
            <p style="margin: 0;">Si no solicitaste este registro, por favor ponte en contacto con la Rectoría o Secretaría Académica.</p>
        </div>
    </div>
    """

    # Remitente verificado en SMTP (Gmail requiere que coincida con el usuario autenticado)
    from_email = f"ACADEMIX <{settings.EMAIL_HOST_USER}>" if settings.EMAIL_HOST_USER else settings.DEFAULT_FROM_EMAIL

    try:
        msg = EmailMultiAlternatives(
            subject=asunto,
            body=texto_plano,
            from_email=from_email,
            to=[destinatario]
        )
        msg.attach_alternative(texto_html, "text/html")
        enviados = msg.send(fail_silently=False)
        logger.info(f"Correo de credenciales enviado exitosamente a {destinatario} (resultado={enviados}).")
        return True
    except Exception as e:
        logger.error(f"Fallo al enviar correo de credenciales a {destinatario}: {str(e)}")
        print(f"[EMAIL_ERROR] No se pudo enviar correo a {destinatario}: {e}")
        return False
