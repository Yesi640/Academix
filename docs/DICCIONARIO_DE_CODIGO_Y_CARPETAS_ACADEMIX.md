# GUÍA MAESTRA DE CÓDIGO Y ESTRUCTURA DE CARPETAS — ACADEMIX
## Manual de Conocimiento Integral del Código Fuente para las 3 Integrantes
**Proyecto:** Plataforma de Gestión Escolar y Aprendizaje Adaptativo — ACADEMIX  
**Stack Principal:** Python 3.12 | Django 5.x | SQLite3 / PostgreSQL | HTML5, CSS3 Nativo & Vanilla JS  
**Propósito:** Que las 3 integrantes dominen exactamente qué hace cada archivo y carpeta para sustentar con total seguridad ante jurados e instructores.

---

## 🧭 1. El Flujo de Trabajo en Django (Patrón MVT)
Para entender cualquier código en Academix, deben tener presente cómo viaja una petición web en Django:

```
[ Navegador Web ] (Usuario hace clic o envía formulario)
       │
       ▼
 1. [ config/urls.py ] ──> Distribuye la URL a la aplicación correspondiente (apps/*/urls.py)
       │
       ▼
 2. [ views.py ] ────────> El Controlador / Lógica de Negocio:
       ├── Consulta o guarda datos usando [ models.py ] (ORM de Base de Datos)
       ├── Valida datos de entrada con [ forms.py ]
       └── Envía los datos procesados a la plantilla visual
       │
       ▼
 3. [ templates/*.html ] ─> La Vista Visual: Renderiza el diseño con HTML, CSS y JavaScript
       │
       ▼
[ Pantalla del Usuario ] (Respuesta final cargada en el navegador)
```

---

## 📂 2. Radiografía de las Carpetas Principales de la Raíz

| Carpeta / Archivo Raíz | ¿Qué es y cuál es su función exacta? |
| :--- | :--- |
| **`manage.py`** | **El ejecutor maestro de Django por consola.** A través de él se ejecutan los comandos del sistema: arrancar el servidor (`runserver`), crear migraciones (`makemigrations`), aplicarlas (`migrate`) y crear superusuarios (`createsuperuser`). |
| **`config/`** | **El cerebro y centro de configuración global del proyecto.** Contiene los ajustes que rigen a todas las aplicaciones. |
| **`apps/`** | **El corazón del código.** Contiene las 15 micro-aplicaciones modulares e independientes del sistema. |
| **`templates/`** | **Las vistas visuales (HTML).** Contiene todos los archivos de diseño que el usuario final ve e interactúa en pantalla. |
| **`static/` y `staticfiles/`** | **Archivos estáticos del diseño.** Hojas de estilo CSS (`style.css`), lógica de interfaz en JavaScript (`.js`), iconos, logotipos e imágenes estáticas del sistema. |
| **`media/`** | **Repositorio de archivos subidos por los usuarios.** Fotos de perfil, evidencias de tareas subidas por estudiantes en PDF/Word, adjuntos del observador. |
| **`docs/`** | **La biblioteca documental oficial.** Todos los manuales de entrega, técnicos, de usuario, APA 7, presentación interactiva y guías de roles. |
| **`scripts/`** | **Scripts de mantenimiento operativo.** Contiene utilidades como `backup_diario.bat` para realizar copias de seguridad de la base de datos automáticamente. |
| **`scratch/`** | **Scripts de apoyo y pruebas.** Utilidades puntuales para configuración de normas institucionales y categorías (`setup_categories_and_norms.py`). |
| **`db.sqlite3`** | **Base de datos relacional local de desarrollo.** Archivo que almacena todas las tablas, usuarios, notas y configuraciones del colegio en entorno local. |
| **`.env` / `.env.example`** | **Variables de entorno secretas.** Almacena claves criptográficas (`SECRET_KEY`), credenciales de base de datos y modo depuración (`DEBUG=True/False`). |
| **`requirements.txt`** | **Lista de dependencias y librerías Python.** Especifica las librerías necesarias para que el proyecto funcione (`Django`, `Pillow`, `python-dotenv`, `cryptography`, etc.). |
| **`Procfile` / `build.sh` / `render.yaml`** | **Archivos de despliegue en la nube.** Configuración para poner la plataforma en servidores como Render, Railway o VPS Linux. |

---

## ⚙️ 3. Carpeta `config/` (El Núcleo del Proyecto)

1. **`config/settings.py`**:
   - **¿Qué hace?:** Define qué aplicaciones están activas (`INSTALLED_APPS`), el motor de base de datos (`DATABASES`), los procesadores de contexto (`TEMPLATES`), la zona horaria (`TIME_ZONE = 'America/Bogota'`), el idioma español (`LANGUAGE_CODE = 'es-co'`), y las rutas de archivos multimedia y estáticos.
2. **`config/urls.py`**:
   - **¿Qué hace?:** El enrutador principal. Define los caminos base del sistema:
     - `/` $\rightarrow$ Redirige al login o al dashboard.
     - `/accounts/` $\rightarrow$ Envía a la app de usuarios.
     - `/courses/` $\rightarrow$ Envía a la gestión de cursos y grados.
     - `/grades/` $\rightarrow$ Envía a calificaciones y RAPs.
     - `/attendance/` $\rightarrow$ Envía a toma de asistencia.
     - `/admin/` $\rightarrow$ Panel interno administrativo de Django.
3. **`config/wsgi.py`**:
   - **¿Qué hace?:** *Web Server Gateway Interface*. Permite que servidores profesionales como **Gunicorn**, **Nginx** o Apache se comuniquen con el código Python en producción.

---

## 🧩 4. Estructura Estándar de Cualquier Aplicación en `apps/`
Cada una de las carpetas dentro de `apps/` sigue la misma estructura estandarizada:

- **`models.py` (La Base de Datos):** Define las tablas y columnas. Cada clase es una tabla (ej. `class Student(models.Model)`), y cada variable es una columna con su tipo (`CharField`, `IntegerField`, `ForeignKey`).
- **`views.py` (La Lógica / El Cerebro):** Recibe lo que el usuario pide desde la web, consulta o guarda en la base de datos, aplica validaciones y decide qué pantalla mostrar o qué respuesta enviar.
- **`urls.py` (Las Direcciones):** Conecta las direcciones web con las vistas de `views.py` (ej. `path('calificar/', views.calificar_view, name='calificar')`).
- **`forms.py` (Formularios y Validaciones):** Crea formularios seguros en HTML y valida que los datos ingresados no contengan código malicioso ni errores tipográficos.
- **`admin.py` (Administración de Django):** Registra los modelos para que el superadministrador pueda editarlos directamente desde `/admin/`.
- **`tests.py` (Pruebas Automatizadas):** Código que prueba automáticamente que las notas se calculen bien o que los usuarios inicien sesión sin fallos.
- **`migrations/` (Historial de BD):** Archivos que registran los cambios estructurales aplicados a la base de datos cada vez que se modifica un modelo.

---

## 🏢 5. Detalle de las 15 Micro-Aplicaciones en `apps/`

### 1. `apps/accounts/` (Usuarios, Perfiles y Roles)
- **Función:** Maneja el registro, inicio de sesión, cambio de clave y control de acceso.
- **Modelos clave:** `User` (usuario del sistema con email y rol), `Profile` (datos extendidos como foto de perfil, teléfono, cédula).
- **Lógica destacada:** El login adaptativo permite ingresar seleccionando el rol (Rector, Docente, Alumno, Acudiente, Secretaria) y la institución educativa activa.

### 2. `apps/courses/` (Jerarquía de Grados, Cursos y Aulas)
- **Función:** Estructura académica física y lógica del colegio.
- **Modelos clave:** `GradeLevel` (Grados: 6°, 7°, 8°...), `Course` (Cursos/Salones: 601, 702), `Section`, `InstitutionSetting` (Personalización de nombre, escudo y taxonomía del colegio).
- **Lógica destacada:** Motor de aprovisionamiento que crea aulas y salones de forma automática o manual.

### 3. `apps/subjects/` (Áreas y Asignaturas)
- **Función:** Plan de estudios y asignación académica docente.
- **Modelos clave:** `Area` (Matemáticas, Ciencias Naturales), `Subject` (Álgebra, Biología, Química), `AcademicAssignment` (vínculo que dice qué docente enseña qué materia en qué curso específico).
- **Lógica destacada:** Impide que dos docentes se solapen en la misma materia de un mismo salón.

### 4. `apps/grades/` (Calificaciones, Competencias y RAPs)
- **Función:** El motor de evaluación cuantitativo y cualitativo institucional.
- **Modelos clave:** `Competency` (Competencias por asignatura), `RAP` (Resultados de Aprendizaje Previstos), `Grade` (Nota final individual), `PeriodGradeSummary`.
- **Lógica destacada:** Validación estricta para que los RAPs de un periodo sumen exactamente el **100.00%** y escala de notas de **1.0 a 5.0** homologada al Decreto 1290 de 2009.

### 5. `apps/attendance/` (Asistencia Diaria y Novedades)
- **Función:** Registro ágil del llamado a lista en el aula de clase.
- **Modelos clave:** `AttendanceSession` (Sesión de clase en fecha y hora), `AttendanceRecord` (Estado individual del alumno: Presente, Falta Injustificada, Falta Justificada, Retardo), `AttendanceJustification` (Certificados médicos o notas de acudientes).
- **Lógica destacada:** Vista rápida que carga la lista de estudiantes del salón y permite guardar la asistencia de todo el curso con un solo clic.

### 6. `apps/discipline/` (Observador del Estudiante)
- **Función:** Bitácora disciplinaria y convivencial del alumno.
- **Modelos clave:** `DisciplinaryIncident` (Reporte de la falta, fecha y descripción), `DisciplinaryCategory` (Falta Leve, Grave, Gravísima), `DisciplinaryCommitment` (Compromisos firmados por alumno y acudiente).
- **Lógica destacada:** Notificaciones automáticas de alertas disciplinarias y seguimiento al debido proceso escolar.

### 7. `apps/homework/` (Gestión de Tareas y Evidencias)
- **Función:** Aula virtual de actividades y entregas escolares.
- **Modelos clave:** `Homework` (Tarea creada por el docente con instrucciones, fecha límite y adjuntos), `HomeworkSubmission` (Entrega subida por el estudiante con archivo y comentarios), `HomeworkFeedback` (Calificación y retroalimentación del docente).
- **Lógica destacada:** Bloqueo automático de entregas vencidas según la fecha límite configurada.

### 8. `apps/students/` (Expediente del Estudiante)
- **Función:** Hoja de vida académica y matrícula del aprendiz.
- **Modelos clave:** `Student` (Expediente con código único `EST-XXXX`, tipo de documento, acudiente vinculado, información médica y curso matriculado).
- **Lógica destacada:** Generación automática de IDs únicos institucionales para evitar cédulas duplicadas.

### 9. `apps/teachers/` (Directorio Docente)
- **Función:** Gestión del talento humano pedagógico.
- **Modelos clave:** `Teacher` (Perfil profesional del docente, especialidad, escalafón, asignación horaria y dirección de grupo).

### 10. `apps/periods/` (Periodos Académicos y Años Lectivos)
- **Función:** Control de calendarios escolares.
- **Modelos clave:** `AcademicYear` (Año escolar ej. 2026), `AcademicPeriod` (1er Periodo, 2do Periodo, fechas de apertura y cierre de digitación de notas).
- **Lógica destacada:** Bloquea la edición de notas si el periodo ya fue cerrado por Rectoría.

### 11. `apps/reports/` (Boletines Oficiales y Reportes)
- **Función:** Motor de generación de informes para impresión y entrega de notas.
- **Lógica destacada:** Generación dinámica de boletines académicos consolidados en PDF (`boletin_pdf.html`) con promedios, puestos y firmas digitales.

### 12. `apps/alerts/` (Sistema de Alertas Tempranas)
- **Función:** Detección automática de estudiantes en riesgo de reprobación por bajo rendimiento acumulado o exceso de inasistencias.

### 13. `apps/audit/` (Registro de Auditoría y Trazabilidad)
- **Función:** Bitácora inmutable que guarda: quién modificó una nota, a qué hora, desde qué dirección IP y cuál era el valor anterior.

### 14. `apps/rules/` (Manual de Convivencia)
- **Función:** Catálogo tipificado de normas, deberes, derechos y procedimientos formativos de la institución educativa.

### 15. `apps/finance/` (Tesorería Institucional)
- **Función:** Control básico de pensiones, matrículas escolares y estado de paz y salvo del estudiante.

---

## 🎨 6. Carpeta `templates/` (La Capa Visual)

La carpeta `templates/` sigue la misma estructura modular de `apps/`:

- **`templates/base.html`**:
  - **La plantilla maestra.** Contiene la barra superior (Navbar), el menú lateral colapsable (Sidebar), la importación de tipografías (`Outfit`, `Plus Jakarta Sans`), iconos (`Lucide`) y estilos CSS globales. Las demás pantallas heredan de este archivo usando `{% extends 'base.html' %}`.
- **`templates/accounts/`**: Formularios de inicio de sesión (`login.html`), perfil de usuario y cambio de contraseña.
- **`templates/grades/`**: Planilla transaccional interactiva de notas (`grade_entry.html`), gestión de RAPs y ponderaciones.
- **`templates/attendance/`**: Pantalla de llamado a lista con botones rápidos para marcar asistencias (`take_attendance.html`).
- **`templates/reports/`**: Diseño oficial del boletín escolar en PDF (`boletin_pdf.html`).
- **`templates/homework/`**: Bandeja de tareas del docente y formulario de subida de evidencias del alumno.
- **`templates/partials/`**: Fragmentos HTML reutilizables (tablas, modales, alertas y spinners de carga).

---

## 🛠️ 7. Scripts Raíz de Soporte y Despliegue

- **`iniciar_servidor_red.bat` y `iniciar_servidor_red.py`**:
  - Detecta automáticamente la dirección IP local de la computadora (ej. `192.168.1.15`) y arranca el servidor escuchando en el puerto `8000` para que cualquier dispositivo en la red Wi-Fi o cableada del colegio pueda conectarse sin configuraciones complejas.
- **`seed_mallas_rap.py`**:
  - Script que puebla automáticamente la base de datos con las áreas, asignaturas, competencias y RAPs estándar de básica y media, asegurando que sumen el 100% de ponderación para pruebas inmediatas.
- **`scripts/backup_diario.bat`**:
  - Script por lotes de Windows para automatizar copias de seguridad de la base de datos con marca de tiempo (cumpliendo con la regla 3-2-1).
- **`firewall.bat`**:
  - Configura las reglas del Firewall de Windows para abrir el puerto 8000 de forma segura en la red del colegio.

---

## 🎓 8. ¿Quién debe defender cada parte del código ante el SENA?

### 👤 INTEGRANTE 1 — Dominio de la Experiencia de Usuario y Flujos Funcionales
- **Carpetas asignadas:**
  - `templates/` (Especialmente `base.html`, `grades/`, `attendance/`, `discipline/`).
  - `apps/attendance/` y `apps/discipline/` (Flujo de vida escolar diario).
  - `apps/homework/` (Interacción estudiante-profesor).
- **Defensa clave:** *"Yo domino cómo la interfaz se comunica con el usuario. Las vistas renderizan datos con Bootstrap/CSS sin sobrecargar el navegador, facilitando que un profesor califique o tome lista en menos de un minuto."*

### ⚙️ INTEGRANTE 2 — Dominio de la Lógica, Base de Datos y Seguridad
- **Carpetas asignadas:**
  - `config/settings.py` y `config/urls.py` (Enrutamiento y middlewares).
  - `apps/grades/models.py` y `apps/grades/views.py` (Cálculo matemático de RAPs y notas 1.0 a 5.0).
  - `apps/courses/` y `apps/subjects/` (Modelo relacional 3FN).
  - `apps/audit/` y `apps/accounts/` (Seguridad RBAC, autenticación y hashing de contraseñas).
- **Defensa clave:** *"Yo domino el backend en Django y el ORM. Los modelos respetan la 3FN, evitamos el problema de consultas N+1 con prefetch, y aplicamos validaciones en models.py y views.py para blindar la consistencia de los datos."*

### 🚀 INTEGRANTE 3 — Dominio de la Infraestructura, Scripts, Roles y Despliegue
- **Carpetas asignadas:**
  - `manage.py`, `config/wsgi.py`, `Procfile`, `build.sh`.
  - `iniciar_servidor_red.bat` y `iniciar_servidor_red.py` (Conectividad en red local).
  - `scripts/backup_diario.bat` y `firewall.bat` (Seguridad perimetral y respaldos).
  - `apps/students/` y `apps/teachers/` (Aprovisionamiento y matrículas del manual de roles).
- **Defensa clave:** *"Yo domino la puesta en marcha, infraestructura de red y aprovisionamiento. Conozco cómo se configuran las IPs, cómo se protegen las terminales con VLANs y scripts, y el orden exacto de creación de usuarios para evitar fallos de integridad."*

---

## 📖 9. Glosario Técnico Rápido para Responder Preguntas del Jurado

- **¿Qué es el ORM?** *(Object-Relational Mapping):* Es la herramienta de Django que traduce código Python a sentencias SQL automáticamente, evitando tener que escribir `SELECT` o `INSERT` manuales y protegiendo contra inyecciones SQL.
- **¿Qué es una Migración?** Es un archivo que registra cómo evoluciona la base de datos (por ejemplo, cuando se añade un campo nuevo a un modelo) y lo sincroniza con la base de datos real (`python manage.py migrate`).
- **¿Qué es un Context Processor?** Es una función que inyecta variables globales a todas las plantillas HTML (como el nombre y escudo de la institución activa en Academix).
- **¿Qué es RBAC?** *(Role-Based Access Control):* Control de acceso basado en roles. Garantiza que un estudiante no pueda ver las pantallas de secretaría ni un profesor modificar cursos ajenos.
- **¿Qué es CSRF Token?** *(Cross-Site Request Forgery):* Un código de seguridad invisible que Django coloca en cada formulario para certificar que la petición proviene de un usuario legítimo y no de un atacante externo.
