# GUÍA MAESTRA DE DEFENSA TÉCNICA Y RESOLUCIÓN DE SABOTAJES EN VIVO
## Manual de Dominio Total del Código Fuente de ACADEMIX para la Evaluación Individual del Instructor
### Proyecto: ACADEMIX v2.5.1 — Plataforma de Gestión Escolar y Control Académico
**Programa:** Tecnología en Análisis y Desarrollo de Software (ADSO) | **Ficha:** 3173430  
**Dirigido a las 3 Integrantes:** Sofia Helena Torres, Julián Esteban Rocha / Integrante 2, Integrante 3  
**Objetivo de Supervivencia:** Responder con precisión qué hace cada línea, función y archivo, identificar inmediatamente **qué se daña** cuando el profesor altere el código en vivo, diagnosticar el error en consola/pantalla y **repararlo en segundos**.

---

## 🧭 LA FÓRMULA DE RESPUESTA EN 4 PASOS ANTE EL PROFESOR

Cuando el instructor señale una función, borre una línea o cambie un valor para "dañar el sistema", **ninguna debe quedarse callada ni dudar**. Deben aplicar inmediatamente esta estructura de respuesta profesional:

```
┌────────────────────────────────────────────────────────────────────────────────────────────────────┐
│                         FÓRMULA DE RESPUESTA ANTE EL SABOTAJE DEL PROFESOR                         │
├────────────────────────────────────────────────────────────────────────────────────────────────────┤
│  1. QUÉ HACE:       "Profesor, ese bloque/función se encarga de [Función exacta en el sistema]."    │
│  2. QUÉ DAÑÓ:       "Al modificar/borrar esa línea, usted acaba de romper [Mecanismo afectado]."   │
│  3. QUÉ ERROR DA:   "En pantalla/consola saldrá un error [Nombre de la Excepción / Código HTTP]."  │
│  4. CÓMO SE ARREGLA:"Para solucionarlo, la línea correcta que debe restaurarse es [Código exacto]."│
└────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

# ÍNDICE GENERAL DEL CÓDIGO POR MÓDULOS CRÍTICOS

1. [El Cerebro del Sistema: `config/settings.py` y `config/urls.py`](#1-el-cerebro-del-sistema-configsettingspy-y-configurlspy)
2. [Autenticación, Usuarios y Control de Acceso: `apps/accounts/`](#2-autenticación-usuarios-y-control-de-acceso-appsaccounts)
3. [Motor Curricular, Calificaciones y RAPs al 100%: `apps/grades/`](#3-motor-curricular-calificaciones-y-raps-al-100-appsgrades)
4. [Control de Periodos y Años Lectivos: `apps/periods/`](#4-control-de-periodos-y-años-lectivos-appsperiods)
5. [Carga Masiva Transaccional y Expedientes: `apps/students/`](#5-carga-masiva-transaccional-y-expedientes-appsstudents)
6. [Boletines Oficiales PDF y Verificación QR: `apps/reports/`](#6-boletines-oficiales-pdf-y-verificación-qr-appsreports)
7. [Asistencia, Disciplina y Trazabilidad: `apps/attendance/` y `apps/audit/`](#7-asistencia-disciplina-y-trazabilidad-appsattendance-y-appsaudit)
8. [Vistas Visuales, Formularios y Seguridad Web: `templates/`](#8-vistas-visuales-formularios-y-seguridad-web-templates)
9. [Comandos de Rescate en Consola (Cheatsheet de Terminal)](#9-comandos-de-rescate-en-consola-cheatsheet-de-terminal)
10. [Top 20 de Sabotajes Más Probables del Profesor con Pregunta y Respuesta Exacta](#10-top-20-de-sabotajes-más-probables-del-profesor-con-pregunta-y-respuesta-exacta)

---

# 1. EL CEREBRO DEL SISTEMA: `config/settings.py` y `config/urls.py`

## 1.1 `config/settings.py` (Configuración Maestra)

### A. `AUTH_USER_MODEL = 'accounts.CustomUser'`
- **¿Qué hace exactamente?:** Le indica a Django que no utilice su tabla de usuarios por defecto (`auth_user`), sino nuestro modelo personalizado `CustomUser` ubicado en `apps/accounts/models.py`, el cual tiene los roles (`RECTOR`, `DOCENTE`, `ESTUDIANTE`, etc.), el tipo de documento y el vínculo con la escuela.
- **¿Qué pasa si el profesor lo borra o comenta?:**
  - **Error en Consola:** `ValueError: Dependency on app with no migrations: accounts` o `InconsistentMigrationHistory`. Si el servidor arranca, lanzará `AttributeError: 'User' object has no attribute 'role'` en cada vista que consulte el rol del usuario.
  - **Qué daña en el sistema:** Destruye todo el sistema de roles RBAC. Ninguna vista puede saber si quien entra es rector, docente o acudiente.
  - **Cómo se arregla:**
    ```python
    AUTH_USER_MODEL = 'accounts.CustomUser'
    ```

### B. `INSTALLED_APPS` (Aplicaciones Registradas)
- **¿Qué hace exactamente?:** Es la lista donde se declaran las librerías base de Django y nuestras 15 micro-aplicaciones (`apps.accounts`, `apps.grades`, `apps.students`, `apps.courses`, etc.). Si una app no está en esta lista, para Django no existe.
- **¿Qué pasa si el profesor borra `'apps.grades'`?:**
  - **Error en Consola:** `LookupError: No installed app with label 'grades'`.
  - **Error en el Navegador:** `TemplateSyntaxError` al intentar cargar cualquier pantalla que use modelos o tags de calificaciones.
  - **Qué daña:** Desconecta completamente el módulo de notas. Las URLs de notas dejan de funcionar y la base de datos no reconoce las tablas `grades_graderecord`.
  - **Cómo se arregla:** Volver a agregar `'apps.grades'` dentro de la lista `INSTALLED_APPS`.

### C. `MIDDLEWARE` (Los Guardianes de Peticiones HTTP)
En `settings.py`, la lista `MIDDLEWARE` procesa cada clic o envío de formulario antes de llegar a la vista y antes de salir al navegador:
1. `'django.middleware.security.SecurityMiddleware'`: Activa cabeceras de seguridad XSS y redirección HTTPS.
2. `'django.contrib.sessions.middleware.SessionMiddleware'`: Gestiona las cookies de sesión (mantiene al usuario conectado).
   - *Si el profesor lo quita:* `AttributeError: 'WSGIRequest' object has no attribute 'session'`. El login se vuelve imposible.
3. `'django.middleware.csrf.CsrfViewMiddleware'`: Protege contra ataques de falsificación de petición en sitios cruzados.
   - *Si el profesor lo quita:* El sistema queda vulnerable a ataques CSRF donde un atacante puede ejecutar acciones a nombre de la rectora sin su conocimiento.
4. `'django.contrib.auth.middleware.AuthenticationMiddleware'`: Asocia el usuario autenticado con la variable `request.user`.
   - *Si el profesor lo quita:* **Fallo catastrófico.** Salta: `AttributeError: 'WSGIRequest' object has no attribute 'user'`. El 100% de las vistas fallan porque ninguna puede saber quién está logueado.
   - *Cómo se arregla:* Restaurar `'django.contrib.auth.middleware.AuthenticationMiddleware'` en su posición dentro de `MIDDLEWARE`.

### D. `DATABASES` (Conexión al Motor Relacional)
- **¿Qué hace exactamente?:** Define el motor y las credenciales de la base de datos. En desarrollo local usa `sqlite3` (`db.sqlite3`), y en producción en Render usa `django.db.backends.postgresql` leyendo `DATABASE_URL`.
- **¿Qué pasa si el profesor cambia el `'ENGINE'` o borra el `'NAME'`?:**
  - **Error:** `django.db.utils.OperationalError: no such table` o `ImproperlyConfigured`.
  - **Qué daña:** La aplicación no puede leer ni guardar un solo dato.
  - **Cómo se arregla:**
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    ```

### E. `DEBUG = True` y `ALLOWED_HOSTS`
- **¿Qué hace exactamente?:** `DEBUG = True` activa la pantalla amarilla detallada con el rastro de errores para desarrolladores. `ALLOWED_HOSTS` define qué dominios o IPs pueden consultar el servidor.
- **¿Qué pasa si el profesor pone `DEBUG = False` y deja `ALLOWED_HOSTS = []`?:**
  - **Error en Pantalla:** `Bad Request (400) - Invalid HTTP_HOST header`.
  - **Qué daña:** Nadie puede entrar al servidor por red ni por `localhost`.
  - **Cómo se arregla:** En desarrollo poner `DEBUG = True` o definir `ALLOWED_HOSTS = ['*']` o `['localhost', '127.0.0.1']`.

---

## 1.2 `config/urls.py` (El Enrutador Maestro)

- **¿Qué hace exactamente?:** Es la tabla de enrutamiento principal. Usa la función `include()` para delegar las sub-rutas a cada aplicación:
  ```python
  path('accounts/', include('apps.accounts.urls')),
  path('grades/', include('apps.grades.urls')),
  path('students/', include('apps.students.urls')),
  path('reports/', include('apps.reports.urls')),
  ```
- **¿Qué pasa si el profesor borra la coma al final de una línea o cambia el string `include('apps.grades.urls')`?:**
  - Si borra la coma: `SyntaxError: invalid syntax` en la consola al arrancar.
  - Si cambia el path: Al dar clic en Calificaciones saldrá **HTTP 404 Page Not Found** ("The current path, grades/, didn't match any of these").
  - **Cómo se arregla:** Restaurar la ruta correcta con su `include()` y verificar que el archivo `apps/grades/urls.py` tenga definido `app_name = 'grades'`.

---

# 2. AUTENTICACIÓN, USUARIOS Y CONTROL DE ACCESO: `apps/accounts/`

## 2.1 `apps/accounts/models.py`

### A. Modelo `School` (Multi-Escuela / SaaS)
```python
class School(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
```
- **¿Qué hace?:** Permite que una sola instalación de Academix atienda a múltiples colegios de forma aislada.
- **Sabotaje del Profesor:** Quita `unique=True` en `code`.
  - **Qué daña:** Permite registrar dos colegios con el mismo código, provocando que los estudiantes de una escuela terminen matriculados en otra.
  - **Solución:** Restaurar `unique=True`.

### B. Modelo `CustomUser(AbstractUser)`
```python
class CustomUser(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        RECTOR = 'RECTOR', 'Directivo / Rector'
        SECRETARIA = 'SECRETARIA', 'Secretaría Académica'
        TEACHER = 'TEACHER', 'Docente'
        STUDENT = 'STUDENT', 'Estudiante'
        PARENT = 'PARENT', 'Padre de Familia / Acudiente'

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.STUDENT, db_index=True)
    document_number = models.CharField(max_length=30, unique=True, null=True, blank=True)
    school = models.ForeignKey('School', on_delete=models.SET_NULL, null=True, blank=True)
```
- **¿Qué hace?:** Define los 6 roles oficiales del colegio y almacena el documento de identidad único.
- **Properties clave:**
  ```python
  @property
  def is_teacher(self):
      return self.role == self.Role.TEACHER

  @property
  def is_student(self):
      return self.role == self.Role.STUDENT

  @property
  def is_rector(self):
      return self.role == self.Role.RECTOR
  ```
- **Sabotaje 1 del Profesor:** Borra el decorador `@property` en `def is_teacher(self):`.
  - **Qué daña:** Cuando en las plantillas o vistas se evalúa `if user.is_teacher:`, Python no ejecuta el método sino que evalúa el objeto función, el cual siempre da `True`. Como consecuencia, ¡los estudiantes tendrían permisos de docentes! Y en vistas con llamada `user.is_teacher()` daría `TypeError: 'bool' object is not callable` si antes estaba como propiedad.
  - **Solución:** Asegurar que tenga siempre el decorador `@property`.
- **Sabotaje 2 del Profesor:** Cambia `school = models.ForeignKey(..., on_delete=models.SET_NULL, null=True, blank=True)` por `on_delete=models.CASCADE`.
  - **Qué daña:** **Desastre total.** Si un rector borra una sede o escuela, ¡se eliminan automáticamente en cascada todos los usuarios, profesores y alumnos asociados a ella!
  - **Solución:** Mantener `on_delete=models.SET_NULL` para proteger los registros de personas.

---

## 2.2 `apps/accounts/views.py`

### A. Vista `login_view(request)`
```python
@ratelimit(key='ip', rate='5/m', block=True)
def login_view(request):
    if request.method == 'POST':
        # Validación de credenciales y autenticación
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Redirección inteligente según rol
```
- **¿Qué hace?:** Valida usuario y contraseña, restringe ataques por fuerza bruta (5 intentos por minuto por IP con HTTP 429) y redirige a cada persona a su dashboard específico (docente a sus materias, alumno a sus notas).
- **Sabotaje 1 del Profesor:** Comenta la línea `login(request, user)`.
  - **Qué daña:** El usuario escribe usuario y clave correctos, la página recarga pero nunca inicia sesión. Sigue apareciendo en el login porque la sesión nunca se guardó en la cookie.
  - **Solución:** Descomentar `login(request, user)`.
- **Sabotaje 2 del Profesor:** Quita el decorador `@ratelimit(...)`.
  - **Qué daña:** Deja el sistema vulnerable a ataques de fuerza bruta automatizados (Violación de la norma OWASP Top 10 A07 y Hallazgo HAL-01 de la auditoría).
  - **Solución:** Reincorporar el decorador `@ratelimit(key='ip', rate='5/m', block=True)`.

---

# 3. MOTOR CURRICULAR, CALIFICACIONES Y RAPS AL 100%: `apps/grades/`

Este es el módulo que **más le gusta preguntar a los profesores del SENA**, porque aquí está la matemática del sistema y la normativa del Decreto 1290 de 2009.

## 3.1 `apps/grades/models.py`

### A. Modelo `EvaluationCriterion` (Criterios / RAPs)
```python
class EvaluationCriterion(models.Model):
    course_section = models.ForeignKey('courses.CourseSection', on_delete=models.CASCADE)
    subject = models.ForeignKey('subjects.Subject', on_delete=models.CASCADE)
    academic_period = models.ForeignKey('periods.AcademicPeriod', on_delete=models.CASCADE)
    name = models.CharField(max_length=100) # Ej: RAP 1: Lógica de programación
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01')), MaxValueValidator(Decimal('100.00'))]
    )
    order = models.PositiveSmallIntegerField(default=1)
    norm = models.ForeignKey('subjects.SubjectNorm', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        unique_together = ('course_section', 'subject', 'academic_period', 'name')
```
- **¿Qué hace?:** Representa cada columna de la planilla de notas (los RAPs o actividades). Cada una tiene un porcentaje que debe sumar el 100% del periodo.
- **Sabotaje 1 del Profesor:** Cambia `DecimalField` por `FloatField`.
  - **Qué daña:** Introduce **errores de redondeo binario** propios de los números de coma flotante en computadores (ej: `3.3000000000000003` en vez de `3.30`). Los porcentajes nunca sumarían 100.00% exactos sino 99.999999%, bloqueando el cierre del periodo.
  - **Solución:** Usar siempre `DecimalField(max_digits=5, decimal_places=2)`.
- **Sabotaje 2 del Profesor:** Quita `unique_together = ('course_section', 'subject', 'academic_period', 'name')`.
  - **Qué daña:** Permite crear dos columnas llamadas exactamente "RAP 1" en la misma materia y salón, duplicando las notas de los estudiantes.

### B. Modelo `GradeRecord` (La Nota Individual del Alumno)
```python
class GradeRecord(models.Model):
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE)
    criterion = models.ForeignKey(EvaluationCriterion, on_delete=models.CASCADE)
    score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('10.00'))]
    )
    is_locked = models.BooleanField(default=False)
```
- **¿Qué hace?:** Almacena la calificación que un docente le asigna a un estudiante específico en un RAP concreto.
- **Sabotaje del Profesor:** Cambia el validador a `MaxValueValidator(Decimal('5.00'))` si la institución califica sobre 10.0, o quita los validadores.
  - **Qué daña:** Si quita los validadores, un profesor podría digitar una nota de `-5.0` o `999.0` por error y la base de datos la aceptaría, destruyendo los promedios y los boletines.
  - **Solución:** Mantener siempre los `validators` de rango entre `0.00` y el máximo institucional (`5.00` o `10.00`).

---

## 3.2 `apps/grades/services.py` (La Lógica Matemática)

### Función Maestra: `calculate_period_final_grade(...)`
```python
def calculate_period_final_grade(student, course_section, subject, academic_period):
    criteria = EvaluationCriterion.objects.filter(
        course_section=course_section, subject=subject, academic_period=academic_period
    )
    weighted_sum = Decimal('0.00')
    has_any_score = False

    for crit in criteria:
        record = GradeRecord.objects.filter(
            student=student, course_section=course_section,
            subject=subject, academic_period=academic_period, criterion=crit
        ).first()

        if record is not None and record.score is not None:
            has_any_score = True
            # FÓRMULA PONDERADA: Nota * (Porcentaje / 100)
            weighted_sum += (record.score * (crit.percentage / Decimal('100.00')))

    final_score = weighted_sum.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    return final_score
```
- **¿Qué hace?:** Aplica la sumatoria ponderada: $\text{Definitiva} = \sum (\text{Nota} \times \frac{\text{Porcentaje}}{100})$ con redondeo financiero exacto `ROUND_HALF_UP` a 2 decimales.
- **Sabotaje 1 del Profesor:** Quita la división `/ Decimal('100.00')`:
  ```python
  weighted_sum += (record.score * crit.percentage) # ¡DAÑADO!
  ```
  - **Qué daña:** Si un estudiante saca `4.0` en un examen que vale `30%`, en lugar de sumar `1.20` sumará `120.00`. Al intentar guardar, Django arrojará: `decimal.InvalidOperation` o `django.db.utils.DataError: numeric field overflow` porque el campo en base de datos solo admite 4 dígitos (`max_digits=4`).
  - **Solución:** Restaurar la división entre 100: `(record.score * (crit.percentage / Decimal('100.00')))`.
- **Sabotaje 2 del Profesor:** Cambia `ROUND_HALF_UP` por truncamiento normal `int()`:
  - **Qué daña:** Una nota de `2.96` se convertiría en `2.0` o `2.9`, haciendo que un estudiante que merecía aprobar con `3.0` pierda la asignatura injustamente.
  - **Solución:** Usar `quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)`.

---

# 4. CONTROL DE PERIODOS Y AÑOS LECTIVOS: `apps/periods/`

## 4.1 `apps/periods/models.py`

```python
class AcademicPeriod(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', '🟢 Abierto / Activo'
        CLOSED = 'CLOSED', '🟡 Cerrado'
        LOCKED = 'LOCKED', '🔴 Bloqueado'

    status = models.CharField(max_length=15, choices=Status.choices, default=Status.ACTIVE)

    @property
    def is_editable(self):
        return self.status == self.Status.ACTIVE
```

- **¿Qué hace?:** Controla si los profesores pueden calificar o no. Si el periodo está en `CLOSED` o `LOCKED`, la plataforma congela las notas para emitir boletines.
- **Sabotaje del Profesor:** Modifica la propiedad `is_editable` para que siempre devuelva `True`:
  ```python
  @property
  def is_editable(self):
      return True # ¡DAÑADO!
  ```
  - **Qué daña:** **Fraude de calificaciones.** Cualquier profesor puede entrar en diciembre y cambiar las notas del primer periodo de febrero que ya habían sido entregadas a los padres de familia en boletines físicos.
  - **Solución:**
    ```python
    @property
    def is_editable(self):
        return self.status == self.Status.ACTIVE
    ```

---

# 5. CARGA MASIVA TRANSACCIONAL Y EXPEDIENTES: `apps/students/`

## 5.1 `apps/students/views.py` — `bulk_upload_students_view`

Este archivo es una joya técnica del proyecto porque implementa **Transacciones Atómicas con Puntos de Guardado (Savepoints)**.

```python
from django.db import transaction

for row_num, row in enumerate(rows_data[start_idx:], start=start_idx + 1):
    # Lectura y limpieza de datos del estudiante...
    try:
        with transaction.atomic(): # <--- EL ESCUDO ATÓMICO
            # 1. Crear usuario CustomUser
            # 2. Crear StudentProfile
            # 3. Crear matrícula Enrollment
            created_count += 1
    except Exception as e:
        errors.append(f"Fila {row_num}: Error al matricular: {str(e)}")
```

- **¿Qué hace exactamente?:** Lee archivos Excel (`.xlsx`) o CSV y matricula a cientos de estudiantes en segundos. La instrucción `with transaction.atomic():` crea un **Savepoint (punto de guardado)** por cada estudiante. Si el alumno de la fila 45 tiene un dato corrupto, la transacción revierte **únicamente esa fila**, registra el error y continúa procesando a los otros 99 estudiantes sin parar el sistema ni duplicar registros.
- **Sabotaje 1 del Profesor:** Borra la línea `with transaction.atomic():`.
  - **Qué daña:** **Corrupción de base de datos.** Si en la fila 45 se genera el usuario pero falla la matrícula del curso, el sistema queda con un "usuario huérfano" en `CustomUser` sin perfil en `StudentProfile`. Al intentar volver a subir el archivo corregido, saldrá `IntegrityError: column document_number is not unique` y no dejará matricular a nadie más.
  - **Solución:** Envolver siempre la creación en el bloque `with transaction.atomic():`.
- **Sabotaje 2 del Profesor:** Borra la verificación de extensiones `.xlsx` o la importación de `openpyxl`.
  - **Qué daña:** Si suben un archivo Excel moderno (`.xlsx`), el servidor intentará leerlo con `csv.reader` como texto plano. Como los archivos Excel son en realidad archivos binarios comprimidos en ZIP (con cabecera `PK\x03\x04`), saldrá un error ininteligible de caracteres extraños o `UnicodeDecodeError`, botando un error 500 al usuario.
  - **Solución:** Mantener la detección con `openpyxl.load_workbook(io.BytesIO(content))`.

---

# 6. BOLETINES OFICIALES PDF Y VERIFICACIÓN QR: `apps/reports/`

## 6.1 `apps/reports/views.py` y `urls.py`

### A. Vista `verify_bulletin_view(request, token)`
```python
def verify_bulletin_view(request, token):
    """
    Vista pública para verificar autenticidad de boletines escaneando el código QR.
    """
    from apps.courses.models import InstitutionSetting
    institution = InstitutionSetting.get_settings()
    context = {
        'token': token,
        'institution': institution,
        'is_valid': len(token) >= 16,
    }
    return render(request, 'reports/partials/verify_bulletin.html', context)
```
- **¿Qué hace?:** Permite que un acudiente, universidad o empresa escanee el código QR impreso en el boletín PDF con su celular y verifique si el documento fue emitido legalmente por la institución.
- **Sabotaje 1 del Profesor:** Le agrega el decorador `@login_required` a esta vista:
  ```python
  @login_required # ¡DAÑADO!
  def verify_bulletin_view(request, token):
  ```
  - **Qué daña:** **Destruye la verificación pública.** Cuando una universidad o un tercero escanee el QR del boletín para comprobar su validez, el sistema le pedirá usuario y contraseña de Academix en vez de mostrarle el certificado de autenticidad.
  - **Solución:** Quitar `@login_required`, pues la vista debe ser de libre acceso público (cumpliendo con no divulgar datos sensibles de menores según la Ley 1581).
- **Sabotaje 2 del Profesor:** Modifica la plantilla para que imprima en pantalla la cédula, teléfono y dirección del estudiante menor de edad.
  - **Qué daña:** **Violación gravísima de la Ley Estatutaria 1581 de 2012 (Habeas Data de Menores de Edad) y Circular 002 de la SIC.** Expone datos privados de niños a cualquier persona que tenga el link del QR.
  - **Solución:** En la vista de verificación QR únicamente se debe mostrar: Nombre del alumno, Grado escolar, Año lectivo y Condición final (Aprobado/Reprobado).

---

# 7. ASISTENCIA, DISCIPLINA Y TRAZABILIDAD: `apps/attendance/` y `apps/audit/`

## 7.1 `apps/attendance/models.py` (Llamado a Lista)

```python
class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'PRESENT', 'Presente'
        ABSENT = 'ABSENT', 'Inasistencia Injustificada'
        JUSTIFIED = 'JUSTIFIED', 'Inasistencia Justificada'
        LATE = 'LATE', 'Llegada Tarde'

    session = models.ForeignKey(AttendanceSession, on_delete=models.CASCADE)
    student = models.ForeignKey('students.StudentProfile', on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PRESENT)

    class Meta:
        unique_together = ('session', 'student')
```
- **¿Qué hace?:** Guarda el llamado a lista diario de cada alumno.
- **Sabotaje del Profesor:** Borra `unique_together = ('session', 'student')`.
  - **Qué daña:** Si un profesor da doble clic rápido en "Guardar Asistencia", el sistema creará dos o tres registros de asistencia para el mismo alumno en la misma clase, falseando los porcentajes de inasistencia del boletín.
  - **Solución:** Conservar la restricción `unique_together`.

## 7.2 `apps/audit/services.py` (La Caja Negra del Sistema)

```python
def log_audit(user, action, model_name, object_id, details=None, ip_address=None):
    AuditLog.objects.create(
        user=user, action=action, model_name=model_name,
        object_id=str(object_id), details=details, ip_address=ip_address
    )
```
- **¿Qué hace?:** Registra de forma inmutable quién cambió una nota, qué valor tenía antes, qué valor tiene ahora, fecha, hora y dirección IP.
- **Sabotaje del Profesor:** Comenta la llamada `log_audit(...)` en `apps/grades/views.py`.
  - **Qué daña:** Pérdida de no-repudio y trazabilidad. Si un docente altera una nota de 2.0 a 5.0 de forma fraudulenta, no queda ningún registro de auditoría para investigarlo (Violación de la norma IEEE 730).
  - **Solución:** Garantizar que cada modificación de notas invoque a `log_audit`.

---

# 8. VISTAS VISUALES, FORMULARIOS Y SEGURIDAD WEB: `templates/`

## 8.1 `templates/accounts/login.html`

```html
<form method="POST" action="{% url 'accounts:login' %}">
    {% csrf_token %} <!-- EL TOKEN DE SEGURIDAD -->
    
    {% if form.errors %}
    <div class="alert alert-danger" role="alert" aria-live="assertive">
        <div>Usuario o contraseña incorrectos.</div>
    </div>
    {% endif %}

    <input type="text" name="username" id="id_username" class="form-control" required>
    <input type="password" name="password" id="id_password" class="form-control" required>
    <button type="submit">Iniciar Sesión</button>
</form>
```

- **Sabotaje 1 del Profesor:** Borra la etiqueta `{% csrf_token %}` en el formulario.
  - **Error en Pantalla:** **HTTP 403 Forbidden — CSRF verification failed. Request aborted.**
  - **Qué daña:** Nadie en el planeta puede iniciar sesión. Django rechaza de inmediato cualquier formulario POST que no contenga el token criptográfico contra ataques de falsificación de sitios cruzados.
  - **Solución:** Escribir inmediatamente `{% csrf_token %}` dentro del `<form>`.
- **Sabotaje 2 del Profesor:** Borra `role="alert"` y `aria-live="assertive"` en el `<div>` de error.
  - **Qué daña:** **Incumplimiento de la Resolución 1519 de 2020 de MinTIC y las normas W3C WCAG 2.1 AA (Accesibilidad Web).** Los lectores de pantalla para personas ciegas no anuncian el mensaje de error cuando fallan las credenciales (Hallazgo HAL-02 de la auditoría).
  - **Solución:** Restaurar `role="alert"` y `aria-live="assertive"`.

## 8.2 `templates/base.html` (La Plantilla Maestra)

- **¿Qué hace?:** Define el esqueleto visual de todo Academix: Navbar, Sidebar con control condicional por rol (`{% if user.is_teacher %}`), estilos CSS globales y scripts de Lucide Icons. Las demás plantillas heredan de ella usando `{% extends 'base.html' %}`.
- **Sabotaje del Profesor:** Cambia el nombre de `{% block content %}` por `{% block contenido %}` en `base.html` pero deja las hijas con `content`.
  - **Qué daña:** Las páginas se ven en blanco o vacías, mostrando solo el menú lateral y la barra superior pero sin ningún contenido en el centro.
  - **Solución:** Sincronizar el nombre del bloque para que tanto la madre como las hijas usen `{% block content %}` y `{% endblock %}`.

---

# 9. COMANDOS DE RESCATE EN CONSOLA (CHEATSHEET DE TERMINAL)

Si el profesor les dice: *"El sistema está caído o no arranca por consola, arréglenlo frente a mí"*, estos son los comandos que deben ejecutar:

| Problema del Profesor | Comando de Rescate Inmediato | Explicación Técnica |
| :--- | :--- | :--- |
| *"La base de datos tiene tablas faltantes o desincronizadas"* | `python manage.py migrate` | Aplica todas las migraciones pendientes en `db.sqlite3`. |
| *"El profesor creó un modelo nuevo pero no aparece en la BD"* | `python manage.py makemigrations` seguido de `python manage.py migrate` | Detecta cambios en los `models.py`, genera el script SQL y lo aplica. |
| *"Faltan usuarios de prueba o se dañaron los roles"* | `python manage.py setup_production_init` o `python manage.py init_roles` | Comando personalizado de Academix que recrea la jerarquía de roles institucional. |
| *"El puerto 8000 está ocupado por otro proceso"* | `python manage.py runserver 8080` | Levanta el servidor en el puerto alternativo `8080`. |
| *"No se ven los iconos o estilos en red local"* | `python manage.py collectstatic --noinput` | Recopila todos los archivos estáticos en la carpeta `staticfiles/`. |
| *"Falta una librería que el profesor desinstaló"* | `pip install -r requirements.txt` | Reinstala en lote todas las librerías oficiales del sistema. |
| *"¿Cómo arrancar el servidor para que se vea en celulares/otras PCs?"* | `python iniciar_servidor_red.py` | Script automatizado de Academix que detecta la IP local y arranca en `0.0.0.0:8000`. |

---

# 10. TOP 20 DE SABOTAJES MÁS PROBABLES DEL PROFESOR CON PREGUNTA Y RESPUESTA EXACTA

Utilicen esta tabla para estudiar y memorizar los casos más comunes:

| # | ¿Qué va a dañar el profesor? | Archivo Afectado | ¿Qué error exacto sale? | ¿Cómo se lo explicas y cómo se arregla? |
| :-: | :--- | :--- | :--- | :--- |
| **1** | Borra `{% csrf_token %}` en el login. | `templates/accounts/login.html` | **HTTP 403 Forbidden (CSRF verification failed)** | *"Profesor, eliminó el token de protección contra peticiones falsificadas. Django rechaza el POST por seguridad. Se arregla escribiendo `{% csrf_token %}` dentro del form."* |
| **2** | Comenta `AUTH_USER_MODEL = 'accounts.CustomUser'`. | `config/settings.py` | `InconsistentMigrationHistory` o `AttributeError: no attribute 'role'` | *"Profesor, obligó a Django a usar el usuario básico sin roles. Se arregla restaurando la variable `AUTH_USER_MODEL` apuntando a nuestro modelo."* |
| **3** | Cambia `Decimal` por `float` en el cálculo de notas. | `apps/grades/services.py` | Notas como `3.4999999999999` y sumas que no dan 100% | *"Profesor, introdujo errores de precisión binaria de coma flotante. En sistemas financieros y de notas la norma ISO 25010 exige `Decimal` con redondeo `ROUND_HALF_UP`."* |
| **4** | Borra `with transaction.atomic():` en carga masiva. | `apps/students/views.py` | Usuarios creados a medias y claves duplicadas | *"Profesor, quitó el Savepoint transaccional ACID. Si un alumno falla, deja datos corruptos en la BD. Se arregla reincorporando `with transaction.atomic():`."* |
| **5** | Quita `@login_required` en la vista de notas. | `apps/grades/views.py` | Cualquier persona sin clave entra a editar notas | *"Profesor, dejó la vista pública sin autenticación perimetral. Se arregla colocando el decorador `@login_required` encima de la función."* |
| **6** | Le pone `@login_required` a la verificación QR del boletín. | `apps/reports/views.py` | Pide login cuando alguien escanea el código en la calle | *"Profesor, bloqueó la verificación pública de autenticidad. El QR debe ser público pero sin exponer datos sensibles de menores según Ley 1581."* |
| **7** | Cambia `self.status == self.Status.ACTIVE` por `True` en periodos. | `apps/periods/models.py` | Docentes pueden cambiar notas de periodos ya cerrados | *"Profesor, rompió el bloqueo de periodos. Permite modificar notas extemporáneas violando la trazabilidad. Se arregla validando contra `Status.ACTIVE`."* |
| **8** | Quita `unique_together` en `EvaluationCriterion`. | `apps/grades/models.py` | Aparecen columnas "RAP 1" duplicadas en la planilla | *"Profesor, quitó la restricción de unicidad relacional. Permite duplicar componentes de evaluación en la misma materia."* |
| **9** | Comenta `login(request, user)` en `login_view`. | `apps/accounts/views.py` | El login se recarga indefinidamente y no entra | *"Profesor, autentica las credenciales pero nunca crea la cookie de sesión en el navegador. Se arregla descomentando `login(request, user)`."* |
| **10** | Quita `'apps.grades'` de `INSTALLED_APPS`. | `config/settings.py` | `LookupError: No installed app with label 'grades'` | *"Profesor, desconectó la micro-aplicación del ecosistema Django. La base de datos y las URLs desconocen el módulo de notas. Se agrega de nuevo a la lista."* |
| **11** | Quita `AuthenticationMiddleware` de `MIDDLEWARE`. | `config/settings.py` | `AttributeError: 'WSGIRequest' has no attribute 'user'` | *"Profesor, quitó el middleware que inyecta el usuario logueado en la petición. El 100% de las vistas colapsan. Se restaura en la posición correspondiente."* |
| **12** | Quita la división `/ Decimal('100.00')` en promedios. | `apps/grades/services.py` | `DataError: numeric field overflow` (Notas de 350.0) | *"Profesor, multiplicó la nota por el porcentaje entero sin normalizarlo a 1.0. La nota desborda los 4 dígitos permitidos en la base de datos."* |
| **13** | Borra `@property` en `is_teacher` de `CustomUser`. | `apps/accounts/models.py` | Los métodos devuelven el objeto función y los alumnos ven menús de profesores | *"Profesor, convirtió una propiedad dinámica en un método simple. En las plantillas `user.is_teacher` evalúa a True por ser función existente."* |
| **14** | Pone `DEBUG = False` con `ALLOWED_HOSTS = []`. | `config/settings.py` | **Bad Request (400) — Invalid HTTP_HOST header** | *"Profesor, activó modo producción sin autorizar los dominios o IPs que pueden consultar el servidor. Se arregla agregando `'localhost'` o `'*'"`.* |
| **15** | Borra el archivo `.env` o la clave `SECRET_KEY`. | Raíz / `.env` | `KeyError: 'SECRET_KEY'` o `django.core.exceptions.ImproperlyConfigured` | *"Profesor, borró las variables de entorno donde reside la clave criptográfica del sistema. Se arregla copiando `.env.example` a `.env`."* |
| **16** | Cambia `on_delete=models.SET_NULL` por `models.CASCADE` en usuarios de escuela. | `apps/accounts/models.py` | Borrar un colegio borra todos los profesores y alumnos | *"Profesor, configuró un borrado destructivo en cascada. La regla de integridad exige `SET_NULL` para conservar las hojas de vida históricas."* |
| **17** | Quita `enforce_report_card_clearance` en reportes. | `apps/reports/views.py` | Alumnos con deudas de pensión descargan boletines | *"Profesor, desactivó el control financiero institucional que valida si el estudiante está a paz y salvo antes de emitir el boletín."* |
| **18** | Cambia el nombre del bloque `{% block content %}` en una vista. | `templates/*.html` | La pantalla sale completamente vacía/blanca | *"Profesor, rompió la herencia visual de Django MVT. La plantilla hija no coincide con el bloque definido en `base.html`."* |
| **19** | Borra `log_audit(...)` al guardar calificaciones. | `apps/grades/views.py` | No queda registro de quién alteró una nota en auditoría | *"Profesor, vulneró la trazabilidad y el no-repudio exigidos por la norma IEEE 730 y la Ley 1581. Si alguien hace fraude, no hay evidencia en la bitácora."* |
| **20** | Modifica `unique=True` en `document_number` de usuarios. | `apps/accounts/models.py` | Se pueden crear dos estudiantes con la misma cédula | *"Profesor, permitió colisión de identidades. Destruye la integridad referencial en el expediente del estudiante y la carga masiva."* |

---

# 11. ESTRATEGIA DE DEFENSA SUGERIDA PARA LAS 3 INTEGRANTES

Para que cada una tenga su especialidad bien definida ante las preguntas del instructor:

### 👩‍💻 INTEGRANTE 1: Especialista en Frontend, Plantillas y Accesibilidad
- **Archivos a su cargo:** `templates/base.html`, `templates/accounts/login.html`, `templates/reports/`, `templates/grades/`.
- **Temas a defender:** Tokens CSRF, atributos ARIA de la Resolución 1519 de MinTIC, herencia de plantillas (`extends` / `block`), diseño responsivo y prevención de errores visuales.

### 👩‍💻 INTEGRANTE 2: Especialista en Lógica de Negocio, RAPs y Base de Datos
- **Archivos a su cargo:** `apps/grades/services.py`, `apps/grades/models.py`, `apps/periods/models.py`, `apps/accounts/models.py`.
- **Temas a defender:** Fórmulas de RAPs con `Decimal` al 100.00%, bloqueo de periodos lectivos (`is_editable`), relaciones relacionales (FK, `unique_together`, `on_delete`) y roles de usuario.

### 👩‍💻 INTEGRANTE 3: Especialista en Arquitectura, Carga Masiva y Seguridad
- **Archivos a su cargo:** `apps/students/views.py` (Carga masiva), `apps/reports/views.py` (QR Criptográfico), `config/settings.py` (Middlewares), `apps/audit/`.
- **Temas a defender:** Transacciones atómicas ACID con Savepoints, lectura de Excel `.xlsx` con `openpyxl`, limitador de tasa contra fuerza bruta (`@ratelimit`), verificación pública de QR y comandos de consola de Django.

---

*Con esta guía dominada, ninguna pregunta ni intento de sabotaje del profesor podrá sorprenderlas. Tienen la explicación exacta, el diagnóstico del error y la línea de código para resolverlo en vivo.*

