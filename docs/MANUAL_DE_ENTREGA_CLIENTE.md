# MANUAL OFICIAL DE ENTREGA Y OPERACIÓN DEL SISTEMA
## Plataforma de Gestión Académica y Aprendizaje — ACADEMIX
**Documento de Entrega al Cliente, Rectoría y Administración Institucional**  
*Versión de Entrega: 2.0.0 Estable | Fecha de Puesta en Producción: 2026*

---

## 1. Acta de Entrega y Bienvenida al Cliente

Estimado **Equipo Directivo y Administrativo**:

Hacemos entrega formal de la plataforma **ACADEMIX**, un sistema de información web integral concebido para optimizar la gestión escolar, centralizar las calificaciones, modernizar el control de asistencia diaria, automatizar la entrega de tareas virtuales y blindar la trazabilidad académica e institucional.

El sistema se entrega 100% operativo, preconfigurado para trabajar tanto en un equipo principal (servidor institucional) como en **red local cableada o Wi-Fi**, permitiendo que directivos, secretaría, docentes, acudientes y estudiantes se conecten de manera concurrente desde sus computadores personales, tabletas o celulares sin necesidad de instalar software adicional en sus dispositivos.

---

## 2. Cómo Ingresar al Sistema por Primera Vez

### 2.1 Direcciones de Acceso (URLs)

1. **Desde el Computador Servidor (Donde está instalado el sistema):**
   - Abre tu navegador favorito (Google Chrome, Microsoft Edge, Firefox, Brave).
   - Escribe en la barra de direcciones:
     ```
     http://localhost:8000/
     ```
2. **Desde Cualquier Otro Dispositivo Conectado a la Red del Colegio (Docentes, Secretaría, Estudiantes):**
   - Abre el navegador web.
   - Escribe la dirección IP asignada al servidor dentro de tu red local:
     ```
     http://192.168.X.X:8000/
     ```
   *(Nota: Puedes consultar la IP exacta ejecutando el archivo `iniciar_servidor_red.bat` provisto en el sistema).*

---

### 2.2 Credenciales Maestras de Entrega

Para la recepción y primera configuración del sistema se entregan las siguientes cuentas de inicio:

| Rol de Entrega | Rol en el Formulario | Usuario / Identificación | ID ÚNICO del Alumno | Contraseña Exacta | Nombre del Titular |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **👑 Super-Administrador** | Administrador | `admin` | *(No aplica)* | `Admin2026*` | Administrador General |
| **🏛️ Directivo / Rector** | Rector / Rectora | `rector` | *(No aplica)* | `Rector2026*` | Rector Institucional |
| **📋 Secretaría Académica** | Secretaria | `secretaria1` | *(No aplica)* | `Secre2026*` | Secretaría Académica |
| **👨‍🏫 Docente / Instructor** | Docente | `docente1` | *(No aplica)* | `Profe2026*` | Docente de Área / Titular |
| **🎓 Estudiante / Aprendiz** | Alumno | `est_1023456789` | `EST-456789` *(o `1023456789`)* | `Estudiante2026*` | Carlos Andrés Gómez Pérez |
| **👨‍👩‍👧 Padre de Familia** | Padre de Familia | `manuel` | `EST-456789` *(o `1023456789`)* | `Padre2026*` | Manuel Gómez (Acudiente) |

> **⚠️ REGLA DE SEGURIDAD CRÍTICA N° 1:**  
> Por política de seguridad institucional, en cuanto ingreses por primera vez debes hacer clic en tu avatar en la esquina superior derecha, entrar a **Cambiar Contraseña** y definir una clave secreta que solo la dirección del colegio conozca.

---

### 2.3 Cómo Funciona el Formulario de Inicio de Sesión (Login)

La pantalla de acceso cuenta con 4 campos intuitivos:
1. **Seleccione su Rol**: Elige en la lista desplegable tu función (*Rector / Rectora, Docente, Alumno, Padre de Familia, Secretaria*).
2. **Seleccione su Institución** *(Modo Multi-Escuela)*: Si la plataforma administra más de una sede o colegio, selecciona tu institución para cargar su escudo y colores corporativos.
3. **Usuario o Identificación**:
   - Digita tu nombre de usuario (ejemplo: `rector`) o tu número de cédula/documento.
4. **ID ÚNICO del Alumno** *(Exclusivo para Estudiantes)*:
   - Si se selecciona el rol *Alumno*, se activa este campo para validar el código institucional (ejemplo: `ALU-2026-1001` o número de documento del aprendiz).
5. **Contraseña**: Digita tu clave de acceso y pulsa el botón **Ingresar al Sistema**.

---

## 3. Checklist de Puesta en Marcha (Primeros Pasos del Cliente)

Sigue este orden secuencial para configurar tu institución desde cero:

```
┌────────────────────────────────────────────────────────────────────────┐
│  PASO 1: Personalización y Marca (Nombre, NIT, Logo, Escudo, Colores) │
├────────────────────────────────────────────────────────────────────────┤
│  PASO 2: Periodos Lectivos (Fechas y Porcentajes de los Periodos)      │
├────────────────────────────────────────────────────────────────────────┤
│  PASO 3: Estructura de Cursos (Grados: 6°, 7°... y Cursos: 6A, 6B...)  │
├────────────────────────────────────────────────────────────────────────┤
│  PASO 4: Malla Curricular (Asignaturas / Competencias / RAPs)         │
├────────────────────────────────────────────────────────────────────────┤
│  PASO 5: Creación de Docentes y Asignación de Carga Académica         │
├────────────────────────────────────────────────────────────────────────┤
│  PASO 6: Matrícula de Estudiantes (Individual o Carga Masiva CSV)      │
├────────────────────────────────────────────────────────────────────────┤
│  PASO 7: Vinculación de Acudientes / Padres de Familia                 │
└────────────────────────────────────────────────────────────────────────┘
```

### Paso 1: Identidad Institucional y Marca
- **Ruta:** *Menú Lateral > Administración y Marca > Personalización y Marca*
- Ingresa el **Nombre Oficial** de tu institución (aparecerá en boletines y certificados).
- Ingresa el **Lema**, **Código DANE** y **NIT**.
- Carga el **Escudo / Logo** oficial en formato PNG o JPG.
- Selecciona el **Modelo Institucional**:
  - *Colegio Tradicional* (Primaria, Secundaria, Media).
  - *Técnico / SENA* (Trimestres, Fichas, Competencias, Aprendices).
  - *Universidad / Superior* (Semestres, Materias, Créditos).
  - *Academia / Cursos Libres* (Niveles, Módulos, Talleres).
- Haz clic en **Guardar Ajustes**. El sistema adaptará de inmediato los nombres de todos los módulos.

### Paso 2: Periodos Lectivos
- **Ruta:** *Menú Lateral > Estructura Académica > Periodos Lectivos*
- Verifica que el **Año Lectivo 2026** esté activo.
- Crea o revisa los cortes evaluativos (ej. *Periodo 1: 25%, Periodo 2: 25%, Periodo 3: 25%, Periodo 4: 25%*).

### Paso 3: Cursos y Grados
- **Ruta:** *Menú Lateral > Estructura Académica > Cursos y Grados*
- Comprueba los grados existentes o agrega nuevos.
- Abre los cursos de cada grado indicando su jornada (Mañana, Tarde, Única) y aula física.

---

## 4. Cómo Crear los Usuarios del Sistema

Academix cuenta con asistentes optimizados para que la secretaría o el rector registren a todos los actores escolares sin complicaciones técnicas.

---

### 4.1 Creación del Cuerpo Docente / Instructores

*Ruta: Menú Lateral > Estructura Académica > Cuerpo Docente > Botón "Nuevo Docente"*

1. Haz clic en **Nuevo Registro de Docente**.
2. Completa los datos en pantalla:
   - **Nombres y Apellidos** del profesor.
   - **Tipo y Número de Documento** (Cédula de Ciudadanía).
   - **Especialidad o Título** (ej. *Licenciado en Matemáticas y Física*).
   - **Correo Electrónico** y **Teléfono Celular**.
3. Haz clic en **Guardar y Registrar Docente**.

#### 🤖 ¿Qué hace el sistema automáticamente?
- Crea un usuario con el formato: `doc_<NumeroDeDocumento>` (ejemplo: `doc_1098765432`).
- Asigna como contraseña provisional el **número de documento** del docente.
- Activa el indicador de seguridad `must_change_password=True`, de modo que cuando el docente ingrese por primera vez, el sistema le pedirá de forma obligatoria crear su contraseña personal secreta.
- Envía un correo automático de bienvenida si el servicio de correo está configurado.

#### 📌 Asignación de Carga Académica (Qué enseña cada docente)
- En la misma pantalla de **Cuerpo Docente**, haz clic en el botón verde **Asignar Carga Académica**.
- Selecciona el docente, el curso (ej. *9°-A*), la asignatura (ej. *Biología*) y marca si es el **Director de Grupo**.
- Pulsa **Guardar Asignación**. En ese instante, al docente le aparecerá el curso en su panel de calificaciones y llamado de lista.

---

### 4.2 Creación y Matrícula de Estudiantes / Aprendices

Existen **dos métodos** según la cantidad de alumnos a ingresar:

#### Método A: Registro Individual con Matrícula Inmediata (Uno a Uno)
*Ruta: Menú Lateral > Estructura Académica > Matrículas y Alumnos > Botón "Nuevo Alumno"*

1. Completa la ficha de ingreso:
   - Nombres y Apellidos completos.
   - Tipo de documento (Tarjeta de Identidad, Registro Civil, Cédula).
   - Número de documento.
   - Correo electrónico del estudiante o del acudiente.
   - **Curso / Salón a Matricular** (ej. *10°-B*).
   - **Código de Estudiante** (opcional; si se deja en blanco el sistema genera automáticamente uno como `ALU-2026-XXXX`).
   - Selección de Acudiente (si ya fue registrado).
2. Haz clic en **Confirmar Matrícula**.

#### 🤖 Credenciales automáticas generadas para el Estudiante:
- **Usuario:** `est_<NumeroDeDocumento>` o el código generado.
- **Contraseña Inicial:** El número de documento del alumno.
- **ID ÚNICO:** El código de matrícula asignado (ej. `ALU-2026-1001`).

---

#### Método B: Carga Masiva desde Archivo Excel / CSV (Recomendado para inicio de año)
*Ruta: Menú Lateral > Estructura Académica > Matrículas y Alumnos > Botón "Carga Masiva CSV"*

1. Haz clic en el botón **Descargar Plantilla Oficial CSV**.
2. Abre la plantilla en Microsoft Excel y llena las columnas:
   - `first_name` (Nombres)
   - `last_name` (Apellidos)
   - `document_type` (`TI`, `CC`, `RC`)
   - `document_number` (Número de documento sin puntos ni comas)
   - `email` (Correo electrónico)
   - `phone` (Teléfono)
   - `section_code` o `grade_level` (Código del curso o grado)
3. Guarda el archivo con formato `.csv` delimitado por comas.
4. En Academix, arrastra el archivo a la zona de carga masiva y haz clic en **Procesar e Importar Alumnos**.
5. El sistema creará en pocos segundos todos los usuarios, perfiles de estudiante y sus matrículas en el año lectivo activo.

---

### 4.3 Creación y Vinculación de Acudientes / Padres de Familia

El rol de acudiente permite que los padres sigan de cerca las notas, tareas y ausencias de sus hijos.

1. **Desde la Matrícula del Alumno:**  
   Al crear o editar al estudiante en el campo *Padre o Acudiente Responsable*, puedes asociar la cuenta de un padre registrado.
2. **Desde el Formulario de Registro:**  
   El padre puede registrarse indicando su documento y el **ID Único del Alumno** a vincular.
3. Una vez vinculado, el acudiente verá en su panel únicamente la información de su hijo (o selector si tiene más de uno en el colegio).

---

### 4.4 Panel de Administración Global de Usuarios

*Ruta: Menú Lateral > Administración y Marca > Gestión Usuarios*

Este módulo exclusivo de Rectoría y Administración permite:
- **Buscar cualquier cuenta** por nombre, apellido, cédula, correo o rol.
- **Filtrar por estado:** Activos o Inactivos.
- **Activar / Desactivar accesos con un clic:** Si un docente o estudiante se retira de la institución, pulsa el botón de estado para deshabilitar su cuenta de inmediato sin borrar su historial académico.
- **Auditar fechas de registro y último acceso**.

---

## 5. Comportamiento y Alcance de Cada Rol

| Rol en el Sistema | ¿Qué puede hacer? (Alcance Operativo) | ¿Qué NO puede hacer? (Límites de Seguridad) |
| :--- | :--- | :--- |
| 👑 **Administrador del Sistema** | • Control técnico integral de la plataforma.<br>• Creación de escuelas y gestión de usuarios.<br>• Consulta de bitácora de auditoría inmutable.<br>• Mantenimiento y configuración del servidor. | No debe alterar calificaciones de periodos cerrados sin orden directiva y justificación registrada en auditoría. |
| 🏛️ **Directivo / Rector** | • Control global institucional y toma de decisiones.<br>• Apertura y **cierre oficial de periodos lectivos**.<br>• Supervisión de sábanas consolidadas y cuadro de honor.<br>• Personalización de marca, escudo y paleta visual.<br>• Aprobación de planes de estudio y mallas curriculares. | No dicta clases directamente salvo que se asigne carga docente. |
| 📋 **Secretaría Académica** | • Matrícula individual y masiva de estudiantes.<br>• Gestión de expedientes digitales y observador del alumno.<br>• Emisión e impresión de certificados y boletines de notas.<br>• Registro de docentes y soporte a padres de familia. | No puede cerrar periodos lectivos ni cambiar temas de marca global. |
| 👨‍🏫 **Docente / Instructor** | • Planilla de notas interactiva en vivo.<br>• Llamado de lista diario con 4 estados (P, A, J, T).<br>• Publicación de tareas con archivos adjuntos.<br>• Calificación y retroalimentación de trabajos de alumnos.<br>• Visualización de la sábana de notas (si es Director de Grupo). | Solo puede calificar y llamar lista en los cursos y materias que tiene formalmente asignados. No puede modificar notas de periodos ya cerrados. |
| 🎓 **Estudiante / Aprendiz** | • Consulta de calificaciones parciales y definitivas.<br>• Carga y entrega de tareas con documentos adjuntos.<br>• Verificación de comentarios y notas de profesores.<br>• Seguimiento a su récord de asistencias.<br>• Descarga de su boletín de calificaciones oficial con QR. | No puede ver calificaciones ni información de otros estudiantes. No puede enviar tareas después de la fecha límite establecida. |
| 👨‍👩‍👧 **Padre de Familia / Acudiente** | • Monitoreo en tiempo real del rendimiento de su acudido.<br>• Alertas tempranas sobre inasistencias y tareas pendientes.<br>• Selector para alternar entre varios hijos en el colegio.<br>• Descarga de boletines periódicos de sus hijos. | Solo tiene acceso de lectura supervisora; no puede modificar registros ni calificaciones. |

---

## 6. Flujo de Trabajo Cotidiano durante el Periodo Escolar

### Día a Día (Docentes)
1. **Inicio de clase:** El profesor ingresa desde su computador o teléfono a *Llamado de Lista*, selecciona la clase y en menos de 30 segundos guarda las ausencias o retardos.
2. **Tareas y Actividades:** Crea la actividad indicando instrucciones y fecha límite; los alumnos la reciben de inmediato en su panel.
3. **Calificación:** Ingresa a *Planilla de Notas*, escribe las notas obtenidas en talleres o evaluaciones y pulsa *Guardar*. El sistema calcula promedios y porcentajes en vivo.

### Al Término de Cada Periodo (Rectoría y Secretaría)
1. **Auditoría de digitación:** Rectoría verifica qué docentes tienen planillas completas.
2. **Cierre de Periodo:** Desde *Cierres y Promoción*, el Rector pulsa **Cerrar Periodo**. A partir de ese momento, las notas quedan congeladas y protegidas contra alteraciones.
3. **Emisión de Boletines:** Secretaría va a *Reportes > Boletines por Sección*, selecciona el curso y genera en bloque los PDF oficiales con escudo, notas y observaciones listos para entregar a los acudientes.
4. **Sábana de Notas:** Se exporta a Excel el consolidado de todo el plantel para el archivo reglamentario institucional.

---

## 7. Mantenimiento, Copias de Seguridad y Soporte

### 💾 ¿Cómo realizar copias de seguridad (Backups)?
La base de datos de Academix almacena toda la vida académica del plantel. Se recomienda realizar una copia de seguridad semanal:
- **Respaldo Rápido:** Copia el archivo `db.sqlite3` ubicado en la carpeta principal del sistema a una memoria USB o disco externo seguro.
- **Respaldo SQL:** Ejecuta el comando de exportación o conserva el archivo `academix_db_backup.sql`.

### 🌐 ¿Cómo reiniciar el servidor en red?
Si el computador principal se apaga o reinicia:
1. Enciende el equipo servidor.
2. Haz doble clic en el archivo `iniciar_servidor_red.bat`.
3. Se abrirá una ventana de consola indicando la dirección IP activa (ej. `http://192.168.1.50:8000`).
4. ¡El sistema estará nuevamente en línea para toda la institución!

---
**ACADEMIX 2026** — *Tecnología al servicio de la calidad educativa.*  
*Entrega formal completada y certificada para operación en producción.*
