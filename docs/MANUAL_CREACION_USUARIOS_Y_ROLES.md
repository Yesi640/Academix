# MANUAL DE CREACIÓN DE USUARIOS DESDE CERO Y GUÍA MODULAR POR ROL
**Plataforma Integral de Gestión Académica — ACADEMIX**  
*Documento Operativo para el Cliente, Rectoría y Administración Escolar | Versión 2.0*

---

## 📌 Contexto Inicial de Entrega

El cliente recibe el sistema configurado con las **dos cuentas de control maestro**:
1. **👑 Super-Administrador** (`admin` / `Admin2026*`): Soporte técnico, infraestructura y base de datos.
2. **🏛️ Directivo / Rector** (`rector` / `Rector2026*`): Máxima autoridad institucional, cierres y parametrización de marca.

A partir de este punto, **el cliente debe crear y poner en marcha a todos los demás integrantes de la comunidad escolar** desde cero. Este manual detalla el orden exacto de creación y la función que cumple cada rol en sus módulos correspondientes.

---

## 🗺️ ORDEN RECOMENDADO DE CREACIÓN (Flujo Lógico Escolar)

Para evitar bloqueos (por ejemplo, no puedes asignarle materias a un profesor que no existe, ni matricular alumnos en un curso sin salones), sigue estrictamente esta secuencia:

```
┌────────────────────────────────────────────────────────────────────────┐
│  PASO 1: Crear la Cuenta de Secretaría Académica                      │
├────────────────────────────────────────────────────────────────────────┤
│  PASO 2: Crear el Cuerpo Docente y Asignar su Carga Académica         │
├────────────────────────────────────────────────────────────────────────┤
│  PASO 3: Crear y Matricular Estudiantes (Individual o Masivo CSV)      │
├────────────────────────────────────────────────────────────────────────┤
│  PASO 4: Crear y Vincular a los Padres de Familia / Acudientes        │
└────────────────────────────────────────────────────────────────────────┘
```

---

## PARTE 1: Cómo Crear Todos los Usuarios Paso a Paso

---

### PASO 1: Cómo Crear la Cuenta de Secretaría Académica

La Secretaría es el brazo ejecutor del plantel (quien matriculará alumnos y expedirá certificados).

#### Método Directo (Recomendado desde el Panel de Control):
1. Inicia sesión con la cuenta de **Rector** (`rector`) o **Administrador** (`admin`).
2. En la barra superior, haz clic en tu avatar y selecciona **Panel Django Admin** (o ingresa directamente en la URL: `http://localhost:8000/admin/`).
3. En la sección **ACCOUNTS**, haz clic en **+ Añadir** al lado de **Usuarios Institucionales** (`CustomUser`).
4. **Formulario de Registro de Secretaría:**
   - **Nombre de usuario:** Escribe un identificador institucional (ejemplo: `secretaria` o `secre_central`).
   - **Contraseña y confirmación:** Asigna una clave inicial segura (ejemplo: `Secre2026*`).
   - Haz clic en **Guardar y continuar editando**.
5. **Datos y Rol Institucional:**
   - **Nombres y Apellidos:** Escribe el nombre completo de la secretaria o secretario.
   - **Correo electrónico:** Correo institucional para notificaciones.
   - **Tipo y Número de documento:** Cédula de Ciudadanía.
   - **Rol en el Sistema (Campo Clave):** Selecciona en la lista desplegable **Secretaría Académica** (`SECRETARIA`).
   - **Permisos de personal (`is_staff`):** Márcalo activo si deseas que acceda también al panel auxiliar.
   - **Debe Cambiar Contraseña (`must_change_password`):** Marca esta casilla para que el sistema le pida obligatoriamente crear su propia clave en su primer acceso.
6. Haz clic en el botón azul **GUARDAR**.
7. ¡Listo! La secretaría ya puede ingresar desde el portal principal seleccionando el rol *Secretaria*.

---

### PASO 2: Cómo Crear el Cuerpo Docente y Asignar Carga Académica

Los docentes orientan el aula y califican. Se crean desde el módulo de la plataforma sin tocar bases de datos.

#### 2.1 Registro del Docente en la Planta Institucional
*Ruta: Menú Lateral > Estructura Académica > Cuerpo Docente*

1. En la parte superior de la pantalla, haz clic en el botón verde **+ Nuevo Registro de Docente**.
2. Completa los campos del asistente:
   - **Nombres:** (ejemplo: *Martha Cecilia*)
   - **Apellidos:** (ejemplo: *Pérez Salazar*)
   - **Tipo de Documento:** Cédula de Ciudadanía (`CC`).
   - **Número de Documento:** (ejemplo: `1098765432`) *(Sin puntos ni espacios)*.
   - **Especialidad o Título:** (ejemplo: *Licenciada en Matemáticas y Física*).
   - **Correo Electrónico:** (ejemplo: `martha.perez@colegio.edu.co`).
   - **Teléfono de Contacto:** (ejemplo: `3101234567`).
3. Haz clic en el botón verde **Guardar y Registrar Docente**.

#### 🤖 ¿Qué credenciales genera el sistema automáticamente?
- **Usuario:** Se genera con el formato `doc_<NumeroDeCedula>` (ejemplo: `doc_1098765432`).
- **Contraseña inicial:** El mismo número de cédula del docente.
- **Primer inicio de sesión:** El sistema le pedirá de forma forzada crear su contraseña personal secreta.

---

#### 2.2 Asignación Académica (Qué materia dicta en qué curso)
Un profesor no podrá calificar ni tomar lista hasta que le asignes sus salones y materias.

1. En la misma pantalla de **Cuerpo Docente**, haz clic en el botón azul **Asignar Carga Académica**.
2. En la ventana emergente, completa:
   - **Docente:** Elige al profesor registrado (ej. *Martha Cecilia Pérez*).
   - **Curso / Salón:** Selecciona el salón (ej. *10-A*).
   - **Asignatura / Saber:** Selecciona la materia que dictará (ej. *Matemáticas*).
   - **Año Lectivo:** Selecciona el año activo (ej. *2026*).
   - **¿Es Director de Grupo?:** Marca esta casilla si este docente es el titular o director encargado de ese salón.
3. Haz clic en **Guardar Asignación**.
4. ¡Inmediatamente esa materia y salón aparecerán habilitados en la planilla del profesor!

---

### PASO 3: Cómo Crear y Matricular Estudiantes / Aprendices

Puedes matricular estudiantes uno a uno o cargar el colegio completo desde una hoja de cálculo.

---

#### Método A: Registro Individual (Uno por Uno)
*Ruta: Menú Lateral > Estructura Académica > Matrículas y Alumnos*

1. Haz clic en el botón azul **+ Nuevo Alumno**.
2. Diligencia los datos personales:
   - **Nombres y Apellidos:** (ejemplo: *Juan David Morales Toro*).
   - **Tipo de Documento:** Tarjeta de Identidad (`TI`), Registro Civil (`RC`) o Cédula (`CC`).
   - **Número de Documento:** (ejemplo: `1023456789`).
   - **Código de Estudiante:** *(Opcional)* Si lo dejas vacío, el sistema generará uno como `EST-456789` o `ALU-2026-1025`.
   - **Correo Electrónico y Teléfono:** Datos de contacto del alumno o acudiente.
   - **Curso / Sección a Matricular:** Selecciona el salón correspondiente (ej. *10-A*).
   - **Acudiente Responsable:** Selecciona el padre si ya fue creado, o déjalo pendiente para vincularlo luego.
3. Haz clic en el botón verde **Confirmar y Matricular**.

#### 🤖 Credenciales generadas para el Estudiante:
- **Usuario:** `est_<NumeroDocumento>` (ejemplo: `est_1023456789`).
- **ID ÚNICO del Alumno:** El código escolar asignado (ejemplo: `EST-456789`).
- **Contraseña inicial:** El número de documento del estudiante.

---

#### Método B: Carga Masiva desde Excel / CSV (Recomendado para inicio de año)
*Ruta: Menú Lateral > Estructura Académica > Matrículas y Alumnos*

1. Haz clic en el botón verde **Carga Masiva CSV**.
2. Haz clic en el enlace **"Descargar Plantilla Oficial CSV"**.
3. Abre el archivo en Microsoft Excel. Verás las columnas reglamentarias:
   - `first_name`: Nombres del alumno.
   - `last_name`: Apellidos del alumno.
   - `document_type`: Tipo (`TI`, `CC`, `RC`).
   - `document_number`: Número de identificación sin puntos.
   - `email`: Correo institucional o personal.
   - `phone`: Número de contacto.
   - `section_code`: Código del salón donde quedará matriculado (ej. `10-A`, `6-B`).
4. Guarda el archivo con formato **CSV (delimitado por comas)**.
5. Regresa a Academix, arrastra el archivo a la casilla de importación y pulsa **Procesar e Importar Alumnos**.
6. En menos de 30 segundos, cientos de estudiantes quedarán creados, matriculados y con sus usuarios listos para acceder.

---

### PASO 4: Cómo Crear y Vincular Padres de Familia / Acudientes

El rol de acudiente permite que los padres hagan seguimiento a las notas y fallas de sus hijos.

#### Opción 1: Registro desde el Formulario Público
1. El padre de familia ingresa a la dirección del portal: `http://localhost:8000/accounts/register/` (o pulsa "Registrarse" en la pantalla de bienvenida).
2. Selecciona en Rol: **Padre de Familia**.
3. Llena sus datos personales (Nombres, Apellidos, Cédula, Correo y su Contraseña personal).
4. El sistema le solicitará el campo obligatorio: **ID ÚNICO del Alumno**.
5. El padre digita el código de su hijo (ej. `EST-456789` o el número de tarjeta de identidad del alumno).
6. Al pulsar **Registrar mi Cuenta**, el sistema valida la existencia del alumno y los enlaza automáticamente.

#### Opción 2: Vinculación desde la Secretaría
1. La secretaría ingresa a `Matrículas y Alumnos`.
2. Busca al alumno y pulsa **Editar Ficha**.
3. En el campo **Padre o Acudiente**, selecciona al usuario correspondiente y pulsa **Guardar Cambios**.

---

## PARTE 2: Función de Cada Rol en su Respectivo Módulo

---

### 📋 1. MÓDULOS DE SECRETARÍA ACADÉMICA

| Módulo en Pantalla | ¿Qué función cumple la Secretaría en este módulo? |
| :--- | :--- |
| **Matrículas y Alumnos** | • Matricular estudiantes nuevos de forma individual.<br>• Realizar cargas masivas de salones completos desde archivos Excel/CSV.<br>• Consultar y editar datos demográficos de los alumnos.<br>• Cancelar o trasladar matrículas de estudiantes retirados. |
| **Expedientes Digitales** | • Cargar y verificar documentos reglamentarios en PDF (Registro civil, certificados de años anteriores, carné de EPS).<br>• Validar el estado de completitud de la carpeta digital de cada alumno. |
| **Observador Escolar** | • Registrar anotaciones de convivencia, felicitaciones o llamados de atención en la hoja de vida del estudiante. |
| **Cuerpo Docente** | • Dar de alta a nuevos profesores en la planta institucional para que Rectoría les asigne carga académica. |
| **Reportes y Certificados** | • Generar en bloque todos los **Boletines de Calificaciones en PDF** por salón.<br>• Emitir certificados de estudio y constancias de matrícula oficiales con sello y código QR. |

---

### 👨‍🏫 2. MÓDULOS DEL DOCENTE / INSTRUCTOR

| Módulo en Pantalla | ¿Qué función cumple el Docente en este módulo? |
| :--- | :--- |
| **Mis Asignaciones** | • Ver el mapa general de todos los cursos y materias que tiene asignados en el año lectivo activo.<br>• Acceder con un clic al aula de trabajo de cada salón. |
| **Planilla de Notas** | • Seleccionar periodo, salón y materia.<br>• Digitar calificaciones parciales de talleres, evaluaciones y trabajos.<br>• El sistema calcula en vivo el promedio ponderado y el estado de aprobación.<br>• Guardar las notas oficiales con un clic. |
| **Llamado de Lista** | • Tomar la asistencia diaria en segundos.<br>• Registrar el estado de cada estudiante con un clic: 🟢 Presente (P), 🔴 Falta (A), 🟡 Justificado (J) o 🟠 Retardo (T). |
| **Tareas y Envíos** | • Crear y publicar actividades escolares con instrucciones claras, fecha/hora límite de entrega y documentos adjuntos de apoyo.<br>• Revisar los trabajos enviados por los alumnos, asignar la puntuación numérica y redactar comentarios de retroalimentación formativa. |
| **Malla Curricular / RAPs** | • Consultar los estándares, competencias y Resultados de Aprendizaje (RAPs) que corresponden al plan de estudios de su materia. |
| **Sábana de Notas** *(Solo si es Director de Grupo)* | • Si el docente es titular de salón, puede consultar la sábana consolidada con las notas de todas las materias de sus alumnos a cargo. |

---

### 🎓 3. MÓDULOS DEL ESTUDIANTE / APRENDIZ

| Módulo en Pantalla | ¿Qué función cumple el Estudiante en este módulo? |
| :--- | :--- |
| **Panel Principal (Dashboard)** | • Visualizar su promedio general acumulado en tiempo real.<br>• Ver las materias inscritas y el semáforo de alertas sobre asignaturas que requieren refuerzo.<br>• Consultar el calendario con las próximas tareas por entregar. |
| **Mis Calificaciones** | • Consultar el desglose de notas parciales y definitivas por materia en el periodo activo y periodos pasados.<br>• Verificar qué materias lleva aprobadas según la escala institucional. |
| **Mis Tareas** | • Ver las tareas escolares activas con su fecha límite.<br>• Descargar las guías y talleres adjuntados por sus profesores.<br>• Cargar su trabajo de respuesta (documentos PDF, Word, imágenes o enlaces web) antes de que venza el plazo.<br>• Consultar la nota final y la retroalimentación pedagógica recibida del docente. |
| **Mis Asistencias** | • Consultar su récord de asistencia a clases para evitar la pérdida de asignaturas por fallas injustificadas. |
| **Boletín de Calificaciones** | • Visualizar y descargar su boletín oficial en PDF con código QR y token de validación digital ante cualquier entidad externa. |

---

### 👨‍👩‍👧 4. MÓDULOS DEL PADRE DE FAMILIA / ACUDIENTE

| Módulo en Pantalla | ¿Qué función cumple el Padre en este módulo? |
| :--- | :--- |
| **Selector de Acudidos** | • Si el padre tiene varios hijos en el colegio, dispone de un selector superior para alternar entre el expediente de cada hijo con un solo clic. |
| **Notas del Estudiante** | • Supervisar en vivo las calificaciones parciales y el promedio acumulado de su hijo sin esperar a la entrega final de notas. |
| **Asistencia del Acudido** | • Recibir alertas inmediatas si su hijo no asistió a alguna clase o presentó retardos no justificados. |
| **Tareas y Actividades** | • Revisar los deberes escolares que los profesores han dejado a su hijo, comprobando qué tareas están pendientes por entregar para apoyar su disciplina en el hogar. |
| **Descarga de Boletines** | • Descargar e imprimir los boletines periódicos de calificaciones oficiales de su hijo en PDF. |

---

## 🔒 RESUMEN DE PRIVACIDAD Y SEGURIDAD ENTRE ROLES

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        POLÍTICA DE AISLAMIENTO                         │
├────────────────────────────────────────────────────────────────────────┤
│ • Un DOCENTE solo puede calificar las materias y cursos que tiene      │
│   formalmente asignados por la administración.                         │
│ • Un ESTUDIANTE jamás puede ver notas, tareas ni expedientes de otros   │
│   compañeros.                                                          │
│ • Un PADRE DE FAMILIA solo tiene acceso de consulta a los datos de sus │
│   propios hijos formalmente vinculados por parentesco.                 │
│ • Las calificaciones de un periodo CERRADO por Rectoría quedan         │
│   congeladas y blindadas contra modificaciones de cualquier usuario.   │
└────────────────────────────────────────────────────────────────────────┘
```

---
*Manual de Creación de Usuarios y Funciones Modulares — ACADEMIX © 2026*  
*Documento certificado para operación y administración institucional.*
