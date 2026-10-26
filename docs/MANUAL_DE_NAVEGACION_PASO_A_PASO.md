# MANUAL PASO A PASO: CÓMO NAVEGAR POR ACADEMIX DESDE CERO
**Guía Visual y Práctica de Navegación para Cualquier Usuario**  
*Plataforma Integral de Gestión Escolar y Aprendizaje | Versión 2.0*

---

## 🧭 ¿De qué se trata esta guía?
Esta guía te explica, **paso por paso y desde el principio**, cómo encender el sistema, cómo ingresar desde tu navegador, cómo entender cada parte de la pantalla y cómo moverte por todos los módulos sin perderte.

---

## ÍNDICE RÁPIDO
1. [PASO 1: Encender el Sistema](#paso-1-encender-el-sistema)
2. [PASO 2: Abrir la Página en tu Navegador](#paso-2-abrir-la-página-en-tu-navegador)
3. [PASO 3: Cómo Iniciar Sesión (Login)](#paso-3-cómo-iniciar-sesión-login)
4. [PASO 4: Anatomía de la Pantalla (El Mapa de la Página)](#paso-4-anatomía-de-la-pantalla-el-mapa-de-la-página)
5. [PASO 5: Rutas de Navegación Guiadas (¿Qué deseas hacer hoy?)](#paso-5-rutas-de-navegación-guiadas-qué-deseas-hacer-hoy)
   - [Ruta A: Consultar o Cambiar mi Contraseña](#ruta-a-consultar-o-cambiar-mi-contraseña)
   - [Ruta B: Digitar Notas en la Planilla (Docentes)](#ruta-b-digitar-notas-en-la-planilla-docentes)
   - [Ruta C: Tomar Asistencia / Llamar Lista (Docentes)](#ruta-c-tomar-asistencia--llamar-lista-docentes)
   - [Ruta D: Crear o Calificar Tareas (Docentes)](#ruta-d-crear-o-calificar-tareas-docentes)
   - [Ruta E: Consultar mis Calificaciones (Estudiantes y Padres)](#ruta-e-consultar-mis-calificaciones-estudiantes-y-padres)
   - [Ruta F: Enviar una Tarea Escolar (Estudiantes)](#ruta-f-enviar-una-tarea-escolar-estudiantes)
   - [Ruta G: Descargar el Boletín en PDF con Código QR](#ruta-g-descargar-el-boletín-en-pdf-con-código-qr)
   - [Ruta H: Matricular Alumnos y Ver Expedientes (Secretaría)](#ruta-h-matricular-alumnos-y-ver-expedientes-secretaría)
   - [Ruta I: Personalizar el Colegio, Escudo y Modelo (Rectoría)](#ruta-i-personalizar-el-colegio-escudo-y-modelo-rectoría)
6. [PASO 6: Cómo Cerrar Sesión de Forma Segura](#paso-6-cómo-cerrar-sesión-de-forma-segura)
7. [Diccionario Rápido de Botones y Colores](#diccionario-rápido-de-botones-y-colores)

---

## PASO 1: Encender el Sistema

Antes de abrir internet, el servidor de Academix debe estar encendido.

1. Abre el explorador de archivos en tu computador.
2. Ve a la carpeta del proyecto: **`c:\Academix`**
3. Haz **doble clic** sobre:
   - **`iniciar_servidor_produccion.bat`** (si vas a usar el sistema en ese mismo computador), o
   - **`iniciar_servidor_red.bat`** (si tus compañeros o tú van a conectarse desde otros computadores o celulares por Wi-Fi).
4. Verás aparecer una ventana de consola negra con letras blancas que dice:  
   `Starting development server at http://127.0.0.1:8000/`  
   *(Déjala abierta mientras trabajes; si la cierras, el sistema se apagará).*

---

## PASO 2: Abrir la Página en tu Navegador

1. Abre tu navegador de internet favorito (**Google Chrome, Microsoft Edge, Mozilla Firefox o Brave**).
2. Haz clic en la barra de direcciones superior (donde normalmente escribes google.com).
3. Escribe exactamente:
   ```text
   http://localhost:8000/
   ```
   *(Si estás en otro computador o celular conectado al Wi-Fi del colegio, escribe la dirección IP que te mostró la consola, por ejemplo: `http://192.168.1.15:8000/`).*
4. Presiona la tecla **Enter**.
5. ¡Verás el Portal Institucional de bienvenida de Academix!

---

## PASO 3: Cómo Iniciar Sesión (Login)

En la pantalla de bienvenida verás el escudo institucional y un botón grande que dice **"Ingresar al Portal"**. Haz clic en él y sigue estos 4 campos:

```text
┌────────────────────────────────────────────────────────┐
│  🎓 ACADEMIX — Portal Institucional                   │
│                                                        │
│  1. Seleccione su Rol:                                 │
│  [ ▼ Docente (o Rector, Alumno, Padre, Secretaria) ]   │
│                                                        │
│  2. Usuario o Identificación:                          │
│  [ Escribe aquí tu usuario o tu cédula             ]   │
│                                                        │
│  3. ID ÚNICO del Alumno (Solo para Alumnos y Padres):  │
│  [ EST-456789 o Documento del Alumno               ]   │
│                                                        │
│  4. Contraseña:                                        │
│  [ ••••••••••••••••                                ]   │
│                                                        │
│  ┌──────────────────────────────────────────────────┐  │
│  │             INGRESAR AL SISTEMA                  │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────┘
```

### Tabla de Cuentas Listas para Usar:

| Si quieres entrar como... | 1. Selecciona en Rol | 2. En Usuario escribe | 3. En ID ÚNICO escribe | 4. En Contraseña escribe |
| :--- | :--- | :--- | :--- | :--- |
| **👑 Administrador** | Administrador | `admin` | *(Dejar vacío)* | `Admin2026*` |
| **🏛️ Rector(a)** | Rector / Rectora | `rector` | *(Dejar vacío)* | `Rector2026*` |
| **📋 Secretaria** | Secretaria | `secretaria1` | *(Dejar vacío)* | `Secre2026*` |
| **👨‍🏫 Docente** | Docente | `docente1` | *(Dejar vacío)* | `Profe2026*` |
| **🎓 Alumno** | Alumno | `est_1023456789` | `EST-456789` | `Estudiante2026*` |
| **👨‍👩‍👧 Padre de Familia** | Padre de Familia | `manuel` | `EST-456789` | `Padre2026*` |

Haz clic en el botón azul **"Ingresar al Sistema"**. ¡Listo, ya estás dentro!

---

## PASO 4: Anatomía de la Pantalla (El Mapa de la Página)

Una vez ingresas, la pantalla se organiza siempre en **3 áreas fijas**:

```text
┌────────────────────────────────────────────────────────────────────────┐
│ [≡] Año Lectivo 2026 • Sede Central        🔔 Avisos   🎨 Tema  👤 Usuario [▼] │ ← 1. BARRA SUPERIOR
├──────────────────────┬─────────────────────────────────────────────────┤
│ 🎓 ACADEMIX          │                                                 │
│ 👤 Tu Nombre (Rol)   │                                                 │
│                      │                                                 │
│ 📌 MENÚ PRINCIPAL    │            2. ÁREA DE TRABAJO Y CONTENIDO       │
│ • Panel Principal    │                                                 │
│ • Agenda             │   (Aquí aparecen las tablas, los formularios,   │
│                      │    las planillas de notas y las tarjetas con    │
│ 📚 EVALUACIÓN Y AULA │    toda la información de la sección activa)    │
│ • Calificaciones     │                                                 │
│ • Asistencia         │                                                 │
│ • Tareas             │                                                 │
│                      │                                                 │
│ ⚙️ CUENTA            │                                                 │
│ • Mi Perfil          │                                                 │
│ • Cerrar Sesión      │                                                 │
└──────────────────────┴─────────────────────────────────────────────────┘
  ↑ 3. BARRA LATERAL (Menú)
```

1. **La Barra Superior (Topbar):**
   - **Botón `≡` (Hamburguesa):** Si necesitas más espacio para ver una tabla ancha, haz clic aquí para ocultar o mostrar el menú lateral.
   - **Indicador:** Te recuerda el año activo (ej. *Año Lectivo 2026*).
   - **Campana `🔔`:** Muestra avisos y recordatorios del colegio.
   - **Tu Avatar y Nombre (arriba a la derecha):** Haz clic para abrir el menú rápido de tu cuenta (Perfil, Cambiar Clave, Salir).
2. **La Barra Lateral (Sidebar):**
   - Es tu menú de navegación. Haz clic en cualquier botón para ir a esa sección.
   - La opción donde estés parado se resaltará con color azul.
3. **El Área de Trabajo:**
   - Es el centro de la pantalla donde ejecutas tus tareas (ver gráficos, calificar, guardar datos, descargar archivos).

---

## PASO 5: Rutas de Navegación Guiadas (¿Qué deseas hacer hoy?)

---

### Ruta A: Consultar o Cambiar mi Contraseña
1. Haz clic en tu nombre o avatar en la esquina superior derecha.
2. En el menú desplegable, haz clic en **Cambiar Contraseña**.
3. Escribe tu contraseña actual, escribe tu nueva clave y confírmala.
4. Haz clic en **Actualizar Contraseña**.

---

### Ruta B: Digitar Notas en la Planilla (Docentes)
1. En el menú lateral izquierdo, haz clic en **Planilla de Notas** (o entra desde **Mis Asignaciones**).
2. Verás tres selectores en la parte superior:
   - **Periodo:** Elige el periodo que estás evaluando (ej. *Periodo 1*).
   - **Curso:** Elige el salón (ej. *10-A*).
   - **Asignatura:** Elige la materia (ej. *Matemáticas*).
3. Se cargará automáticamente la lista de estudiantes con sus casillas de notas.
4. Escribe la nota de cada alumno directamente en la casilla (ej. `4.5`, `3.8`, `2.5`).
5. Observa cómo el promedio final y el estado (Aprobado / Reprobado) se calculan solos en tiempo real.
6. Al terminar de calificar, haz clic en el botón verde **Guardar Calificaciones**.

---

### Ruta C: Tomar Asistencia / Llamar Lista (Docentes)
1. En el menú lateral izquierdo, haz clic en **Llamado de Lista**.
2. Selecciona la **Fecha**, el **Curso** y la **Sesión / Hora**.
3. El sistema carga la lista con todos los estudiantes marcados en 🟢 **Presente (P)** por defecto.
4. Con un solo clic cambia a quien haya faltado:
   - 🔴 **(A)** Ausente / Falta
   - 🟡 **(J)** Excusa Justificada
   - 🟠 **(T)** Retardo / Tardanza
5. Haz clic en el botón verde **Registrar Asistencia**. ¡Listo en menos de 1 minuto!

---

### Ruta D: Crear o Calificar Tareas (Docentes)
1. En el menú lateral izquierdo, haz clic en **Tareas y Envíos**.
2. **Para crear una nueva tarea:**
   - Haz clic en el botón azul **Nueva Tarea**.
   - Llena el título, el salón, la materia, las instrucciones y la **fecha/hora límite de entrega**.
   - *(Opcional)* Adjunta una guía o taller en PDF o Word con el botón *Seleccionar archivo*.
   - Haz clic en **Publicar Tarea**.
3. **Para calificar trabajos entregados:**
   - Haz clic en la tarea creada y pulsa **Ver Entregas**.
   - Verás quién ya entregó. Haz clic en el archivo del estudiante para revisarlo.
   - Digita su calificación numérica y escribe un comentario de retroalimentación pedagógica.
   - Haz clic en **Guardar Calificación**.

---

### Ruta E: Consultar mis Calificaciones (Estudiantes y Padres)
1. En el menú lateral izquierdo, haz clic en **Mis Calificaciones** (o *Notas del Estudiante* si eres Padre).
2. Selecciona el **Periodo** que quieres revisar.
3. Aparecerá una tabla clara con todas tus materias:
   - La nota de cada componente evaluativo.
   - La **calificación definitiva** de la materia.
   - El estado en color: verde si vas aprobando, rojo o naranja si necesitas refuerzo.

---

### Ruta F: Enviar una Tarea Escolar (Estudiantes)
1. En el menú lateral izquierdo, haz clic en **Mis Tareas**.
2. Verás tarjetas organizadas con tus actividades:
   - Si la tarjeta dice 🔵 **Activa**, aún estás a tiempo de entregarla.
   - Si el profesor subió una guía, pulsa **Descargar Guía / Material**.
3. Para enviar tu solución:
   - Haz clic en el botón azul **Entregar mi Trabajo**.
   - Escribe un comentario o pega un enlace (si hiciste un video o diapositivas web).
   - Haz clic en **Seleccionar archivo** y elige tu documento (PDF, Word, imagen o ZIP).
   - Haz clic en el botón verde **Confirmar y Enviar Tarea**.
4. La tarjeta cambiará a 🟢 **Entregado**. Cuando el docente la revise, cambiará a 🟣 **Calificado** con tu nota y los comentarios del profesor.

---

### Ruta G: Descargar el Boletín en PDF con Código QR
1. Ve a **Mis Calificaciones** (como estudiante o padre) o al módulo de **Reportes** (como secretaría o directivo).
2. Haz clic en el botón **Descargar Boletín PDF** del periodo deseado.
3. Se abrirá o descargará un documento oficial con:
   - El escudo y encabezado oficial del colegio.
   - La tabla completa de notas, fallas y observaciones.
   - El puesto del estudiante en el salón.
   - Un **Código QR y Token de Seguridad** que cualquier persona puede escanear para certificar que el boletín es auténtico.

---

### Ruta H: Matricular Alumnos y Ver Expedientes (Secretaría)
1. En el menú lateral, haz clic en **Matrículas y Alumnos**.
2. **Para buscar un alumno:** Escribe su nombre o documento en la caja de búsqueda rápida.
3. **Para ver su expediente:** Haz clic en el botón **Expediente** al lado de su nombre. Podrás consultar o subir sus documentos legales (registro civil, carné de salud) y revisar su observador disciplinario.
4. **Para matricular un nuevo alumno individual:** Haz clic en **Nuevo Alumno**, llena sus datos, asígnale su curso y pulsa **Confirmar Matrícula**.
5. **Para carga masiva:** Si vas a matricular muchos estudiantes al inicio de año, pulsa **Carga Masiva CSV**, descarga la plantilla en Excel, llénala y súbela para matricular a todos en bloque en un solo paso.

---

### Ruta I: Personalizar el Colegio, Escudo y Modelo (Rectoría)
1. Ingresa como Rector y ve en el menú lateral a `Administración y Marca > Personalización y Marca`.
2. Aquí puedes:
   - Escribir el **Nombre Oficial** de tu institución, lema, NIT y DANE.
   - Subir el archivo de imagen con el **Escudo / Logo** del plantel.
   - Elegir el **Modelo Institucional**:
     - *Colegio:* Grados, Cursos, Asignaturas, Estudiantes y Docentes.
     - *Técnico / SENA:* Trimestres, Fichas, Competencias, Aprendices e Instructores.
     - *Universidad:* Semestres, Grupos, Materias, Estudiantes y Profesores.
3. Haz clic en **Guardar Ajustes**. Todo el sistema adaptará de inmediato sus términos y pantallas.

---

## PASO 6: Cómo Cerrar Sesión de Forma Segura

Cuando termines de trabajar en la plataforma (especialmente si estás en un computador compartido de la sala de profesores o de la biblioteca):

1. Ve a la esquina superior derecha de la pantalla.
2. Haz clic sobre tu **Nombre o Foto de Perfil**.
3. En el menú que se despliega, haz clic en la última opción en color rojo: **Cerrar Sesión** *(o en el menú lateral abajo en "Cerrar Sesión")*.
4. El sistema cerrará tu acceso y te devolverá a la pantalla de bienvenida protegiendo tu información.

---

## Diccionario Rápido de Botones y Colores

| Color / Icono | ¿Qué significa en Academix? | Ejemplo de uso |
| :---: | :--- | :--- |
| 🟢 **Verde** | Acción positiva o guardado exitoso | "Guardar Calificaciones", "Registrar Asistencia", "Confirmar Entrega" |
| 🔵 **Azul** | Navegación, consulta o acción principal | "Ver Detalles", "Entregar mi Trabajo", "Descargar Boletín" |
| 🟡 **Amarillo** | Advertencia, material complementario o pendiente | "Descargar Guía", tareas pendientes de calificar, avisos |
| 🔴 **Rojo** | Alerta, ausencia, cancelación o salida | Estudiante ausente, tarea vencida, botón "Cerrar Sesión" |
| 🟣 **Morado** | Tarea ya calificada con retroalimentación | Tarjeta de tarea con nota final del docente |
| **`≡` (Tres líneas)** | Botón Hamburguesa | Ocultar o mostrar el menú lateral para ampliar tu pantalla |
| **`🔔` (Campana)** | Centro de Notificaciones | Ver avisos, circulares y alertas del colegio |
| **`🔍` (Lupa)** | Búsqueda rápida | Filtrar estudiantes o asignaturas en segundos |

---
*Manual de Navegación Paso a Paso — ACADEMIX © 2026*  
*Documento diseñado para uso libre de la comunidad educativa.*
