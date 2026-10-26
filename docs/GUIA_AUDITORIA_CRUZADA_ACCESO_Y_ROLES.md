# GUÍA DE OPERACIÓN A CIEGAS Y ACCESO AL SISTEMA — ACADEMIX
## Actividad: Auditoría Cruzada de Manuales y Software
**Documento para el Equipo Evaluador (Sin Intervención Verbal)**  
*Plataforma Multi-Entorno Adaptativa de Gestión Académica y Aprendizaje*  
*Versión: 2.0.0 | Año Lectivo 2026*

---

## 📌 Protocolo de Evaluación a Ciegas

Estimados compañeros del **Equipo Evaluador**:

Este documento ha sido diseñado siguiendo la regla de **Cero Explicaciones Verbales**. Contiene toda la información necesaria para que puedan encender el sistema, acceder con cualquier rol institucional y validar los flujos operativos de la plataforma de forma autónoma.

---

## 1. Paso 0: Cómo Poner en Marcha el Sistema (Iniciar el Servidor)

Si el servidor aún no está encendido en el computador donde van a evaluar, sigan cualquiera de estas dos opciones rápidas:

### Opción Rápida (Recomendada — 1 solo clic):
1. Abran la carpeta principal del proyecto: `c:\Academix`
2. Hagan doble clic sobre el archivo:
   - **`iniciar_servidor_produccion.bat`** (para evaluar en el mismo computador), o
   - **`iniciar_servidor_red.bat`** (si van a conectarse desde varios computadores o celulares por red local / Wi-Fi).
3. Se abrirá una ventana de consola negra indicando que el servidor está activo en:
   ```text
   Starting development server at http://127.0.0.1:8000/
   ```
   *(No cierren esa ventana mientras estén evaluando).*

### Opción por Consola / Terminal:
Si prefieren iniciarlo por comandos, abran una terminal en `c:\Academix` y ejecuten:
```powershell
.\venv\Scripts\activate
python manage.py runserver 0.0.0.0:8000
```

---

## 2. Paso 1: Cómo Ingresar al Sistema desde el Navegador

1. Abran su navegador web preferido (**Google Chrome, Microsoft Edge, Firefox o Brave**).
2. Escriban en la barra de direcciones:
   ```text
   http://localhost:8000/
   ```
   *(O la dirección IP que muestre la consola si están en otro computador conectado por Wi-Fi, ej: `http://192.168.1.15:8000/`).*
3. Verán la página de bienvenida con el nombre institucional y escudo del colegio.
4. Hagan clic en el botón principal **"Ingresar al Portal"** para desplegar el formulario de acceso.

---

## 3. Tabla Maestra de Credenciales de Prueba (Cheat Sheet)

Para facilitar la evaluación inmediata, el sistema cuenta con usuarios preconfigurados para cada uno de los 6 roles. Utilicen los siguientes datos exactos:

| Rol a Seleccionar | Campo "Usuario o Identificación" | Campo "ID ÚNICO del Alumno" | Contraseña Exacta | Nombre del Usuario de Prueba |
| :--- | :--- | :--- | :--- | :--- |
| **👑 Administrador** | `admin` | *(No aplica)* | `Admin2026*` | Administrador General del Sistema |
| **🏛️ Rector / Rectora** | `rector` | *(No aplica)* | `Rector2026*` | Rector Institucional |
| **📋 Secretaria** | `secretaria1` | *(No aplica)* | `Secre2026*` | Secretaría Académica |
| **👨‍🏫 Docente** | `docente1` | *(No aplica)* | `Profe2026*` | Docente de Área / Titular |
| **🎓 Alumno** | `est_1023456789` | `EST-456789` *(o `1023456789`)* | `Estudiante2026*` | Carlos Andrés Gómez Pérez |
| **👨‍👩‍👧 Padre de Familia** | `manuel` | `EST-456789` *(o `1023456789`)* | `Padre2026*` | Manuel Gómez (Acudiente de Carlos) |

> **💡 Nota para evaluar Estudiante o Padre de Familia:**  
> Al seleccionar el rol **Alumno** o **Padre de Familia**, el formulario activa automáticamente la casilla **"ID ÚNICO del Alumno"**. Pueden escribir el código institucional `EST-456789` o el número de documento `1023456789`.

---

## 4. Guía de Misiones de Prueba (Flujos para el Evaluador a Ciegas)

Para auditar y comprobar que cada rol cumple su función, sigan estas misiones paso a paso:

---

### 🧪 Misión 1: Probar el Rol Rector (`rector` / `Rector2026*`)
1. **Inicio:** Selecciona rol *Rector / Rectora*, digita usuario `rector` y contraseña `Rector2026*`. Pulsa *Ingresar*.
2. **Dashboard Directivo:** Observa las estadísticas globales del colegio, estudiantes activos, profesores y distribución por jornadas.
3. **Personalización y Marca:** Ve al menú lateral `Administración y Marca > Personalización y Marca`. Aquí puedes ver o cambiar el nombre del colegio, lema, NIT y escudo oficial.
4. **Cierres y Promoción:** Ve a `Cierres y Promoción > Cierres y Promoción`. Observa cómo se gestionan y bloquean los periodos para proteger las calificaciones.
5. **Cerrar Sesión:** Haz clic en tu nombre en la esquina superior derecha y selecciona **Cerrar Sesión**.

---

### 🧪 Misión 2: Probar el Rol Secretaría (`secretaria1` / `Secre2026*`)
1. **Inicio:** Selecciona rol *Secretaria*, usuario `secretaria1`, clave `Secre2026*`.
2. **Matrículas y Alumnos:** Ve a `Estructura Académica > Matrículas y Alumnos`.
   - Verás la lista de alumnos matriculados con filtros rápidos de búsqueda.
   - Haz clic en el botón de **Expediente** de cualquier alumno para revisar sus documentos cargados y su observador escolar.
   - Observa el botón de **Carga Masiva CSV** para matricular listas enteras de alumnos desde Excel.
3. **Boletines y Reportes:** Ve al módulo de reportes para emitir constancias o boletines individuales en PDF con código QR.
4. **Cierra sesión.**

---

### 🧪 Misión 3: Probar el Rol Docente (`docente1` / `Profe2026*`)
1. **Inicio:** Selecciona rol *Docente*, usuario `docente1`, clave `Profe2026*`.
2. **Mis Asignaciones:** Verás tus cursos y materias asignadas. Haz clic en **Entrar al Aula** o **Calificar**.
3. **Planilla de Notas:**
   - Selecciona el curso y la materia.
   - Digita o modifica una calificación en las casillas interactivas. Observa cómo el promedio se recalcula automáticamente en vivo.
   - Haz clic en **Guardar Calificaciones**.
4. **Llamado de Lista (Asistencia Diaria):**
   - Ve a `Llamado de Lista`.
   - Selecciona fecha y sesión; marca a los alumnos presentes o ausentes con un solo clic (P, A, J, T) y pulsa **Registrar Asistencia**.
5. **Tareas y Envíos:**
   - Ve a `Tareas y Envíos`.
   - Puedes crear una nueva tarea con fecha límite y archivo adjunto, o revisar y calificar los trabajos enviados por los alumnos.
6. **Cierra sesión.**

---

### 🧪 Misión 4: Probar el Rol Estudiante (`est_1023456789` / `Estudiante2026*`)
1. **Inicio:**
   - Rol: *Alumno*
   - Usuario: `est_1023456789`
   - ID ÚNICO del Alumno: `EST-456789` (o `1023456789`)
   - Contraseña: `Estudiante2026*`
2. **Panel del Estudiante:** Observa el promedio acumulado, alertas y materias inscritas.
3. **Mis Calificaciones:** Consulta las notas parciales y definitivas registradas por los docentes.
4. **Mis Tareas:**
   - Entra a `Mis Tareas`.
   - Abre una tarea activa, pulsa **Entregar mi Trabajo**, escribe un comentario y adjunta un archivo de prueba.
   - Observa el anillo de puntuación en tareas calificadas con los comentarios del docente.
5. **Descarga de Boletín:** Genera tu boletín valorativo oficial en PDF con código de verificación QR.
6. **Cierra sesión.**

---

### 🧪 Misión 5: Probar el Rol Padre de Familia (`manuel` / `Padre2026*`)
1. **Inicio:**
   - Rol: *Padre de Familia*
   - Usuario: `manuel`
   - ID ÚNICO del Alumno: `EST-456789` (o `1023456789`)
   - Contraseña: `Padre2026*`
2. **Panel de Supervisión:** Verás que estás vinculado al alumno **Carlos Andrés Gómez Pérez**.
3. **Supervisión de Notas y Asistencia:** Puedes ver en tiempo real el progreso de tu hijo, inasistencias y tareas escolares pendientes.
4. **Cierra sesión.**

---

### 🧪 Misión 6: Probar el Rol Administrador (`admin` / `Admin2026*`)
1. **Inicio:** Selecciona rol *Rector* o entra directo con usuario `admin` y contraseña `Admin2026*`.
2. **Gestión de Usuarios:** Ve a `Administración y Marca > Gestión Usuarios`.
   - Busca a cualquier docente o estudiante.
   - Prueba el botón para activar/desactivar un usuario con un solo clic.
3. **Bitácora de Auditoría Inmutable:** Ve a `Auditoría Inmutable`.
   - Comprueba cómo el sistema registró con fecha, hora, usuario e IP cada una de las pruebas y acciones que acabas de realizar en las misiones anteriores.

---

## 5. Misión Especial: Probar la Adaptabilidad Multi-Entorno

Academix tiene la capacidad única de amoldarse al tipo de institución:
1. Ingresa como Rector (`rector`).
2. Ve a `Administración y Marca > Personalización y Marca`.
3. En **Modelo Institucional**, cambia de *Colegio* a **Técnico / SENA** y pulsa **Guardar Ajustes**.
4. ¡Observa la magia de adaptación!:
   - Los cursos ahora se llaman **Fichas**.
   - Los grados ahora se llaman **Trimestres**.
   - Los estudiantes ahora se llaman **Aprendices**.
   - Los docentes ahora se llaman **Instructores**.
   - Las materias ahora se llaman **Competencias y RAPs**.
5. Puedes regresar a modo *Colegio* en cualquier momento sin perder datos.

---

## 6. Solución Rápida de Incidencias (Troubleshooting)

| Problema | Causa Posible | Solución Inmediata |
| :--- | :--- | :--- |
| **La página no carga en `localhost:8000`** | El servidor no se ha iniciado | Haz doble clic en `iniciar_servidor_produccion.bat` en `c:\Academix`. |
| **Error: "El ID ÚNICO del alumno es obligatorio"** | Se seleccionó rol Alumno o Padre pero falta el ID | Digita `EST-456789` o `1023456789` en la casilla correspondiente. |
| **Error: "Credenciales inválidas"** | Error de digitación en mayúsculas | Verifica las credenciales en la Tabla Maestra de la Sección 3 respetando mayúsculas y asteriscos. |
| **Conexión en red desde otro PC o celular** | Bloqueo por firewall local | Ejecuta el archivo `firewall.bat` como administrador en el PC servidor para habilitar el puerto 8000. |

---
*Fin de la Guía de Evaluación a Ciegas — ACADEMIX © 2026*
