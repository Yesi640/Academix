# Manual de Usuario: Guía Práctica de Navegación en Academix
**Sistema Integral de Gestión Académica y Aprendizaje**  
*Documento de Orientación y Usabilidad | Versión 2.0*

---

## 1. Introducción y Conceptos Clave

Bienvenido a **Academix**, una plataforma diseñada para centralizar y simplificar todas las operaciones académicas, de aula y de seguimiento institucional. 

### 💡 Adaptabilidad Institucional (Terminología Dinámica)
Academix adapta automáticamente los nombres de sus menús y pantallas según el tipo de institución en la que estés trabajando:

| Elemento en el Sistema | Modo Colegio | Modo Técnico / SENA | Modo Universidad | Modo Academia |
| :--- | :--- | :--- | :--- | :--- |
| **Persona que aprende** | Estudiante | Aprendiz | Estudiante | Alumno(a) |
| **Persona que enseña** | Docente | Instructor(a) | Profesor(a) | Tutor(a) |
| **Nivel formativo** | Grado | Trimestre | Semestre | Nivel |
| **Salón o grupo** | Curso / Sección | Ficha | Grupo | Clase |
| **Materia o saber** | Asignatura | Competencia / RAP | Materia | Módulo / Taller |

*Este manual utiliza términos generales para que cualquier usuario se oriente con facilidad.*

---

## 2. Cuentas y Credenciales de Acceso al Sistema

Para ingresar y navegar con cualquiera de los roles institucionales disponibles, utiliza las siguientes credenciales preconfiguradas:

| Rol a Seleccionar | Rol en el Formulario | Usuario / Identificación | ID ÚNICO del Alumno | Contraseña Exacta | Nombre del Titular |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **👑 Administrador** | Administrador | `admin` | *(No aplica)* | `Admin2026*` | Administrador General del Sistema |
| **🏛️ Rector / Directivo** | Rector / Rectora | `rector` | *(No aplica)* | `Rector2026*` | Rector Institucional |
| **📋 Secretaría** | Secretaria | `secretaria1` | *(No aplica)* | `Secre2026*` | Secretaría Académica |
| **👨‍🏫 Docente** | Docente | `docente1` | *(No aplica)* | `Profe2026*` | Docente de Área / Titular |
| **🎓 Estudiante** | Alumno | `est_1023456789` | `EST-456789` *(o `1023456789`)* | `Estudiante2026*` | Carlos Andrés Gómez Pérez |
| **👨‍👩‍👧 Padre de Familia** | Padre de Familia | `manuel` | `EST-456789` *(o `1023456789`)* | `Padre2026*` | Manuel Gómez (Acudiente de Carlos) |

> **💡 Nota importante:**  
> Al seleccionar el rol **Alumno** o **Padre de Familia**, se activará el campo obligatorio **"ID ÚNICO del Alumno"**. Digita `EST-456789` o `1023456789`.

---

## 3. Anatomía de la Pantalla (Elementos Globales)

Al iniciar sesión en Academix, encontrarás una interfaz dividida en tres áreas principales diseñadas para una navegación ágil e intuitiva:

```
┌────────────────────────────────────────────────────────────────────────┐
│ [≡] Año Lectivo 2026 • Sede Central        🔔 Avisos   🎨 Tema  👤 Usuario [▼] │ ← Barra Superior (Topbar)
├──────────────────────┬─────────────────────────────────────────────────┤
│ 🎓 ACADEMIX          │                                                 │
│ 👤 Tu Nombre (Rol)   │                                                 │
│                      │                                                 │
│ 📌 MENÚ PRINCIPAL    │            ÁREA PRINCIPAL DE CONTENIDO           │
│ • Panel Principal    │                                                 │
│ • Agenda             │   (Tarjetas informativas, planillas de notas,   │
│                      │    listas de asistencia, entrega de tareas)     │
│ 📚 EVALUACIÓN Y AULA │                                                 │
│ • Calificaciones     │                                                 │
│ • Asistencia         │                                                 │
│ • Tareas             │                                                 │
│                      │                                                 │
│ ⚙️ CUENTA            │                                                 │
│ • Mi Perfil          │                                                 │
│ • Cerrar Sesión      │                                                 │
└──────────────────────┴─────────────────────────────────────────────────┘
  ↑ Barra Lateral (Sidebar)
```

### 2.1 Barra Superior (Topbar)
Ubicada en la parte más alta de la pantalla en todo momento:
1. **Botón Hamburguesa (`≡`)**: Haz clic para contraer o expandir la barra lateral. Ideal si estás en pantallas pequeñas o necesitas más espacio para ver planillas de notas.
2. **Contexto Institucional**: Muestra el año lectivo activo (ej. *Año Lectivo 2026*) y la sede correspondiente.
3. **Campana de Avisos y Notificaciones (`🔔`)**: Muestra alertas del sistema, avisos de actividades y novedades importantes.
4. **Paleta de Colores (`🎨`)** *(Exclusivo para Rector / Administrador)*: Permite personalizar los colores institucionales y el tema visual.
5. **Menú de Usuario (Avatar y Nombre)**:
   - **Mi Perfil**: Consulta y actualización de datos personales y de contacto.
   - **Cambiar Contraseña**: Recomendado realizarlo de forma periódica.
   - **Bitácora de Auditoría / Admin**: Accesos administrativos directos (según permisos).
   - **Cerrar Sesión**: Salida segura del sistema.

### 2.2 Barra Lateral de Navegación (Sidebar)
Es tu brújula principal para moverte entre las diferentes áreas de Academix:
- Los enlaces se iluminan en **azul/color de énfasis** indicando en qué página te encuentras.
- Las opciones disponibles cambian automáticamente de acuerdo con tu **rol asignado** (Estudiante, Docente, Acudiente o Administrador).

### 2.3 Área de Contenido Principal
Aquí se ejecutan todas las tareas operativas. Incluye:
- **Miga de pan (Breadcrumbs)**: Para saber la ruta recorrida (ej. *Inicio > Tareas > Entrega*).
- **Barra de filtros y búsqueda rápida**: Para encontrar rápidamente estudiantes, asignaturas o periodos sin recargar la página.
- **Botones de acción destacados**: Identificados por colores estándar:
  - 🟢 **Verde**: Guardar, confirmar entrega, exportar o crear nuevo registro.
  - 🔵 **Azul**: Ver detalles, editar, consultar o filtrar.
  - 🟡 **Amarillo**: Descargar archivos adjuntos, ver alertas preventivas.
  - 🔴 **Rojo**: Eliminar o cerrar periodos con confirmación de seguridad.

---

## 3. Guía de Navegación por Rol de Usuario

---

### 🎓 3.1 Guía para el Estudiante / Aprendiz

#### Paso 1: Conocer tu Panel Principal (Dashboard)
- Al ingresar verás tu resumen académico: **Promedio General**, cantidad de asignaturas cursadas, tareas activas y estado de asistencias.
- Visualiza alertas tempranas si alguna materia requiere atención.

#### Paso 2: Consultar tus Calificaciones
1. En el menú lateral, haz clic en **Mis Calificaciones**.
2. Selecciona el **Periodo Lectivo** que deseas revisar (ej. *Primer Periodo* o *Trimestre 1*).
3. Verás la lista de asignaturas, la nota de cada componente (cognitivo, procedimental, actitudinal) y la **calificación definitiva**.
4. La tabla resalta automáticamente con colores si la materia está aprobada o en riesgo de recuperación.

#### Paso 3: Gestionar y Enviar Tareas Escolares
1. En el menú lateral, haz clic en **Mis Tareas**.
2. Identifica el estado de cada tarjeta:
   - 🔵 **Activa**: Tarea pendiente por entregar, con fecha límite visible.
   - 🟢 **Entregada**: Trabajo enviado correctamente; esperando calificación.
   - 🟣 **Calificada**: Revisa tu nota numérica y los comentarios del docente en el anillo de puntuación.
   - 🔴 **Vencida**: El plazo expiró y el formulario de envío se encuentra cerrado.
3. Para entregar:
   - Haz clic en **Entregar mi Trabajo**.
   - Escribe un comentario o enlace web explicativo.
   - Haz clic en **Examinar** para adjuntar tu documento (PDF, Word, imagen o comprimido).
   - Pulsa **Confirmar y Enviar Tarea**.

#### Paso 4: Revisar Asistencias
- En **Mis Asistencias** podrás consultar el histórico de clases, con el detalle de fechas, materias, y el registro de retardos o inasistencias justificadas.

#### Paso 5: Consultar y Descargar Boletines
- Desde el módulo de reportes o panel de calificaciones puedes abrir tu **Boletín de Calificaciones en PDF**.
- Cada boletín incluye un código de verificación digital / QR para validar su autenticidad ante terceros.

---

### 👨‍🏫 3.2 Guía para el Docente / Instructor / Profesor

#### Paso 1: Panel de Control del Docente
- En el **Dashboard** encuentras acceso directo a tus grupos asignados, tareas pendientes por calificar y alertas de estudiantes en riesgo académico.

#### Paso 2: Mis Asignaciones Académicas
1. En el menú lateral, haz clic en **Mis Asignaciones**.
2. Visualizarás todas las materias/competencias que tienes asignadas organizadas por grado y grupo.
3. Desde cada tarjeta tienes accesos directos para: **Calificar**, **Llamar Lista** o **Asignar Tareas**.

#### Paso 3: Planilla de Calificaciones
1. Ve a **Planilla de Notas** (o accede desde tus asignaciones).
2. Selecciona:
   - **Periodo**: (ej. *Periodo 1*).
   - **Curso / Grupo**: (ej. *10-A*).
   - **Asignatura / Módulo**: (ej. *Matemáticas*).
3. Se desplegará la lista de estudiantes matriculados.
4. Digita las notas directamente en las casillas correspondientes. El sistema calcula en vivo el promedio ponderado.
5. Haz clic en **Guardar Calificaciones** antes de cambiar de página.

#### Paso 4: Control Diario de Asistencia (Llamado de Lista)
1. Ve a **Llamado de Lista**.
2. Selecciona la **Fecha**, el **Curso** y la **Sesión / Bloque**.
3. Por defecto todos los alumnos aparecen marcados en 🟢 **Presente (P)**.
4. Con un solo clic cambia a quien corresponda:
   - 🔴 **Ausente / Falta (A)**
   - 🟡 **Justificado (J)**
   - 🟠 **Tardanza / Retardo (T)**
5. Haz clic en el botón verde **Registrar Asistencia**.

#### Paso 5: Asignar y Evaluar Tareas
1. Ve a **Tareas y Envíos**.
2. Para crear una tarea:
   - Haz clic en **Nueva Tarea**.
   - Completa: Título, Curso, Asignatura, Descripción, Fecha y Hora Límite.
   - Opcional: Adjunta guías de trabajo, talleres o lecturas de apoyo.
   - Haz clic en **Publicar Tarea**.
3. Para calificar entregas:
   - Abre la tarea creada y pulsa **Ver Entregas**.
   - Descarga el archivo del estudiante, ingresa la puntuación obtenida y deja una retroalimentación constructiva.

---

### 👨‍👩‍👧 3.3 Guía para el Acudiente / Padre de Familia

#### Paso 1: Selección del Acudido
- Si tienes más de un hijo/estudiante a cargo en la institución, en la parte superior de tu panel verás un selector con el nombre de cada uno para alternar entre sus expedientes con un clic.

#### Paso 2: Seguimiento de Notas y Rendimiento
- Haz clic en **Notas del Estudiante** para ver el estado académico en tiempo real de cada materia cursada durante el periodo en curso.

#### Paso 3: Control de Asistencia y Novedades
- En **Asistencia del Acudido** revisa si tu hijo asistió puntualmente a sus clases o si presenta llamados de atención por inasistencias no justificadas.

#### Paso 4: Acompañamiento en Tareas
- En **Tareas y Actividades** puedes comprobar qué deberes escolares han sido asignados, cuáles están pendientes por entrega y cuáles ya fueron revisados por los docentes.

---

### 👑 3.4 Guía para Directivos y Administradores (Rector / Coordinación / Secretaría)

#### Paso 1: Estructura Institucional y Configuración
1. **Ajustes y Marca** (*Menú > Personalización y Marca*): Configura el nombre oficial, NIT/DANE, escudo institucional y modelo educativo (Colegio, SENA, Universidad o Academia).
2. **Cursos y Grados** (*Menú > Estructura Académica*): Configuración de niveles, jornadas, salones y apertura de grupos lectivos.
3. **Malla Curricular** (*Menú > Malla Curricular*): Creación de áreas de conocimiento, asignaturas y asignación de intensidades horarias.
4. **Periodos Lectivos** (*Menú > Periodos Lectivos*): Definición de fechas de inicio, cierre y porcentajes de evaluación para cada corte académico.

#### Paso 2: Gestión de Matrículas y Personal
1. **Matrículas y Estudiantes**: Admisión individual o mediante carga masiva por archivo Excel/CSV.
2. **Cuerpo Docente**: Alta de profesores y configuración de asignación académica (qué profesor dicta qué materia en qué curso).
3. **Gestión de Usuarios y Roles**: Administración de cuentas, restablecimiento de contraseñas y asignación de permisos.

#### Paso 3: Cierres de Periodo y Promoción
1. Ve a **Cierres y Promoción**.
2. Permite bloquear las planillas de calificaciones una vez concluida la fecha de digitación para garantizar la inmutabilidad de las notas.
3. Ejecutar el cálculo de promoción y graduación al término del año lectivo.

#### Paso 4: Generación de Boletines y Consolidados
1. Ve al módulo de **Reportes**:
   - **Boletines Masivos por Curso**: Generación en lote de todos los boletines de un salón en formato PDF listo para impresión.
   - **Sábana Consolidada de Notas**: Matriz completa de estudiantes vs. materias con exportación a formato Excel/CSV.
   - **Cuadro de Honor**: Reporte automático de los mejores promedios y desempeños destacados por grado.

#### Paso 5: Seguridad y Auditoría
- En **Auditoría Inmutable**, el equipo directivo puede rastrear qué usuario realizó qué acción, en qué fecha y desde qué dirección IP (creación de notas, cambios de matrícula o modificaciones administrativas).

---

## 4. Preguntas Frecuentes y Solución de Problemas

### ❓ Olvidé mi contraseña o no puedo ingresar
1. En la pantalla de login, haz clic en **¿Olvidaste tu contraseña?** si la opción está habilitada por tu institución.
2. Si eres estudiante o padre de familia, comunícate con la secretaría o el administrador del sistema para que restablezca tu clave de acceso provisional.
3. Una vez dentro, dirígete a tu avatar en la esquina superior derecha y selecciona **Cambiar Contraseña**.

### ❓ No veo mis materias o mis cursos asignados
- **Si eres docente**: Verifica con la coordinación académica que tu asignación docente para el año lectivo activo esté registrada en el sistema.
- **Si eres estudiante**: Confirma con la secretaría que tu matrícula se encuentre en estado **Activa** en el curso o ficha correspondiente.

### ❓ ¿Cómo navegar desde un teléfono celular o tableta?
- Academix es 100% responsivo. En dispositivos móviles, la barra lateral se oculta automáticamente.
- Toca el botón **`≡` (tres líneas horizontales)** en la esquina superior izquierda para abrir el menú de navegación y toca cualquier sección para ingresar.

### ❓ ¿Cómo imprimir o guardar un informe en PDF?
- Cada reporte (boletines, fichas de matrícula, listas de asistencia) incluye un botón azul con el ícono de impresora o el texto **Descargar PDF**. 
- Puedes guardarlo directamente en tu equipo o imprimirlo seleccionando tu impresora habitual.

---
*Academix © 2026 - Plataforma de Gestión y Excelencia Académica.*
