# 🌐 MANUAL DE DESPLIEGUE, CONFIGURACIÓN Y ACCESO WEB DE ACADEMIX

**Sistema Integral de Gestión Académica, Control de Calificaciones, Asistencia y Auditoría Escolar**  
*Fecha de Puesta en Producción:* 16 de Octubre de 2026  
*Estado de la Plataforma:* **🟢 OPERATIVO Y EN LÍNEA (LIVE)**

---

## 📌 1. DATOS DE ACCESO AL SISTEMA EN PRODUCCIÓN

La plataforma se encuentra completamente desplegada en internet, accesible desde cualquier computadora, teléfono inteligente o tablet con conexión a la red:

* **Enlace Público Oficial:** [https://academix-q2g4.onrender.com](https://academix-q2g4.onrender.com)
* **Página de Inicio de Sesión (Login):** [https://academix-q2g4.onrender.com/accounts/login/](https://academix-q2g4.onrender.com/accounts/login/)
* **Página de Registro Institucional:** [https://academix-q2g4.onrender.com/accounts/register/](https://academix-q2g4.onrender.com/accounts/register/)
* **Panel de Superadministración Django:** [https://academix-q2g4.onrender.com/admin/](https://academix-q2g4.onrender.com/admin/)
* **Repositorio de Código Fuente (GitHub):** [https://github.com/Yesi640/Academix.git](https://github.com/Yesi640/Academix.git)

---

## 🔑 2. CREDENCIALES DE ACCESO MAESTRO INICIAL

El sistema inicializa automáticamente los usuarios de alta dirección en el arranque para garantizar que puedas gestionar de inmediato la institución:

| Rol Institucional | Nombre de Usuario | Contraseña Inicial | Alcance de Permisos |
| :--- | :--- | :--- | :--- |
| **Superadministrador** | `admin` | `Academix2026!` | Acceso total al sistema, auditoría, base de datos y configuraciones globales. |
| **Rector(a) Institucional** | `rector` | `Academix2026!` | Gestión pedagógica, asignación docente, observación disciplinaria y reportes oficiales. |

> ⚠️ **Recomendación de Seguridad:** Una vez ingreses por primera vez, puedes modificar tu contraseña desde el menú de perfil de usuario para mayor privacidad.

---

## 🛠️ 3. RESUMEN DE MODIFICACIONES Y BLINDAJE TÉCNICO REALIZADO

Para que ACADEMIX pasara de ser un proyecto de desarrollo local a una aplicación web profesional de grado corporativo, se realizaron las siguientes adaptaciones:

### A. Dependencias y Servidores de Producción (`requirements.txt`)
* **Gunicorn (`gunicorn>=22.0.0`):** Servidor HTTP/WSGI para entornos Linux de alta concurrencia.
* **WhiteNoise (`whitenoise>=6.8.0`):** Motor de compresión y distribución estática (CSS, JavaScript, imágenes) directo sin requerir Nginx.
* **Soporte Cloud DB (`dj-database-url`, `psycopg2-binary`):** Permite conectar automáticamente bases de datos PostgreSQL o MySQL mediante la variable `DATABASE_URL`.
* **Exportaciones e Informes (`openpyxl`, `qrcode`, `weasyprint`, `python-docx`):** Garantiza que la descarga de archivos Excel, códigos QR en boletines y documentos administrativos funcionen en la nube.

### B. Endurecimiento de Seguridad en Django (`config/settings.py`)
1. **Detección Automática de Dominios:**
   * Reconoce automáticamente dominios de la nube como `academix-q2g4.onrender.com` e inyecta los orígenes de confianza CSRF requeridos por Django 5.
2. **Auditoría de Despliegue Superada (`check --deploy`):**
   * Configuración de redirección forzada a HTTPS (`SECURE_SSL_REDIRECT = True`).
   * Cookies de sesión y CSRF restringidas a canales encriptados (`SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True`).
   * Cabecera de protección para Reverse Proxy (`SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')`) para evitar bucles de redirección.
   * Activación de HSTS (`SECURE_HSTS_SECONDS = 31536000`), protección contra clickjacking (`X_FRAME_OPTIONS = 'DENY'`) y contra inyección de MIME types (`SECURE_CONTENT_TYPE_NOSNIFF = True`).
3. **Almacenamiento Estático de Django 5 (`STORAGES`):**
   * Migración al nuevo estándar `STORAGES` con almacenamiento comprimido de WhiteNoise.

### C. Automatización de Construcción y Arranque
* **`Procfile`:** Instrucción que indica a la nube cómo arrancar el servicio web:
  `web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT`
* **`build.sh`:** Script que ejecuta 5 pasos obligatorios en cada despliegue:
  1. Actualización de pip.
  2. Instalación de paquetes de producción.
  3. Recopilación de estáticos (`collectstatic --noinput`).
  4. Ejecución de migraciones de base de datos (`migrate`).
  5. Inicialización de datos maestros (`setup_production_init`).
* **`setup_production_init.py`:** Comando que crea el usuario Administrador, Rector, verifica los grados de Transición a 11°, crea el Año Lectivo 2026-2027 y los 4 periodos académicos.

### D. Corrección Integral de Pruebas Unitarias
* Se corrigió la enumeración de auditoría en los módulos de Convivencia Escolar (`apps.discipline`) y Cartera (`apps.finance`).
* Se reactivó la validación estricta de inmutabilidad en Tareas y Calificaciones (`apps.homework`).
* **Resultado:** 100% de las pruebas aprobadas (`OK`).

---

## 🔄 4. CÓMO ACTUALIZAR EL SITIO EN EL FUTURO

Render está configurado con **Integración Continua (CI/CD)** conectada a tu rama `main` de GitHub. Para publicar cualquier cambio futuro, solo debes hacer:

```bash
git add .
git commit -m "Descripción de tu nueva mejora"
git push origin main
```
Render detectará el cambio de forma automática, ejecutará `build.sh` y actualizará tu web en 2 minutos sin interrumpir el servicio.

---

*Desarrollado y preparado con los más altos estándares de calidad pedagógica y seguridad por el equipo ACADEMIX.*
