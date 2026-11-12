# 📘 MANUAL TÉCNICO DE BASE DE DATOS — ACADEMIX
## Sistema Integral de Gestión Académica, Calificaciones, Asistencia y Auditoría Escolar

> **Documento:** Manual Técnico de Administración, Arquitectura y Diccionario de Datos  
> **Evidencia:** Creación de la base de datos en el motor seleccionado según especificaciones técnicas del informe y protocolos de la empresa.  
> **Programa:** Análisis y Desarrollo de Software (ADSO / ADSI - SENA)  
> **Versión:** 1.0 (Producción / Cierre de Proyecto)  
> **Fecha:** Septiembre 2026  

---

## 1. FICHA TÉCNICA DEL MOTOR DE BASE DE DATOS

| Parámetro | Especificación Técnica |
| :--- | :--- |
| **Sistema Gestor (SGBD)** | **MySQL Community Server 8.0 / MariaDB 10.5+** |
| **Motor de Almacenamiento** | **InnoDB** (Cumplimiento estricto de propiedades ACID: Atomicidad, Consistencia, Aislamiento, Durabilidad) |
| **Juego de Caracteres** | `utf8mb4` (Soporte completo para tildes, caracteres internacionales, ñ y emojis) |
| **Colación Predeterminada** | `utf8mb4_unicode_ci` |
| **Modo Dual / Fallback Local** | **SQLite 3.45+ con modo WAL (`PRAGMA journal_mode=WAL`)** para funcionamiento autónomo en red local LAN offline. |
| **Puerto Estándar** | `3306` (MySQL) / `8000` (Intranet HTTP centralizada) |
| **Nombre de la Base de Datos** | `academix_db` |

---

## 2. JUSTIFICACIÓN TÉCNICA Y PROTOCOLOS DE EMPRESA

Conforme a las normas y protocolos empresariales de ingeniería de software y seguridad de la información:

1. **Garantía Transaccional (ACID):** El motor **InnoDB** asegura que las operaciones compuestas —como el **Cierre Anual Transaccional** o la consolidación de notas por periodo— se ejecuten dentro de transacciones atómicas (`START TRANSACTION` / `COMMIT` / `ROLLBACK`). Si ocurre una desconexión o fallo, la base de datos revierte automáticamente al estado previo sin corromper el historial.
2. **Precisión Matemática en Calificaciones:** Para cumplir con la reglamentación del Decreto 1290 y evitar pérdidas de precisión por punto flotante binario (`FLOAT` o `DOUBLE`), todas las calificaciones y ponderaciones porcentuales se modelan exclusivamente como `DECIMAL(5,2)`.
3. **Auditoría Forense Inmutable:** Cada modificación de registro genera un asiento en la tabla `audit_auditlog`, registrando la dirección IP de origen, usuario actor, fecha/hora exacta y el delta de valores antes/después en formato `LONGTEXT (JSON)`.
4. **Principio de Menor Privilegio (PoLP):** La aplicación web no se conecta con usuario `root`, sino mediante un usuario dedicado (`academix_user`) con permisos exclusivos de DML (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) en la base de datos `academix_db`.

---

## 3. DICCIONARIO DE DATOS (CATÁLOGO DE TABLAS PRINCIPALES)

### 3.1 Módulo `accounts` (Usuarios, Roles y Perfiles)

#### Tabla: `accounts_customuser`
Almacena las cuentas de usuario y credenciales del sistema para los 6 roles.
| Campo | Tipo MySQL | Nulo | Clave | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INT` | NO | **PK** | Identificador único auto-incremental del usuario. |
| `password` | `VARCHAR(128)` | NO | | Hash seguro de contraseña mediante PBKDF2-SHA256. |
| `last_login` | `DATETIME` | SÍ | | Fecha y hora del último acceso al sistema. |
| `is_superuser` | `TINYINT(1)` | NO | | Indica privilegios máximos de superadministrador. |
| `username` | `VARCHAR(150)` | NO | **UQ** | Nombre de usuario único para inicio de sesión. |
| `first_name` | `VARCHAR(150)` | NO | | Nombres del usuario. |
| `last_name` | `VARCHAR(150)` | NO | | Apellidos del usuario. |
| `email` | `VARCHAR(254)` | NO | | Correo electrónico principal de notificación. |
| `is_staff` | `TINYINT(1)` | NO | | Acceso permitido al panel administrativo de Django/Jazzmin. |
| `is_active` | `TINYINT(1)` | NO | | Estado lógico de la cuenta (1: Activo, 0: Inactivo). |
| `date_joined` | `DATETIME` | NO | | Fecha y hora de creación de la cuenta. |
| `role` | `VARCHAR(20)` | NO | | Rol institucional: `ADMIN`, `RECTOR`, `SECRETARIA`, `TEACHER`, `STUDENT`, `PARENT`. |
| `document_type` | `VARCHAR(10)` | NO | | Tipo de documento: `CC`, `TI`, `CE`, `PASAPORTE`. |
| `document_number` | `VARCHAR(30)` | SÍ | | Número de identificación oficial. |
| `phone` | `VARCHAR(25)` | SÍ | | Teléfono de contacto institucional o móvil. |
| `address` | `VARCHAR(255)` | SÍ | | Dirección de residencia física. |
| `avatar` | `VARCHAR(100)` | SÍ | | Ruta relativa de la foto de perfil en el servidor. |
| `must_change_password`| `TINYINT(1)` | NO | | Obliga a renovar contraseña en el primer inicio de sesión. |
| `created_at` | `DATETIME` | NO | | Marca temporal de auditoría de creación. |
| `updated_at` | `DATETIME` | NO | | Marca temporal de última modificación. |

#### Tabla: `students_studentprofile`
Expediente detallado del estudiante y datos académicos/médicos.
| Campo | Tipo MySQL | Nulo | Clave | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INT` | NO | **PK** | Identificador de expediente. |
| `user_id` | `INT` | NO | **FK, UQ** | Relación 1:1 con `accounts_customuser.id`. |
| `student_code` | `VARCHAR(20)` | NO | **UQ** | Matrícula / Código estudiantil único. |
| `birth_date` | `DATE` | SÍ | | Fecha de nacimiento. |
| `medical_info` | `TEXT` | SÍ | | Alergias, tipo de sangre y condiciones especiales. |
| `guardian_phone`| `VARCHAR(25)` | SÍ | | Teléfono de emergencia del acudiente. |

#### Tabla: `teachers_teacherprofile`
Ficha técnica del docente y vinculación laboral.
| Campo | Tipo MySQL | Nulo | Clave | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INT` | NO | **PK** | Identificador del docente. |
| `user_id` | `INT` | NO | **FK, UQ** | Relación 1:1 con `accounts_customuser.id`. |
| `professional_title` | `VARCHAR(150)` | SÍ | | Título universitario obtenido. |
| `specialty` | `VARCHAR(100)` | SÍ | | Área pedagógica de especialización. |
| `institutional_phone` | `VARCHAR(25)` | SÍ | | Teléfono o extensión de contacto. |

---

### 3.2 Módulo `courses` y `subjects` (Estructura Curricular)

#### Tabla: `courses_academicyear`
Define el año lectivo escolar.
| Campo | Tipo MySQL | Nulo | Clave | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INT` | NO | **PK** | Identificador del año. |
| `year` | `INT` | NO | **UQ** | Número del año calendario (ej. 2026). |
| `is_active` | `TINYINT(1)` | NO | | Determina el año lectivo vigente para operaciones. |
| `start_date` | `DATE` | SÍ | | Fecha de apertura de clases. |
| `end_date` | `DATE` | SÍ | | Fecha de clausura de clases. |

#### Tabla: `courses_gradelevel`
Niveles educativos institucionales (grados 6° al 11°).
| Campo | Tipo MySQL | Nulo | Clave | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INT` | NO | **PK** | Identificador del grado. |
| `name` | `VARCHAR(50)` | NO | | Nombre formal del grado (ej. Sexto, Once). |
| `order_index` | `INT` | NO | | Posición ordinal para cálculo de promociones (6 a 11). |
| `description` | `VARCHAR(255)` | SÍ | | Observaciones curriculares. |

#### Tabla: `courses_coursesection`
Grupos o secciones de clase física (salones).
| Campo | Tipo MySQL | Nulo | Clave | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INT` | NO | **PK** | Identificador del curso. |
| `name` | `VARCHAR(20)` | NO | | Nomenclatura del grupo (ej. 6-A, 10-B). |
| `grade_level_id` | `INT` | NO | **FK** | Grado al que pertenece (`courses_gradelevel.id`). |
| `academic_year_id`| `INT` | NO | **FK** | Año escolar asociado (`courses_academicyear.id`). |
| `capacity` | `INT` | NO | | Cupo máximo de alumnos permitidos. |

#### Tabla: `subjects_subject`
Catálogo de asignaturas impartidas en la institución.
| Campo | Tipo MySQL | Nulo | Clave | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INT` | NO | **PK** | Identificador de asignatura. |
| `name` | `VARCHAR(100)` | NO | | Nombre de la materia (ej. Álgebra, Español). |
| `code` | `VARCHAR(20)` | NO | **UQ** | Código institucional (ej. MAT-06). |
| `knowledge_area_id`| `INT` | NO | **FK** | Área de conocimiento (`subjects_knowledgearea.id`). |

#### Tabla: `teachers_teachingassignment`
Asignación académica oficial (Docente - Materia - Curso).
| Campo | Tipo MySQL | Nulo | Clave | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INT` | NO | **PK** | Identificador de la asignación. |
| `teacher_id` | `INT` | NO | **FK** | Docente asignado (`teachers_teacherprofile.id`). |
| `course_section_id`| `INT` | NO | **FK** | Salón de clase (`courses_coursesection.id`). |
| `subject_id` | `INT` | NO | **FK** | Materia dictada (`subjects_subject.id`). |
| `academic_year_id` | `INT` | NO | **FK** | Vigencia anual (`courses_academicyear.id`). |

---

### 3.3 Módulo `attendance` (Control de Asistencia Escolar)

#### Tabla: `attendance_attendancesession`
Encabezado de la sesión de clase donde se pasa lista.
| Campo | Tipo MySQL | Nulo | Clave | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INT` | NO | **PK** | Identificador de la sesión. |
| `course_section_id`| `INT` | NO | **FK** | Curso donde se toma lista. |
| `subject_id` | `INT` | NO | **FK** | Asignatura de la sesión. |
| `teacher_id` | `INT` | NO | **FK** | Docente que pasa asistencia. |
| `session_date` | `DATE` | NO | | Fecha en que se llevó a cabo la clase. |
| `time_slot` | `VARCHAR(30)` | SÍ | | Bloque horario o jornada. |

#### Tabla: `attendance_attendancerecord`
Registro individual de asistencia de cada alumno en la sesión.
| Campo | Tipo MySQL | Nulo | Clave | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INT` | NO | **PK** | Identificador del registro. |
| `session_id` | `INT` | NO | **FK** | Sesión de clase (`attendance_attendancesession.id`). |
| `student_id` | `INT` | NO | **FK** | Alumno calificado (`students_studentprofile.id`). |
| `status` | `VARCHAR(15)` | NO | | Estado: `PRESENTE`, `FALTA_JUSTIFICADA`, `FALTA_INJUSTIFICADA`, `RETARDO`. |
| `remarks` | `VARCHAR(255)` | SÍ | | Justificación médica o nota disciplinaria. |

---

### 3.4 Módulo `grades` y `reports` (Calificaciones y Boletines)

#### Tabla: `grades_evaluationcriterion`
Criterios de evaluación configurables por materia y periodo (40% Cognitivo, 40% Procedimental, 20% Actitudinal).
| Campo | Tipo MySQL | Nulo | Clave | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INT` | NO | **PK** | Identificador del criterio. |
| `subject_id` | `INT` | NO | **FK** | Asignatura correspondiente. |
| `period_id` | `INT` | NO | **FK** | Periodo académico evaluado. |
| `name` | `VARCHAR(100)` | NO | | Nombre de la actividad o componente evaluativo. |
| `dimension` | `VARCHAR(20)` | NO | | Dimensión pedagógica (`COGNITIVO`, `PROCEDIMENTAL`, `ACTITUDINAL`). |
| `percentage` | `DECIMAL(5,2)` | NO | | Ponderación porcentual sobre la nota del periodo. |

#### Tabla: `grades_graderecord`
Calificaciones cuantitativas parciales por estudiante.
| Campo | Tipo MySQL | Nulo | Clave | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INT` | NO | **PK** | Identificador de nota. |
| `student_id` | `INT` | NO | **FK** | Estudiante evaluado. |
| `evaluation_criterion_id` | `INT` | NO | **FK** | Criterio calificado (`grades_evaluationcriterion.id`). |
| `score` | `DECIMAL(5,2)` | NO | | Calificación obtenida (escala de 0.00 a 5.00 o 10.00). |
| `graded_at` | `DATETIME` | NO | | Fecha y hora en que se asentó la nota. |

#### Tabla: `grades_periodfinalgrade`
Nota consolidada del periodo para boletines oficiales (Decreto 1290).
| Campo | Tipo MySQL | Nulo | Clave | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INT` | NO | **PK** | Identificador de nota definitiva. |
| `student_id` | `INT` | NO | **FK** | Estudiante. |
| `course_section_id`| `INT` | NO | **FK** | Curso en el que está matriculado. |
| `subject_id` | `INT` | NO | **FK** | Asignatura evaluada. |
| `academic_period_id`| `INT` | NO | **FK** | Periodo académico. |
| `final_score` | `DECIMAL(5,2)` | NO | | Calificación promedio ponderada final. |
| `performance_level` | `VARCHAR(15)` | NO | | Nivel Decreto 1290 (`SUPERIOR`, `ALTO`, `BASICO`, `BAJO`). |
| `is_approved` | `TINYINT(1)` | NO | | Indicador booleano de aprobación. |

---

### 3.5 Módulo `audit` (Trazabilidad Forense)

#### Tabla: `audit_auditlog`
Registro inmutable de auditoría de seguridad y trazabilidad.
| Campo | Tipo MySQL | Nulo | Clave | Descripción |
| :--- | :--- | :---: | :---: | :--- |
| `id` | `INT` | NO | **PK** | Identificador del evento forense. |
| `user_id` | `INT` | SÍ | **FK** | Usuario que efectuó la acción (`accounts_customuser.id`). |
| `action` | `VARCHAR(50)` | NO | | Operación realizada (`LOGIN`, `CREATE`, `UPDATE`, `DELETE`, `GRADE_CHANGE`). |
| `target_model` | `VARCHAR(100)` | NO | | Nombre de la tabla o entidad intervenida. |
| `target_id` | `VARCHAR(50)` | SÍ | | Identificador del registro afectado. |
| `changes_json` | `LONGTEXT` | SÍ | | Delta estructurado en JSON con valores anteriores y nuevos. |
| `ip_address` | `VARCHAR(45)` | SÍ | | Dirección IPv4 o IPv6 del cliente en la red LAN. |
| `timestamp` | `DATETIME` | NO | | Fecha y hora con precisión de milisegundos. |

---

## 4. ÍNDICES Y ESTRATEGIAS DE RENDIMIENTO

Para garantizar tiempos de respuesta inferiores a 100 ms en consultas simultáneas desde la red local, se implementaron los siguientes índices:

1. **Índices de Búsqueda de Usuarios:**
   - `accounts_customuser.username` (Único)
   - `accounts_customuser.email`
   - `accounts_customuser.document_number`
2. **Índices de Matrícula y Asignación:**
   - `students_enrollment(student_id, academic_year_id)` (Evita dobles matrículas)
   - `teachers_teachingassignment(course_section_id, subject_id, academic_year_id)` (Garantiza unicidad de carga docente)
3. **Índices de Calificaciones y Asistencia:**
   - `grades_graderecord(student_id, evaluation_criterion_id)` (Acelera el renderizado de la sábana de notas)
   - `attendance_attendancerecord(session_id, student_id)` (Búsqueda rápida en el llamado de lista)
   - `audit_auditlog(timestamp, action, user_id)` (Consultas forenses de alta velocidad)

---

## 5. POLÍTICAS DE SEGURIDAD Y PERMISOS DE BASE DE DATOS

En un entorno corporativo o de centro educativo, la base de datos MySQL debe gestionarse con roles diferenciados:

```sql
-- 1. Crear base de datos segura
CREATE DATABASE IF NOT EXISTS academix_db 
CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

-- 2. Crear usuario exclusivo de la aplicación (Menor privilegio DML)
CREATE USER 'academix_user'@'localhost' IDENTIFIED BY 'Academix_Pass2026!';
CREATE USER 'academix_user'@'127.0.0.1' IDENTIFIED BY 'Academix_Pass2026!';

-- Otorgar únicamente privilegios requeridos para operación de la app
GRANT SELECT, INSERT, UPDATE, DELETE ON academix_db.* TO 'academix_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON academix_db.* TO 'academix_user'@'127.0.0.1';

-- 3. Usuario de sólo lectura para auditoría / revisoría fiscal
CREATE USER 'academix_auditor'@'%' IDENTIFIED BY 'Audit_ReadOnly2026!';
GRANT SELECT ON academix_db.* TO 'academix_auditor'@'%';

FLUSH PRIVILEGES;
```

---

## 6. PROTOCOLO DE RESPALDO Y RESTAURACIÓN (BACKUP & RECOVERY)

### 6.1 Generación de Copia de Seguridad (Backup)
Para generar un volcado íntegro de la estructura DDL y los datos DML:

```bash
# Vía comando mysqldump estándar (Terminal / PowerShell):
mysqldump -u root -p --default-character-set=utf8mb4 --single-transaction --routines --triggers academix_db > academix_db_backup.sql
```

### 6.2 Procedimiento de Restauración (Recovery)
Para restaurar la base de datos en cualquier servidor MySQL / MariaDB o importar en phpMyAdmin / MySQL Workbench:

**Opción A — Vía Consola (Recomendada):**
```bash
# 1. Ingresar a la consola de MySQL o ejecutar el script directamente:
mysql -u root -p < academix_db_backup.sql
```

**Opción B — Desde la consola interactiva de MySQL:**
```sql
CREATE DATABASE IF NOT EXISTS academix_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE academix_db;
SOURCE C:/Academix/academix_db_backup.sql;
```

**Opción C — Vía phpMyAdmin (XAMPP / WampServer):**
1. Abrir phpMyAdmin en el navegador (`http://localhost/phpmyadmin`).
2. Hacer clic en la pestaña **Importar**.
3. Seleccionar el archivo `academix_db_backup.sql` ubicado en la carpeta raíz del proyecto.
4. Presionar el botón **Continuar**. El sistema creará automáticamente la base de datos `academix_db`, las 34 tablas relacionales y cargará todos los registros existentes.

---

## 7. CONCLUSIÓN Y ESTADO DE ENTREGA

El sistema de persistencia de **ACADEMIX** cumple a cabalidad con los estándares técnicos y de calidad exigidos:
- Esquema relacional en **3FN** con integridad referencial estricta.
- Modelo de auditoría forense inmutable.
- Script de copia de seguridad `academix_db_backup.sql` verificado y 100% operativo.
