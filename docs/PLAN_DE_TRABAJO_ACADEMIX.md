# PLAN DE TRABAJO DEL PROYECTO ACADEMIX
## De acuerdo con la Interpretación del Informe Técnico de Diseño, según Normas y Protocolos de la Empresa

---

**Código del Documento:** PT-ACX-2026-V1  
**Proyecto:** ACADEMIX — Sistema Integral de Gestión Académica, Calificaciones, Asistencia y Auditoría Escolar  
**Organización / Entorno:** Institución Educativa de Educación Básica y Media / Centro de Formación SENA (ADSO / ADSI)  
**Marco Legal y Normativo:** Ley 115 de 1994 (Ley General de Educación), Decreto 1290 de 2009 (Evaluación del Aprendizaje y Promoción Escolar), Ley 1581 de 2012 (Habeas Data / Protección de Datos Personales), Estándar ISO/IEC 25010 (Calidad del Producto de Software)  
**Metodología de Desarrollo:** Marco Ágil Scrum (Desarrollo Incremental e Iterativo en 5 Sprints)  
**Versión del Sistema:** 1.0.0 Release Candidate — Modo Red Local Institucional (LAN / Wi-Fi) y Cloud-Ready  
**Fecha de Elaboración:** Septiembre de 2026  
**Estado:** Ejecutado y Validado al 100%  

---

## 1. INTRODUCCIÓN Y ALCANCE

El presente **Plan de Trabajo** formaliza la planificación, ejecución y cierre del proyecto de desarrollo de software **ACADEMIX**, formulado en estricto cumplimiento con la interpretación técnica del informe de diseño, los requerimientos funcionales y no funcionales del sector educativo colombiano, y las normas y protocolos de calidad de la industria de software.

ACADEMIX ha sido concebido como una plataforma web monolítica modular de alto rendimiento, diseñada para operar tanto en infraestructura de red de área local (LAN/Wi-Fi) institucional —permitiendo la conexión concurrente de computadoras de directivos, docentes, secretaría y dispositivos móviles sin depender de un enlace a Internet externo— como en servidores en la nube centralizados.

El plan articula las 13 aplicaciones modulares construidas, la arquitectura de base de datos relacional con concurrencia optimizada, el motor de reglas pedagógicas fundamentado en el Decreto 1290 de 2009, el subsistema de auditoría inmutable, la seguridad perimetral y el protocolo de despliegue operativo.

---

## 2. INTERPRETACIÓN DEL INFORME TÉCNICO DE DISEÑO

El análisis del informe técnico de diseño condujo a las siguientes decisiones arquitectónicas, tecnológicas y estructurales consolidadas en el proyecto:

### 2.1. Arquitectura de Software y Patrón Estructural
* **Patrón Arquitectónico:** MVT (Model - View - Template) nativo sobre **Django 5.x**, complementado con una capa de servicios desacoplados (`services.py`) en las aplicaciones críticas para concentrar la lógica pura del negocio fuera de los controladores/vistas.
* **Modularidad por Dominios:** Descomposición del sistema en 13 aplicaciones independientes agrupadas bajo el directorio `apps/`, garantizando bajo acoplamiento y alta cohesión:
  1. `apps.accounts`: Gestión de identidades, perfiles y control de acceso basado en roles (RBAC).
  2. `apps.audit`: Trazabilidad inmutable de eventos, modificaciones y deltas de auditoría.
  3. `apps.alerts`: Motor reactivo de semaforización y alertas preventivas/bloqueantes.
  4. `apps.courses`: Gestión de estructura escolar (Años lectivos, Grados y Cursos/Secciones).
  5. `apps.subjects`: Malla curricular (Áreas de conocimiento, Asignaturas e Intensidades).
  6. `apps.periods`: Periodos académicos lectivos (1 a 4), ponderaciones y estados.
  7. `apps.teachers`: Ficha profesional docente y asignación académica única.
  8. `apps.students`: Expedientes estudiantiles, acudientes y matrículas por año lectivo.
  9. `apps.attendance`: Control diario de asistencia, novedades y registro de ausentismo.
  10. `apps.grades`: Componentes de evaluación, planillas dinámicas y cálculo de promedios.
  11. `apps.homework`: Gestión de tareas, consignas pedagógicas y entregas de estudiantes.
  12. `apps.rules`: Motor de validación académica, promociones, cierres y Decreto 1290.
  13. `apps.reports`: Generación de boletines oficiales, consolidados y cuadros de honor.

### 2.2. Arquitectura y Persistencia de Datos
* **Precisión Numérica Estricta:** Uso mandatario de `DecimalField(max_digits=4, decimal_places=2)` para todas las calificaciones (rango de 1.00 a 5.00) y ponderaciones porcentuales, erradicando por diseño los errores de imprecisión binaria inherentes al punto flotante (IEEE-754).
* **Transaccionalidad Atómica:** Activación de `ATOMIC_REQUESTS = True` a nivel de base de datos y uso selectivo del decorador `@transaction.atomic` en servicios críticos (cierre de periodo, consolidación anual, importación de notas), garantizando que ante cualquier falla se realice rollback inmediato sin dejar datos huérfanos.
* **Estrategia Híbrida de Persistencia para Red Local y Producción:**
  - **SQLite WAL (Write-Ahead Logging):** Configurado con `PRAGMA journal_mode=WAL;` y `PRAGMA busy_timeout=30000;`. Permite que múltiples docentes registren notas y asistencias concurrentemente desde distintas computadoras de la red escolar sin provocar bloqueos de base de datos (`database is locked`).
  - **MySQL (InnoDB / UTF8MB4):** Soporte alternativo nativo y configurable desde `.env` para colegios de gran escala con servidor MySQL centralizado.

### 2.3. Modelo de Seguridad y Control de Acceso (RBAC)
* **Modelo de Usuario Personalizado (`CustomUser`):** Extensión de `AbstractUser` de Django para asociar directamente el documento de identidad, teléfono, dirección, avatar institucional y uno de los 6 roles reconocidos:
  - `ADMIN`: Administrador Técnico (Control total, logs de auditoría, configuración).
  - `RECTOR`: Directivo Docente (Supervisión institucional, cierres formales, dashboards ejecutivos).
  - `SECRETARIA`: Gestión Administrativa (Matrículas, expedientes, asignación de cursos).
  - `TEACHER`: Docente (Planillas de notas, asistencia, tareas y observaciones).
  - `STUDENT`: Estudiante (Consulta de notas, boletines, tareas y asistencias).
  - `PARENT`: Padre de Familia / Acudiente (Seguimiento integral del acudido).
* **Trazabilidad y No Repudio (`AuditLog`):** Registro obligatorio de cada operación de inserción, actualización o eliminación con estructura JSON de valores anteriores (`old_values`) y nuevos (`new_values`), IP origen del cliente y usuario autenticado, operando bajo un modelo de solo lectura que prohíbe modificaciones o borrados de logs.

### 2.4. Interfaz de Usuario y Experiencia (UI/UX)
* **Maquetación Corporativa:** Implementación de **Bootstrap 5.3.3** con hoja de estilos personalizada `academix.css` y tipografía moderna Inter/Roboto.
* **Reactividad Dinámica Liviana con HTMX 1.9.10:** Actualización en tiempo real de semáforos de alerta, planillas de notas y validaciones sin recarga completa de página ni la complejidad operativa de SPAs en Node.js.
* **Vistas Optimizadas para Impresión Oficial:** Plantillas CSS `@media print` para la emisión física o digital de boletines de calificaciones, certificados y consolidados según directrices institucionales.

---

## 3. NORMAS, PROTOCOLOS Y ESTÁNDARES DE LA EMPRESA

Para garantizar la calidad técnica, el orden metodológico y la sostenibilidad del software, el proyecto se rigió por los siguientes protocolos institucionales:

| Dimensión | Norma / Protocolo Aplicado | Mecanismo de Verificación en ACADEMIX |
| :--- | :--- | :--- |
| **Estándar de Codificación** | **PEP 8 (Python)** | Nombres en snake_case para funciones/variables, CamelCase para modelos, imports organizados, docstrings claros. |
| **Diseño y Buenas Prácticas** | **Clean Architecture, SOLID, DRY** | Separación de capas (Models, Views, Forms, Services, Templates). Lógica de negocio encapsulada en servicios. |
| **Seguridad en Aplicaciones Web** | **OWASP Top 10** | Protección anti-CSRF multi-host (`CSRF_TRUSTED_ORIGINS`), ORM contra SQL Injection, auto-escape HTML contra XSS, hashes PBKDF2-SHA256 para contraseñas. |
| **Calidad de Software** | **ISO/IEC 25010** | Evaluación de usabilidad (diseño intuitivo), mantenibilidad (código modular), fiabilidad (transacciones atómicas) y portabilidad (LAN y Cloud). |
| **Marco Metodológico** | **Scrum Ágil** | División del alcance en 5 Sprints secuenciales con entregables funcionales verificables en cada iteración. |
| **Protocolo de Red Local** | **IEEE 802.3 / 802.11 (TCP/IP)** | Lanzador automatizado (`iniciar_servidor_red.py`) sobre `0.0.0.0:8000`, detección dinámica de IP y reglas de Windows Firewall (`firewall.bat`). |
| **Regulación Educativa** | **Decreto 1290 de 2009 (MEN)** | Escala de desempeño (Bajo, Básico, Alto, Superior), límite de inasistencias (20%), umbral de reprobación y boletines oficiales por periodos. |

---

## 4. ESTRUCTURA DE DESGLOSE DEL TRABAJO (EDT / WBS) — FASES Y SPRINTS EJECUTADOS

A continuación se detalla la totalidad de las fases, paquetes de trabajo, componentes y tareas implementadas a lo largo del ciclo de vida del proyecto:

```
PROYECTO ACADEMIX
│
├── FASE 1: Núcleo Tecnológico, Seguridad, Auditoría y Alertas (Sprint 1)
│   ├── 1.1 Configuración de entorno (.env, settings.py híbrido LAN/MySQL)
│   ├── 1.2 Modelo CustomUser y Roles RBAC (apps.accounts)
│   ├── 1.3 Subsistema de Auditoría Inmutable y Middleware (apps.audit)
│   ├── 1.4 Motor de Semaforización y Alertas HTMX (apps.alerts)
│   └── 1.5 Layout Corporativo Base (base.html, sidebar, navbar, toasts)
│
├── FASE 2: Estructura Curricular, Plantel y Matrículas (Sprint 2)
│   ├── 2.1 Años Lectivos, Grados y Cursos/Secciones (apps.courses)
│   ├── 2.2 Áreas de Conocimiento y Asignaturas (apps.subjects)
│   ├── 2.3 Periodos Académicos y Ponderaciones (apps.periods)
│   ├── 2.4 Ficha Docente y Asignación Académica (apps.teachers)
│   └── 2.5 Expedientes Estudiantiles y Matrícula Anual (apps.students)
│
├── FASE 3: Asistencia y Novedades de Convivencia (Sprint 3)
│   ├── 3.1 Sesiones de Clase y Asistencia por Asignatura (apps.attendance)
│   ├── 3.2 Registro de Asistencias, Faltas Justificadas/Injustificadas y Retardos
│   └── 3.3 Motor Estadístico de Inasistencia y Alertas Tempranas (>20%)
│
├── FASE 4: Evaluación, Calificaciones y Tareas Escolares (Sprint 4)
│   ├── 4.1 Criterios de Evaluación Ponderados al 100% (apps.grades)
│   ├── 4.2 Planilla Matricial de Calificaciones Dinámica
│   ├── 4.3 Cálculo Automático de Definitivas de Periodo
│   └── 4.4 Módulo de Tareas, Entregas y Adjuntos (apps.homework)
│
├── FASE 5: Motor de Reglas, Promoción, Cierre y Reportes Oficiales (Sprint 5)
│   ├── 5.1 Reglas del Decreto 1290 de 2009 y Promoción Anual (apps.rules)
│   ├── 5.2 Cierre Formal de Periodos y Bloqueo de Modificaciones
│   ├── 5.3 Boletines Oficiales de Calificaciones con CSS Imprimible (apps.reports)
│   ├── 5.4 Consolidados Matriciales por Curso y Exportación CSV
│   └── 5.5 Cuadros de Honor y Estadísticas para Directivos
│
└── FASE 6: Infraestructura de Red Local, Concurrencia y Despliegue
    ├── 6.1 Concurrencia SQLite WAL + 30s Busy Timeout / Configuración MySQL
    ├── 6.2 Lanzador Inteligente de Red (iniciar_servidor_red.py / .bat)
    ├── 6.3 Automatización del Firewall de Windows (firewall.bat)
    └── 6.4 Manual Operativo de Conexión (GUIA_TRABAJO_EN_RED.md)
```

---

## 5. DETALLE DE ACTIVIDADES Y ENTREGABLES POR SPRINT

### SPRINT 1: Arquitectura Base, Seguridad RBAC, Auditoría y Alertas
* **Objetivo:** Establecer los cimientos del sistema, el modelo de autenticación personalizado, la trazabilidad inmutable y el diseño base responsivo.
* **Componentes Construidos:**
  - `config/settings.py`: Configuración híbrida de base de datos, zona horaria `America/Bogota`, idioma `es-co`, URLs y CSRF dinámico.
  - `apps.accounts`: `CustomUser` con roles (`ADMIN`, `RECTOR`, `SECRETARIA`, `TEACHER`, `STUDENT`, `PARENT`), tipos de documento colombianos (CC, TI, CE, RC), vistas de login/logout y redirección inteligente según rol.
  - `apps.audit`: Modelo `AuditLog`, servicio `log_audit()` y `AuditMiddleware` para registrar en tiempo real quién realiza cada cambio, tabla afectada, ID, datos antiguos y nuevos.
  - `apps.alerts`: Modelo `SystemAlert` con semáforos (🔴 Bloqueo, 🟡 Advertencia, 🔵 Información), soporte para alertas globales o por rol, e integración con HTMX para refresco asíncrono.
  - `templates/base.html`: Interfaz maestra con Bootstrap 5.3.3, barra lateral dinámica según permisos, barra superior y pie de página institucional.
* **Entregable:** Plataforma base operativa con login seguro, dashboard adaptativo y trazabilidad total de peticiones.

---

### SPRINT 2: Estructura Curricular, Plantel Docente y Gestión de Matrículas
* **Objetivo:** Modelar la estructura organizativa de una institución educativa colombiana, vinculando años lectivos, grados, asignaturas, docentes y estudiantes.
* **Componentes Construidos:**
  - `apps.courses`: `AcademicYear` (con bandera `is_current` para año lectivo vigente), `GradeLevel` (Primaria, Secundaria, Media) y `CourseSection` (grupos como 6°A, 7°B, 11°A).
  - `apps.subjects`: `KnowledgeArea` (Matemáticas, Humanidades, Ciencias), `Subject` (Álgebra, Inglés, Física) y `GradeSubject` (malla curricular con intensidad horaria semanal).
  - `apps.periods`: `AcademicPeriod` (Periodos 1 al 4) con control de fechas de apertura y cierre, porcentajes ponderados (25% c/u) y estados (Abierto, Cerrado, Bloqueado).
  - `apps.teachers`: `TeacherProfile` vinculado al usuario docente y `TeachingAssignment` (asignación académica única que evita duplicidad de profesores en una misma materia y curso).
  - `apps.students`: `StudentProfile` (código estudiantil, RH, datos médicos, acudiente) y `Enrollment` (matrícula formal con validación de cupo y unicidad por año escolar).
* **Entregable:** Estructura escolar completa cargada y lista para operación académica.

---

### SPRINT 3: Control de Asistencia y Monitoreo de Ausentismo
* **Objetivo:** Brindar a los docentes una herramienta ágil para la toma de asistencia en el aula y generar semáforos de alerta preventiva por deserción o inasistencia.
* **Componentes Construidos:**
  - `apps.attendance`:
    - `AttendanceSession`: Sesión de clase vinculada a fecha, grupo, asignatura, docente y periodo.
    - `AttendanceRecord`: Registro individual por estudiante con estados estandarizados: Presente (`PRESENT`), Falta Injustificada (`ABSENT`), Falta Justificada (`JUSTIFIED`) y Retardo (`LATE`).
    - `apps.attendance.services`: Motor de cálculo de ausentismo estudiantil (`calculate_student_absence_stats`), acumulando horas dictadas vs. horas no asistidas.
    - Semaforización automática: Si un estudiante supera el 20% de faltas en una materia (límite del Decreto 1290), el sistema genera automáticamente una alerta preventiva dirigida al acudiente, docente y coordinación.
* **Entregable:** Módulo de asistencia con registro ágil en un clic y trazabilidad de inasistencias en tiempo real.

---

### SPRINT 4: Planilla de Calificaciones, Evaluación Decimal y Tareas
* **Objetivo:** Implementar la planilla digital de calificaciones con soporte para criterios de evaluación institucionales y un aula de tareas escolares.
* **Componentes Construidos:**
  - `apps.grades`:
    - `EvaluationCriterion`: Definición flexible de componentes de evaluación por asignatura y periodo (ej. Exámenes 40%, Talleres 40%, Actitudinal 20%) con validación estricta de que la suma equivalga al 100.00%.
    - `GradeRecord`: Calificación por estudiante y criterio con validación en rango 1.00 a 5.00 con dos decimales exactos.
    - `PeriodFinalGrade`: Definitiva calculada del periodo lectivo con nivel de desempeño cualitativo (Bajo, Básico, Alto, Superior).
    - Planilla Matricial Interactiva: Vista de cuadrícula que lista todos los estudiantes del curso y permite al profesor calificar fluidamente.
  - `apps.homework`:
    - `Homework`: Publicación de consignas académicas, fecha y hora límite de entrega y carga de material adjunto (PDF/Word).
    - `HomeworkSubmission`: Entrega digital del estudiante con archivo o texto, registro de fecha y calificación por el docente.
* **Entregable:** Sistema de evaluación completo, preciso, sin redondeos arbitrarios y sincronizado con el aula de tareas.

---

### SPRINT 5: Motor de Reglas, Promoción Escolar, Cierres y Boletines Oficiales
* **Objetivo:** Ejecutar las reglas del Decreto 1290 de 2009 para la promoción anual, bloqueo definitivo de periodos y generación de informes oficiales imprimibles.
* **Componentes Construidos:**
  - `apps.rules`:
    - `PromotionRule`: Parámetros institucionales por año lectivo (nota mínima 3.00, máximo 2 materias reprobadas, 20% inasistencia).
    - `AnnualFinalGrade`: Cálculo de la nota definitiva anual ponderando los 4 periodos lectivos.
    - `AcademicClosingLog`: Auditoría especial de cierres formales de periodo y año lectivo.
    - `close_academic_period()`: Servicio transaccional que bloquea la edición de notas y asistencias del periodo, accesible únicamente por Rector o Administrador.
    - `calculate_annual_promotion()`: Motor que dictamina el estado de cada estudiante al final del año: **Promovido**, **No Promovido (Reprobado)** o **Requiere Nivelación**.
  - `apps.reports`:
    - `student_bulletin_view`: Boletín oficial por periodo y acumulado con desglose de áreas, asignaturas, fallas, puestos, escala nacional y firma de directivos, optimizado con estilos de impresión CSS de alta fidelidad.
    - `section_consolidated_view`: Planilla consolidadora general de todo el grupo en una sola matriz para comisiones de evaluación.
    - Exportador de datos: Descarga directa a CSV / Excel de consolidados para secretaría.
    - `honor_roll_view`: Cuadro de honor automático que premia a los mejores promedios del colegio.
* **Entregable:** Motor de promoción certificado y suite completa de reportes oficiales listos para firma y entrega a padres de familia.

---

### FASE 6: Infraestructura de Red Local, Concurrencia y Despliegue Institucional
* **Objetivo:** Permitir que la institución utilice el sistema en su sala de cómputo o en toda la red Wi-Fi escolar de manera inmediata y sin configuraciones complejas.
* **Componentes Construidos:**
  - `iniciar_servidor_red.py`: Script inteligente que inspecciona los adaptadores de red, resuelve la dirección IP real de la máquina en la LAN (ej. `192.168.1.50` o `10.8.182.30`), valida puertos y arranca Django escuchando en `0.0.0.0:8000` con un banner didáctico de acceso.
  - `iniciar_servidor_red.bat`: Lanzador de doble clic para Windows que ejecuta el script en el entorno virtual.
  - `firewall.bat`: Script automatizado que configura una regla de entrada en el Firewall de Windows Defender para habilitar el tráfico TCP en el puerto 8000.
  - `GUIA_TRABAJO_EN_RED.md`: Documento de orientación técnica para directivos y secretarias con pasos de conexión, resolución de problemas y cuentas de prueba preconfiguradas.
  - Configuración SQLite WAL con timeout de 30 segundos, permitiendo escrituras concurrentes fluidas.
* **Entregable:** Paquete de despliegue en red local autosuficiente, probado y documentado.

---

## 6. CRONOGRAMA DE EJECUCIÓN Y CUMPLIMIENTO DE HITOS

| Hito / Fase | Duración Estimada | Duración Real | Estado | Verificación Técnica |
| :--- | :---: | :---: | :---: | :--- |
| **Sprint 1: Núcleo, RBAC, Auditoría y Alertas** | 2 Semanas | 2 Semanas | **100% Completado** | `CustomUser`, `AuditLog`, `SystemAlert`, `AuditMiddleware` y plantillas base activas. |
| **Sprint 2: Estructura Curricular y Matrículas** | 2 Semanas | 2 Semanas | **100% Completado** | Modelos de cursos, grados, asignaturas, perfiles y matrículas integrados con migraciones. |
| **Sprint 3: Control de Asistencia y Novedades** | 1.5 Semanas | 1.5 Semanas | **100% Completado** | Sesiones de clase, planillas de asistencia y semáforos por >20% de inasistencia operativos. |
| **Sprint 4: Calificaciones, Decimales y Tareas** | 2 Semanas | 2 Semanas | **100% Completado** | Planillas dinámicas, criterios sumando 100%, rango 1.0-5.0 y módulo de tareas con adjuntos. |
| **Sprint 5: Reglas, Promoción, Cierre y Reportes** | 2.5 Semanas | 2.5 Semanas | **100% Completado** | Cierre de periodos atómico, reglas Decreto 1290, boletines oficiales y exportación CSV. |
| **Fase 6: Despliegue en Red LAN y Documentación** | 1 Semana | 1 Semana | **100% Completado** | Lanzador inteligente, firewall automatizado, SQLite WAL optimizado y guía en red. |
| **TOTAL PROYECTO** | **11 Semanas** | **11 Semanas** | **100% CUMPLIDO** | **Sistema Integral ACADEMIX en estado Release Candidate.** |

---

## 7. MATRIZ DE RESPONSABILIDADES (RACI)

*(R = Responsable de Ejecutar, A = Aprobador / Responsable Final, C = Consultado, I = Informado)*

| Entregable / Componente | Líder Proyecto | Arquitecto Software | Dev Backend (Django) | Dev Frontend (UI/UX) | Ingeniero QA |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Definición de Arquitectura MVT y DB** | A | R | C | I | C |
| **Modelo de Autenticación y RBAC** | A | C | R | C | R |
| **Módulo de Auditoría Inmutable** | I | A | R | I | R |
| **Motor de Alertas y Semáforos HTMX** | I | C | R | R | C |
| **Malla Curricular y Matrículas** | A | C | R | C | R |
| **Planilla de Calificaciones y Notas** | A | C | R | R | R |
| **Motor de Reglas y Decreto 1290** | A | R | R | I | R |
| **Boletines y Reportes Imprimibles** | A | I | R | R | R |
| **Configuración de Red LAN y Firewall** | I | A | R | I | R |
| **Pruebas de Sistema y Aceptación** | A | C | C | C | R |

---

## 8. GESTIÓN DE RIESGOS Y PLAN DE CONTINGENCIA

Durante la planificación y ejecución técnica del proyecto se identificaron y mitigaron los siguientes riesgos:

| Riesgo Técnico / Operativo | Impacto | Probabilidad | Estrategia de Mitigación Implementada |
| :--- | :---: | :---: | :--- |
| **Bloqueo de SQLite por Concurrencia simultánea de Docentes** | Alto | Media | Habilitación de modo **WAL (Write-Ahead Logging)** y `busy_timeout=30000` (30s de espera activa). Además, arquitectura desacoplada para migrar a MySQL modificando únicamente el archivo `.env`. |
| **Imprecisión Numérica en Calificaciones y Promedios** | Crítico | Baja | Eliminación total del tipo `FloatField`. Implementación estricta de `Decimal(4,2)` con redondeo bancario estándar (`ROUND_HALF_UP`) según norma colombiana. |
| **Pérdida de Trazabilidad ante Modificación Irregular de Notas** | Crítico | Media | Subsistema `AuditLog` inmutable vinculado a `AuditMiddleware`. Ningún registro de auditoría puede ser editado ni eliminado, capturando valores previos y nuevos. |
| **Alteración de Calificaciones luego de Finalizado el Periodo** | Alto | Alta | Funcionalidad de **Cierre Formal de Periodo** (`close_academic_period`), que bloquea la edición para docentes y exige autorización directiva registrada en auditoría. |
| **Inaccesibilidad en Red Local por Bloqueo de Firewall de Windows** | Medio | Alta | Creación del script desatendido `firewall.bat` para abrir el puerto TCP 8000 con permisos de administrador en un solo clic. |
| **Error 403 Forbidden por CSRF en Dispositivos Móviles de la Red** | Alto | Alta | Inclusión de detección dinámica de IPs en `settings.py` para poblar automáticamente `CSRF_TRUSTED_ORIGINS` sin requerir edición manual. |

---

## 9. PROTOCOLO DE PRUEBAS Y ASEGURAMIENTO DE CALIDAD (QA)

El proyecto fue sometido a rigurosos controles de verificación técnica:

1. **Chequeo de Integridad del Framework (`manage.py check`):**
   - Ejecutado con resultado: `System check identified no issues (0 silenced)`.
2. **Validación de Migraciones (`makemigrations --dry-run`):**
   - Confirmación de cero discrepancias entre los modelos y el esquema de base de datos (`No changes detected`).
3. **Pruebas de Flujo Transaccional:**
   - Creación de año lectivo vigente -> Apertura de periodos -> Matrícula de estudiante -> Asignación de docente -> Toma de asistencia -> Calificación de criterios -> Cierre formal de periodo -> Emisión de boletín oficial.
4. **Pruebas de Concurrencia en Red:**
   - Validación de acceso simultáneo desde 3 equipos clientes en la red LAN ejecutando el script `iniciar_servidor_red.py`, constatando respuesta fluida y sin bloqueos de datos.
5. **Pruebas de Fidelidad de Impresión:**
   - Emisión de boletines a formato PDF y papel físico mediante Google Chrome y Microsoft Edge, verificando que los saltos de página (`page-break`), membretes y firmas mantengan diseño profesional.

---

## 10. CONCLUSIÓN Y DICTAMEN TÉCNICO FINAL

El plan de trabajo del proyecto **ACADEMIX** ha sido ejecutado en su totalidad, cumpliendo rigurosamente con:
- La interpretación del informe técnico de diseño del sistema.
- Las normas y estándares de ingeniería de software (PEP 8, Clean Architecture, OWASP, ISO/IEC 25010).
- La legislación educativa colombiana aplicable (Decreto 1290 de 2009).
- Los protocolos institucionales de concurrencia, seguridad y despliegue en red local.

El software se encuentra en estado **100% Funcional y Validado**, listo para su adopción institucional, pruebas de campo y certificación de evidencias de desarrollo de software.
