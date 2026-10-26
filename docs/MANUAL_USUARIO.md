# Manual de Usuario del Sistema Academix
**Guía Integral de Operación y Administración Académica**
*Versión: 2.0.0 | Plataforma Multi-Entorno Adaptativa*

---

## 1. Bienvenida a Academix

**Academix** es tu plataforma de gestión escolar y académica integral. Permite administrar de forma sencilla, ágil e intuitiva todos los procesos institucionales: matrículas, asignación de docentes, planes de estudio, calificaciones, asistencia diaria, tareas y boletines.

### 🌟 Característica Exclusiva: Adaptabilidad Institucional Total
Academix se amolda automáticamente a la naturaleza de tu institución. Dependiendo del modelo seleccionado, el sistema transformará sus términos, menús y formularios:

| Modelo Institucional | ¿A quién se enseña? | ¿Quién orienta? | Nivel Académico | Grupo / Salón | Asignatura / Saber |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Básica Primaria, Secundaria y Media** | Estudiante | Docente | Grado | Curso | Asignatura |
| **Universidad / Superior** | Estudiante | Profesor(a) | Semestre | Grupo | Materia |
| **Técnico / SENA** | Aprendiz | Instructor(a) | Trimestre | Ficha | Competencia / Módulo |
| **Academia / Cursos Libres** | Alumno(a) | Tutor(a) | Nivel | Grupo / Clase | Módulo / Taller |

> **🔒 Garantía de Aislamiento:** La información de un modelo nunca se mezcla con la de otro. Al cambiar de entorno, solo verás los estudiantes, grupos, materias y notas correspondientes a ese modelo.

---

## 2. Acceso al Sistema y Roles

### 2.0 Cómo Poner en Marcha el Sistema (Servidor)
Antes de ingresar al navegador, asegúrate de que el servidor esté activo:
- Haz doble clic en el archivo **`iniciar_servidor_produccion.bat`** (acceso local en el mismo equipo).
- O haz doble clic en **`iniciar_servidor_red.bat`** (si vas a ingresar desde otros equipos o celulares en la red Wi-Fi).

### 2.1 Inicio de Sesión
1. Ingresa a la dirección URL en el navegador: `http://localhost:8000/` (o la IP mostrada en consola si trabajas en red).
2. Haz clic en **"Ingresar al Portal"**.
3. Selecciona tu **Rol**.
4. Ingresa tu **Usuario o Identificación**, el **ID ÚNICO del Alumno** (si eres Alumno o Padre) y tu **Contraseña**.
5. Haz clic en **Ingresar al Sistema**.

### 2.2 Tabla de Usuarios y Credenciales de Prueba para Evaluación
Para pruebas inmediatas sin necesidad de crear cuentas previas:

| Rol | Usuario | ID ÚNICO del Alumno | Contraseña | Perfil / Titular |
| :--- | :--- | :--- | :--- | :--- |
| **👑 Administrador** | `admin` | *(No aplica)* | `Admin2026*` | Administrador General |
| **🏛️ Rector / Directivo** | `rector` | *(No aplica)* | `Rector2026*` | Rector Institucional |
| **📋 Secretaría** | `secretaria1` | *(No aplica)* | `Secre2026*` | Secretaría Académica |
| **👨‍🏫 Docente** | `docente1` | *(No aplica)* | `Profe2026*` | Docente de Área |
| **🎓 Estudiante** | `est_1023456789` | `EST-456789` *(o `1023456789`)* | `Estudiante2026*` | Carlos Andrés Gómez |
| **👨‍👩‍👧 Acudiente / Padre** | `manuel` | `EST-456789` *(o `1023456789`)* | `Padre2026*` | Manuel Gómez (Padre) |

---

## 3. Configuración y Adaptabilidad Institucional

*Ruta: Menú Lateral > Ajustes Institucionales*

### 3.1 Cómo cambiar o elegir el Modelo Educativo
1. Dirígete a **Ajustes Institucionales** en el menú lateral.
2. En la sección superior verás una tarjeta indicando el **Modelo Institucional Activo**.
3. Haz clic en el botón **Cambiar Modelo Institucional**.
4. Selecciona una de las 4 opciones:
   - **Colegio (Básica Primaria, Secundaria y Media)**
   - **Universidad / Superior**
   - **Técnico / SENA**
   - **Academia / Cursos Libres**
5. Haz clic en **Aplicar Modelo**.
6. ¡Listo! El sistema adaptará los nombres de todos los módulos, menús y tablas de inmediato, mostrando únicamente la información perteneciente a dicho modelo.

### 3.2 Personalización de Datos de la Institución
- **Nombre de la Institución**: Nombre oficial visible en reportes y encabezados.
- **Lema y NIT / Código DANE**: Información reglamentaria.
- **Escudo / Logo**: Sube la imagen representativa en formato PNG o JPG.
- **Términos Personalizados**: Si lo deseas, puedes refinar los nombres singulares y plurales de los actores del sistema.

---

## 4. Guía de Módulos Operativos

### 4.1 Estructura Académica (Cursos / Fichas / Grupos)
*Ruta: Menú Lateral > Estructura Académica*
- **Ver Niveles**: Consulta la lista de Grados, Semestres, Trimestres o Niveles.
- **Crear Nuevo Grupo / Curso / Ficha**:
  1. Haz clic en **Nueva Sección / Curso / Ficha**.
  2. Selecciona el nivel correspondiente (ej. *10° Grado* o *Trimestre 1*).
  3. Ingresa el nombre o código (ej. *10-A* o *Ficha 2670123*), jornada y aula.
  4. Guarda los cambios.

---

### 4.2 Plan de Estudios (Asignaturas / Competencias / Materias)
*Ruta: Menú Lateral > Plan de Estudios*
- **Áreas de Conocimiento**: Agrupaciones principales (ej. *Ciencias Básicas, Idiomas, Desarrollo de Software*).
- **Asignaturas / Competencias**:
  1. Haz clic en **Nueva Asignatura / Competencia**.
  2. Asigna el código, nombre y horas semanales o créditos académicos.
  3. Vincula el área correspondiente.

---

### 4.3 Gestión de Estudiantes / Aprendices
*Ruta: Menú Lateral > Estudiantes (o Aprendices / Alumnos)*
- **Listado y Filtros**: Busca por nombre, documento o filtra por curso/ficha.
- **Matricular Nuevo Estudiante**:
  1. Haz clic en **Nuevo Registro**.
  2. Llena los datos personales (Nombres, Apellidos, Tipo y N° de Documento, Email).
  3. Selecciona el curso/ficha al cual quedará matriculado(a).
- **Carga Masiva**: Puedes importar listados masivos desde archivos CSV/Excel usando la opción **Carga Masiva**.

---

### 4.4 Gestión de Docentes / Instructores y Asignación Académica
*Ruta: Menú Lateral > Docentes (o Instructores / Tutores)*
- **Registrar Docente**: Ingreso de perfil profesional, contacto y especialidad.
- **Asignación Académica**:
  - Asocia a cada docente las materias/competencias que impartirá en cada curso o ficha específico.

---

### 4.5 Registro de Calificaciones
*Ruta: Menú Lateral > Calificaciones*
1. Selecciona el **Período / Trimestre Académico**, el **Curso / Ficha** y la **Asignatura / Competencia**.
2. Aparecerá la planilla con los estudiantes matriculados.
3. Ingresa las notas de actividades, talleres o evaluaciones.
4. El sistema calcula automáticamente el promedio ponderado y el estado de aprobación según la escala institucional.
5. Haz clic en **Guardar Calificaciones**.

---

### 4.6 Control de Asistencia Diaria
*Ruta: Menú Lateral > Asistencia*
1. Selecciona la **Fecha**, el **Curso / Grupo** y la **Sesión**.
2. El sistema carga la lista con todos los estudiantes marcados como **Presente** por defecto.
3. Marca rápidamente a quienes tengan:
   - 🟢 **Presente (P)**
   - 🔴 **Falta / Ausente (A)**
   - 🟡 **Excusa / Justificado (J)**
   - 🟠 **Retardo / Tardanza (T)**
4. Haz clic en **Registrar Asistencia**.

---

### 4.7 Tareas y Actividades Virtuales
*Ruta: Menú Lateral > Tareas*
- **Para Docentes / Instructores**:
  1. Crear nueva tarea indicando título, descripción, fecha y hora límite de entrega.
  2. Adjuntar archivos guía o material complementario.
  3. Revisar las entregas recibidas de los estudiantes y calificar con comentarios de retroalimentación.
- **Para Estudiantes / Aprendices**:
  1. Ingresar al detalle de la tarea asignada.
  2. Cargar el archivo de solución (PDF, DOCX, ZIP, etc.) y añadir observaciones.
  3. Enviar entrega antes de la fecha límite.

---

### 4.8 Boletines, Informes y Cuadro de Honor
*Ruta: Menú Lateral > Reportes*
- **Boletín Individual por Estudiante**: Genera el informe valorativo oficial con desglose de materias, notas y observaciones disciplinarias, listo para imprimir en PDF.
- **Consolidado por Curso / Sábana de Notas**: Matriz completa con todos los alumnos y asignaturas del período.
- **Cuadro de Honor**: Muestra a los mejores promedios y puestos destacados por grado y grupo.

---

## 5. Preguntas Frecuentes (FAQ)

### ¿Qué pasa si cambio de modelo institucional (por ejemplo de SENA a Colegio)?
El sistema cambia automáticamente toda la interfaz. La información que registraste en el SENA (fichas, aprendices, instructores) queda guardada de forma segura e independiente, y cuando estás en modo Colegio solo verás los cursos, grados y estudiantes del Colegio.

### ¿Cómo puedo trabajar en red con otros computadores de mi institución?
Solo debes ejecutar en el computador principal el archivo `iniciar_servidor_red.py` o `iniciar_servidor_red.bat`. El sistema mostrará la dirección IP (ejemplo: `http://192.168.1.15:8000`) para que los demás equipos puedan conectarse desde sus navegadores sin instalar nada adicional.

### ¿Se pueden exportar e imprimir los reportes?
Sí, todos los módulos de calificaciones, reportes, consolidados y boletines incluyen botones optimizados para exportación e impresión directa.
