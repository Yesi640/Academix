# 📖 MANUAL DE USUARIO FINAL DEL SISTEMA ACADEMIX
**Guía Integral de Operación, Navegación y Procesos Escolares por Roles**  
*Versión: 2.5.0 | Plataforma Web en la Nube y Red Local*

---

## 1. BIENVENIDA A ACADEMIX

**ACADEMIX** es la plataforma institucional moderna de gestión escolar diseñada para conectar a directivos, secretaría, docentes, alumnos y acudientes en un único entorno ágil, transparente y seguro.

A través de este sistema podrás realizar matrículas, registrar asistencias en tiempo real, asentar calificaciones bimestrales con escalas oficiales, enviar y calificar tareas, redactar novedades en el observador escolar y emitir boletines de calificaciones oficiales con código QR.

---

## 2. TABLA OFICIAL DE ACCESO Y CREDENCIALES

Para ingresar a la plataforma, abre tu navegador web (Google Chrome, Firefox, Safari o Microsoft Edge) y accede al enlace de tu institución:
* **Enlace Web en la Nube:** [https://academix-q2g4.onrender.com/accounts/login/](https://academix-q2g4.onrender.com/accounts/login/)
* **Enlace en Servidor Local:** `http://localhost:8000/accounts/login/`

### 🔑 Credenciales Institucionales Activas:

| Rol a Seleccionar | Usuario / Documento | ID Único Alumno *(si aplica)* | Contraseña | ¿Quién debe usar esta cuenta? |
| :--- | :--- | :--- | :--- | :--- |
| **👑 Superadministrador** | `admin` | *(No aplica)* | `Academix2026!` | Administrador de sistemas y soporte técnico. |
| **🏛️ Rector / Rectora** | `rector` | *(No aplica)* | `Academix2026!` | Rectores y directores de sede institucional. |
| **📋 Secretaría** | `nuryssecretaria` | *(No aplica)* | `123456789` | Secretaría académica, admisiones y cobros. |
| **👨‍🏫 Docente** | `docente` | *(No aplica)* | `Academix2026!` | Profesores de aula y directores de grupo. |
| **🎓 Alumno** | `alumno` *(o ID)* | **`ALU-2026-1001`** | `Academix2026!` | Estudiantes matriculados. |
| **👨‍👩‍👧 Padre de Familia** | `padre` | **`ALU-2026-1001`** | `Academix2026!` | Acudientes y padres de familia. |

---

## 3. PASO A PASO: CÓMO INICIAR SESIÓN

1. En la pantalla de ingreso, asegúrate de seleccionar tu **Sede Escolar** (ej. *Institución Educativa ACADEMIX Central*).
2. En el desplegable **"ROL EN EL SISTEMA"**, elige tu perfil:
   * Si eres docente, elige **Docente**.
   * Si eres secretaria, elige **Secretaria**.
   * Si eres directivo, elige **Rector / Rectora**.
   * Si eres estudiante, elige **Alumno**. *(El formulario te mostrará el campo obligatorio: ID ÚNICO DEL ALUMNO)*.
   * Si eres acudiente, elige **Padre de Familia**. *(Se solicitará tu usuario de padre y el ID de tu hijo)*.
3. Ingresa tu usuario y contraseña correspondiente.
4. Haz clic en el botón azul **"Ingresar a la Plataforma"**.
5. ¡Listo! Accederás de inmediato al Panel de Control (Dashboard) adaptado a tu rol.

---

## 4. GUÍA OPERATIVA SEGÚN TU ROL

### 🏛️ A. ROL: RECTORÍA Y ADMINISTRACIÓN GENERAL (`rector` / `admin`)
* **Panel de Control:** Resumen gráfico con total de estudiantes matriculados, docentes activos, cursos y porcentaje global de asistencia institucional.
* **Gestión de Sedes y Escuelas:** Configuración de nombre del colegio, resolución DANE, lema institucional y escudo en alta definición.
* **Apertura de Año Lectivo y Periodos:** Creación del calendario escolar vigente y habilitación de los 4 periodos académicos bimestrales.
* **Auditoría del Sistema:** Supervisión en tiempo real de cada cambio de nota, matrícula o pago realizado en el colegio con fecha, hora e IP.

---

### 📋 B. ROL: SECRETARÍA ACADÉMICA (`nuryssecretaria`)
* **Admisión y Matrícula en 1 Solo Paso:**
  1. Ingresa a **Estudiantes** > Botón **+ Nuevo Alumno**.
  2. Diligencia nombres, documento de identidad, acudiente y selecciona el curso (ej. *1°A*, *6°-A*).
  3. Al guardar, el sistema genera automáticamente el expediente, el **ID ÚNICO** y envía las credenciales al correo del estudiante.
* **Gestión de Expedientes y Ficha Médica:** Consulta de certificados de estudio, historial de EPS y tipo de sangre del alumno.
* **Módulo de Tesorería y Cartera:**
  * Registro de pagos de matrículas y pensiones mensuales.
  * Emisión de recibos de caja con soporte para paz y salvo escolar.

---

### 👨‍🏫 C. ROL: DOCENTE TITULAR (`docente`)
* **Planilla Digital de Calificaciones:**
  1. Ingresa a **Calificaciones** > Selecciona tu grupo y asignatura asignada.
  2. Registra las valoraciones bimestrales en las tres dimensiones pedagógicas:
     * **SABER (Cognitiva - 40%):** Pruebas y evaluaciones.
     * **HACER (Procedimental - 40%):** Talleres y proyectos de clase.
     * **SER (Actitudinal - 20%):** Convivencia y puntualidad.
  3. El sistema calcula la nota definitiva y la escala nacional (Bajo, Básico, Alto, Superior) de forma automática.
* **Control Diario de Asistencia:**
  * Toma de asistencia rápida por salón: Presente (verde), Inasistencia Injustificada (rojo), Retardo (amarillo) o Excusa Médica (azul).
* **Gestión de Tareas y Talleres:**
  * Publica actividades con fecha límite, instrucciones y archivos adjuntos (PDF o Word).
  * Revisa y califica los envíos de los alumnos con retroalimentación personalizada.
* **Observador Convivencial del Alumno:**
  * Registro de faltas tipo I, II o felicitaciones con firma y compromisos pedagógicos.

---

### 🎓 D. ROL: ESTUDIANTE (`alumno`)
* **Mi Aula Virtual y Tareas:**
  * Visualiza todas las tareas pendientes con sus fechas de vencimiento.
  * Sube tus respuestas y archivos adjuntos con confirmación de entrega en pantalla.
* **Mis Calificaciones y Boletín Escolar:**
  * Consulta tus notas parciales por periodo y tu promedio acumulado.
  * Descarga tu **Boletín Académico Oficial** en PDF con sello institucional y código QR.
* **Mi Registro de Asistencia:**
  * Seguimiento de fallas y justificaciones tramitadas ante secretaría o coordinación.

---

### 👨‍👩‍👧 E. ROL: PADRE DE FAMILIA / ACUDIENTE (`padre`)
* **Seguimiento Académico de tu Hijo:**
  * Monitoreo en tiempo real de calificaciones y tareas enviadas por los profesores.
* **Alertas de Inasistencia:**
  * Notificación inmediata si tu hijo no asistió a una clase.
* **Observador Escolar:**
  * Consulta de anotaciones disciplinarias y felicitaciones emitidas por la institución.
* **Estado de Cuenta Escolar:**
  * Consulta del estado de pagos de pensión y certificados de paz y salvo.

---

## 5. PREGUNTAS FRECUENTES Y SOLUCIÓN DE PROBLEMAS

### ¿Qué hago si al intentar entrar dice "No existe ningún usuario registrado con..."?
1. Verifica que en el menú desplegable **"ROL EN EL SISTEMA"** hayas seleccionado el rol correcto (por ejemplo, si eres estudiante, debes cambiar el selector a "Alumno").
2. Si eres estudiante, debes escribir tu **ID ÚNICO** (ejemplo: `ALU-2026-1001`) o tu número de documento en la casilla correspondiente.
3. Asegúrate de no tener espacios en blanco al inicio o al final de tu usuario.

### ¿Cómo cambio mi contraseña?
Una vez dentro de la plataforma, haz clic sobre tu nombre en la esquina superior derecha, selecciona **"Mi Perfil"** y luego **"Cambiar Contraseña"**.
