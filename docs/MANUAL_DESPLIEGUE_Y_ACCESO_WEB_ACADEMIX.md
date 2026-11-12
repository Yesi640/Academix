# 🌐 MANUAL DE DESPLIEGUE, CONFIGURACIÓN Y ACCESO WEB DE ACADEMIX

**Sistema Integral de Gestión Académica, Control de Calificaciones, Asistencia y Auditoría Escolar**  
*Fecha de Puesta en Producción:* Octubre de 2026  
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

El sistema inicializa automáticamente las cuentas institucionales oficiales permanentes en el despliegue para garantizar la operatividad de todos los estamentos de la comunidad educativa:

| Rol en el Selector | Usuario / Identificación | ID Único Alumno *(si aplica)* | Contraseña | Alcance de Permisos |
| :--- | :--- | :--- | :--- | :--- |
| **👑 Superadministrador** | `admin` | *(No aplica)* | `Academix2026!` | Control total, base de datos, configuraciones globales y auditoría. |
| **🏛️ Rector / Directivo** | `rector` | *(No aplica)* | `Academix2026!` | Gestión pedagógica, directiva, asignaciones y reportes oficiales. |
| **📋 Secretaría Académica** | `nuryssecretaria` | *(No aplica)* | `123456789` | Admisiones, matrículas, certificados, expedientes y cartera. |
| **👨‍🏫 Docente Titular** | `docente` | *(No aplica)* | `Academix2026!` | Calificaciones, asistencia, tareas y observador de convivencia. |
| **🎓 Alumno** | `alumno` *(o ID)* | **`ALU-2026-1001`** | `Academix2026!` | Consulta de notas, boletín, entrega de tareas y asistencia. |
| **👨‍👩‍👧 Padre de Familia** | `padre` | **`ALU-2026-1001`** | `Academix2026!` | Seguimiento académico y disciplinario de su acudiente. |

> ⚠️ **Recomendación de Seguridad:** Una vez ingreses por primera vez, cada usuario puede modificar su contraseña desde su perfil institucional.

---

## 🛠️ 3. ARQUITECTURA DE DESPLIEGUE EN LA NUBE (RENDER)

### A. Archivos de Configuración del Servidor
* **`render.yaml`:** Manifiesto de infraestructura como código (IaC) para Render, definiendo el servicio web Python y la base de datos PostgreSQL.
* **`Procfile`:** Declaración de comando de arranque del servidor WSGI de producción:
  ```text
  web: gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
  ```
* **`build.sh`:** Script ejecutable de construcción automatizada ejecutado por Render en cada despliegue:
  ```bash
  #!/usr/bin/env bash
  set -o errexit
  pip install --upgrade pip
  pip install -r requirements.txt
  python manage.py collectstatic --noinput
  python manage.py migrate --noinput
  python manage.py setup_production_init
  ```

### B. Dependencias Críticas de Producción (`requirements.txt`)
* **Gunicorn (`gunicorn>=22.0.0`):** Servidor HTTP/WSGI para entornos Linux de alta concurrencia.
* **WhiteNoise (`whitenoise>=6.8.0`):** Motor de compresión y distribución estática (CSS, JavaScript, imágenes) directo sin requerir Nginx.
* **Soporte Cloud DB (`dj-database-url`, `psycopg2-binary`):** Permite conectar automáticamente bases de datos PostgreSQL mediante la variable `DATABASE_URL`.
* **Exportaciones e Informes (`openpyxl`, `qrcode`, `weasyprint`, `python-docx`):** Descarga de archivos Excel, códigos QR en boletines y documentos administrativos en la nube.

### C. Endurecimiento de Seguridad en Django (`config/settings.py`)
1. **Detección Automática de Dominios:**
   * Reconoce dominios de la nube como `academix-q2g4.onrender.com` e inyecta los orígenes de confianza CSRF requeridos por Django 5 (`CSRF_TRUSTED_ORIGINS`).
2. **Auditoría de Despliegue Superada (`check --deploy`):**
   * Redirección forzada a HTTPS (`SECURE_SSL_REDIRECT = True`).
   * Cookies de sesión y CSRF restringidas a canales encriptados (`SESSION_COOKIE_SECURE = True`, `CSRF_COOKIE_SECURE = True`).
   * Cabecera de protección para Reverse Proxy (`SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')`).
   * Activación de HSTS (`SECURE_HSTS_SECONDS = 31536000`), protección contra clickjacking (`X_FRAME_OPTIONS = 'DENY'`) y contra inyección de MIME types (`SECURE_CONTENT_TYPE_NOSNIFF = True`).

---

## 💾 4. PERSISTENCIA DE BASE DE DATOS Y VARIABLES DE ENTORNO

Para que los datos (usuarios, matrículas, notas) persistan de por vida y no se reinicien al suspenderse el servidor gratuito:

### Variables de Entorno en el Dashboard de Render:
| Variable | Valor Recomendado | Propósito |
| :--- | :--- | :--- |
| `DATABASE_URL` | `postgresql://user:pass@host:5432/dbname` | Conexión a PostgreSQL persistente en la nube (Neon.tech, Supabase o Render Postgres). |
| `USE_SQLITE_FALLBACK` | `False` | Desactiva el fallback de disco efímero local. |
| `SECRET_KEY` | *(Generado aleatoriamente)* | Clave criptográfica única de producción. |
| `DEBUG` | `False` | Modo estricto de seguridad en producción. |
| `EMAIL_BACKEND` | `django.core.mail.backends.smtp.EmailBackend` | Envío de credenciales por correo electrónico. |
| `EMAIL_HOST` | `smtp.gmail.com` | Servidor SMTP institucional. |
| `EMAIL_PORT` | `587` | Puerto TLS para correo. |
| `EMAIL_HOST_USER` | `academix651@gmail.com` | Cuenta de correo saliente. |
| `EMAIL_HOST_PASSWORD` | `uzgn axgt yxpf mvvv` | Clave de aplicación Google (16 caracteres). |

---

## 🔄 5. CÓMO PUBLICAR ACTUALIZACIONES EN EL FUTURO (CI/CD)

Render está vinculado a la rama `main` de GitHub. Cada vez que realices cambios o mejoras, solo ejecuta:

```bash
git add .
git commit -m "Descripción de la mejora o actualización"
git push origin main
```

Render detectará el cambio automáticamente, ejecutará `build.sh` (actualización de paquetes, estáticos, migraciones y sincronización de usuarios maestros) y desplegará la nueva versión en aproximadamente 2 minutos sin interrumpir el servicio.
