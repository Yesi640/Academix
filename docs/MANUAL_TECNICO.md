# 📘 MANUAL TÉCNICO FINAL DEL SISTEMA ACADEMIX
**Plataforma Integral de Gestión Académica, Control Escolar, Asistencia y Auditoría Institucional**  
*Versión: 2.5.0 | Framework: Django 5.x / Python 3.10+ | Entorno: Producción Cloud (Render / PostgreSQL)*

---

## 1. INTRODUCCIÓN Y ARQUITECTURA GENERAL

### 1.1 Propósito y Alcance del Software
**ACADEMIX** es una plataforma web integral de gestión académica y control administrativo escolar diseñada bajo el patrón de arquitectura **Multi-Sede (Multi-School SaaS)** y **Multi-Modelo Adaptativo**. El sistema centraliza la administración curricular, inscripciones, matrículas, asignación académica docente, registro de calificaciones por periodos bimestrales, control biométrico/asistencia, seguimiento convivencial (Observador del Alumno), gestión de tesorería/cartera y generación de boletines oficiales con código QR de verificación.

### 1.2 Diagrama Arquitectónico del Sistema

```text
               [ NAVEGADOR WEB / CLIENTE (Desktop / Móvil) ]
                                    │
                                    ▼ (HTTPS / TLS 1.3)
                  [ REVERSE PROXY / BALANCEADOR CLOUD ]
                                    │
                         (Cabecera X-Forwarded-Proto)
                                    ▼
                 [ SERVIDOR WSGI GUNICORN (Linux Container) ]
                                    │
           ┌────────────────────────┴────────────────────────┐
           ▼                                                 ▼
[ WHITENOISE STORAGE ]                             [ PIPELINE DJANGO 5.x ]
(Archivos CSS, JS, Fuentes, SVG)                   ├── Middlewares (Security, CSRF, Session)
                                                   ├── Context Processors (Institución, Sede)
                                                   ├── Motor de Enrutamiento (URLs Apps)
                                                   └── Vistas Basadas en Funciones y Clases
                                                             │
                                                             ▼
                                                [ MOTOR ORM DE DJANGO ]
                                                             │
                                        ┌────────────────────┴────────────────────┐
                                        ▼                                         ▼
                            [ POSTGRESQL EN LA NUBE ]                     [ SQLITE CON WAL ]
                            (DATABASE_URL - Producción)                   (Desarrollo Local / Fallback)
```

---

## 2. STACK TECNOLÓGICO Y ESPECIFICACIONES TÉCNICAS

| Capa del Sistema | Tecnología Utilizada | Versión Mínima | Propósito en el Proyecto |
| :--- | :--- | :--- | :--- |
| **Lenguaje Backend** | Python | 3.10.x / 3.11.x / 3.12.x | Lógica central del sistema, servicios y scripts. |
| **Framework Web** | Django | 5.0.x / 5.1.x | Arquitectura MVT, ORM, autenticación y seguridad. |
| **Servidor WSGI** | Gunicorn | >= 22.0.0 | Servidor de producción para peticiones HTTP concurrentes. |
| **Motor de Base de Datos** | PostgreSQL / SQLite 3 | Postgres 15+ / SQLite 3.35+ | Almacenamiento relacional transaccional ACID (`ATOMIC_REQUESTS = True`). |
| **Conector de BD** | `dj-database-url`, `psycopg2-binary` | >= 2.2.0 / >= 2.9.9 | Enlace dinámico mediante cadenas `DATABASE_URL`. |
| **Servidor de Estáticos** | WhiteNoise | >= 6.8.0 | Compresión Gzip/Brotli y entrega eficiente de estáticos. |
| **Frontend & UI** | HTML5, Vanilla CSS3, JavaScript | ES6+ / Bootstrap 5.3 Icons | Interfaz moderna, glassmorphism, responsive sin Tailwind. |
| **Generación de Informes** | `openpyxl`, `qrcode`, `python-docx` | Versiones LTS | Exportación de Excel, códigos QR para boletines y Word. |

---

## 3. ESTRUCTURA MODULAR DEL CÓDIGO FUENTE

El sistema está organizado bajo un enfoque modular desacoplado en el directorio `apps/`:

```text
Academix/
├── apps/
│   ├── accounts/       # Autenticación, modelo CustomUser, Escuelas (School), roles y permisos
│   ├── alerts/         # Alertas tempranas de deserción y rendimiento académico
│   ├── attendance/     # Registro diario de asistencia, justificaciones y novedades
│   ├── audit/          # Registro inmutable de auditoría (AuditLog) para trazabilidad legal
│   ├── courses/        # Años lectivos, Grados escolares (Transición a 11°), Secciones y Cursos
│   ├── discipline/     # Observador del Estudiante, tipificación de faltas y acuerdos convivenciales
│   ├── finance/        # Cartera escolar, conceptos de cobro, obligaciones y pagos de pensión
│   ├── grades/         # Criterios de evaluación (SABER, HACER, SER), notas bimestrales y cierres
│   ├── homework/       # Asignación de tareas, entregas de estudiantes y retroalimentación docente
│   ├── periods/        # Periodos académicos (4 bimestres reglamentarios al 25% c/u)
│   ├── reports/        # Emisión de boletines oficiales, sábana de notas y cuadro de honor
│   ├── rules/          # Escalas de valoración nacional (MEN) y reglas de promoción
│   ├── students/       # Expediente del alumno (StudentProfile), matrículas (Enrollment) y legajo
│   ├── subjects/       # Áreas fundamentales de conocimiento (KnowledgeArea) y asignaturas (Subject)
│   └── teachers/       # Ficha del docente (TeacherProfile) y asignación académica (TeachingAssignment)
├── config/             # settings.py, urls.py, wsgi.py, asgi.py
├── static/             # Hojas de estilo CSS personalizadas, scripts JS e iconografía
├── templates/          # Plantillas HTML semánticas con herencia modular (base.html)
├── build.sh            # Script de construcción y despliegue continuo en la nube
├── Procfile            # Instrucción de arranque Gunicorn para Render/Railway
├── render.yaml         # Infraestructura como Código (IaC) para la nube
└── requirements.txt    # Manifiesto de dependencias de producción
```

---

## 4. MODELO DE DATOS Y ENTIDADES PRINCIPALES

### 4.1 Entidad de Usuarios y Roles (`apps.accounts.models.CustomUser`)
Hereda de `AbstractUser` de Django e implementa 6 roles institucionales canónicos:
* `ADMIN` (Superadministrador del sistema y de la plataforma)
* `RECTOR` (Rector / Rectora Institucional)
* `SECRETARIA` (Secretaría Académica y Admisiones)
* `TEACHER` (Docente Titular / de Área)
* `STUDENT` (Estudiante / Alumno matriculado)
* `PARENT` (Padre de Familia / Acudiente legal)

Campos destacados:
* `document_type`: CC, TI, CE, PEP, PASSPORT.
* `document_number`: Identificación única con índice en base de datos (`db_index=True`).
* `school`: Clave foránea a `School` (soporte multi-institución).
* `must_change_password`: Bandera booleana para forzar cambio de clave temporal.

### 4.2 Expediente Estudiantil (`apps.students.models.StudentProfile`)
* `user`: Relación uno a uno (`OneToOneField`) con `CustomUser`.
* `student_code`: Código único de matrícula institucional (ej. `ALU-2026-1001`).
* `parent`: Clave foránea al usuario padre/acudiente (`CustomUser` con rol `PARENT`).
* `blood_type`, `eps`, `medical_notes`: Ficha médica y antecedentes.

### 4.3 Matrícula Escolar (`apps.students.models.Enrollment`)
* Vincula al `StudentProfile` con un `CourseSection` en un `AcademicYear`.
* Estado de matrícula (`Status`): `ACTIVE`, `PENDING`, `TRANSFERRED`, `WITHDRAWN`, `PROMOTED`.
* Estado financiero: `PAZ_Y_SALVO`, `PENDIENTE`, `MORA`.

### 4.4 Asignación Académica (`apps.teachers.models.TeachingAssignment`)
* Relación ternaria entre `TeacherProfile`, `CourseSection` y `Subject` en un `AcademicYear`.
* Bandera `is_group_director`: Identifica al docente director de grupo.

### 4.5 Calificaciones y Periodos (`apps.grades.models.Grade`)
* Estructurada con base en las 3 dimensiones pedagógicas:
  * **SABER (Cognitiva):** Evaluaciones, quices, sustentaciones.
  * **HACER (Procedimental):** Talleres, tareas, proyectos de aula.
  * **SER (Actitudinal):** Convivencia, puntualidad, ética y valores.
* Vinculada a los 4 periodos académicos anuales ponderados al 25% cada uno.

---

## 5. POLÍTICAS DE SEGURIDAD Y ENDURECIMIENTO (HARDENING)

1. **Aislamiento Multi-Tenant:**
   * Las consultas de estudiantes, grupos, materias y notas están acotadas a la sede escolar (`School`) activa del usuario autenticado.
2. **Protección de Sesión y Cookies:**
   * `SESSION_COOKIE_SECURE = True` y `CSRF_COOKIE_SECURE = True`: Las cookies de navegación solo viajan por canales cifrados HTTPS.
   * `SESSION_COOKIE_HTTPONLY = True`: Impide el acceso a cookies de sesión desde JavaScript (mitigación XSS).
3. **Encabezados HTTP de Seguridad:**
   * `X_FRAME_OPTIONS = 'DENY'`: Bloquea ataques de Clickjacking.
   * `SECURE_CONTENT_TYPE_NOSNIFF = True`: Impide ataques MIME sniffing.
   * `SECURE_HSTS_SECONDS = 31536000`: Forzado estricto de HTTPS por 1 año.
4. **Trazabilidad Inmutable (Auditoría Legal):**
   * Cada acción de login, cambio de notas, retiro de estudiantes y cobro registra en `AuditLog`: Usuario, IP, fecha/hora, acción (`INSERT`, `UPDATE`, `DELETE`) y valores anteriores/nuevos en formato JSON.

---

## 6. COMANDOS DE GESTIÓN Y MANTENIMIENTO CLI

```bash
# 1. Ejecutar verificación de integridad del sistema
python manage.py check --deploy

# 2. Aplicar migraciones pendientes
python manage.py migrate

# 3. Inicializar / Reparar usuarios oficiales y datos maestros de producción
python manage.py setup_production_init

# 4. Crear un respaldo de la base de datos local (Windows)
scripts\backup_diario.bat
```
