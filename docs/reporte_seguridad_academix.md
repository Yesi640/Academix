# 🔐 Reporte de Seguridad del Sistema ACADEMIX
### Informe para la Dirección Institucional

**Fecha de revisión:** 09 de octubre de 2026
**Preparado por:** Equipo de Desarrollo — Revisión de Seguridad
**Sistema revisado:** ACADEMIX — Sistema de Gestión Académica

---

> [!NOTE]
> Este documento fue elaborado para que **cualquier persona** pueda entenderlo, sin necesidad de conocimientos técnicos. Si tiene alguna duda sobre algún punto, puede consultarla directamente con el equipo de desarrollo.

---

## ¿Qué es una auditoría de seguridad?

Una auditoría de seguridad es como contratar a un inspector para que revise una casa antes de habitarla. El inspector no vive ahí, pero camina por todos los cuartos buscando puertas sin seguro, ventanas abiertas o cableado peligroso. En este caso, revisamos el sistema ACADEMIX para encontrar esos "puntos de entrada" que alguien con malas intenciones podría aprovechar.

---

## 📊 Resumen General

Encontramos **15 situaciones de riesgo** en total:

| Color | Nivel | Cantidad | ¿Qué significa? |
|:---:|---|:---:|---|
| 🔴 | **Crítico** | 4 | Peligro inmediato. Puede ocurrir hoy. |
| 🟠 | **Alto** | 6 | Debe corregirse antes de usar el sistema con usuarios reales. |
| 🟡 | **Medio** | 3 | Importante, pero hay más tiempo para corregirlo. |
| 🟢 | **Bajo** | 2 | Mejoras recomendadas, sin urgencia. |

> [!CAUTION]
> Hay **4 problemas críticos** que deben resolverse de inmediato, antes de que el sistema sea usado por estudiantes, docentes o padres de familia.

---

## 🔴 PROBLEMAS CRÍTICOS — Atención Inmediata

---

### ❌ Problema 1 de 4 — La llave del correo institucional está expuesta

**¿Qué pasó?**
El sistema guarda una lista de contraseñas y configuraciones en un archivo interno. Dentro de ese archivo encontramos la **contraseña real del correo de Gmail** que usa ACADEMIX para enviar notificaciones a estudiantes y docentes.

**Analogía:** Es como dejar la llave de la oficina guardada debajo del felpudo de la entrada, con una nota que dice "aquí está la llave".

**¿Qué puede pasar si no se corrige?**
- Cualquier persona que acceda a ese archivo puede entrar al correo institucional.
- Puede enviar correos falsos a nombre de la institución (por ejemplo, citaciones falsas a padres).
- Puede leer todos los correos que el sistema ya envió.
- La cuenta de correo puede ser bloqueada por Google por uso indebido.

**¿Qué debe hacerse?**
1. ✅ **Hoy mismo:** Cambiar la contraseña de ese correo de Gmail desde la configuración de Google.
2. ✅ **Hoy mismo:** Pedirle al equipo técnico que saque esa contraseña del archivo interno y la guarde en un lugar seguro.

---

### ❌ Problema 2 de 4 — El sistema está en "modo prueba" frente a los usuarios reales

**¿Qué pasó?**
El sistema tiene dos modos de funcionamiento: uno para que los programadores hagan pruebas (modo prueba) y otro para el uso real (modo producción). El modo prueba muestra mensajes de error muy detallados, incluyendo información interna del sistema que nunca debería ver un usuario.

**Analogía:** Es como si el tablero de control de un avión tuviera todos los circuitos al descubierto y cualquier pasajero pudiera tocarlos. El modo de prueba es solo para el hangar, no para el vuelo.

**¿Qué puede pasar si no se corrige?**
- Si alguien intenta acceder a una página que no existe o provoca un error, el sistema le muestra un informe detallado con rutas internas, configuraciones y hasta fragmentos del código fuente.
- Un atacante puede usar esa información para encontrar otros puntos débiles del sistema.

**¿Qué debe hacerse?**
- ✅ El equipo técnico debe cambiar una sola línea de configuración para activar el modo de producción. Es un cambio de 5 minutos.

---

### ❌ Problema 3 de 4 — Cualquier persona puede registrarse como Docente, Secretaria o Rector

**¿Qué pasó?**
El formulario de registro de ACADEMIX permite que **cualquier persona**, sin ninguna verificación previa, elija su propio rol dentro del sistema. Esto incluye roles como Docente, Secretaria, Rector o incluso Administrador.

**Analogía:** Es como si la puerta de entrada al colegio tuviera un formulario que dice "¿A qué cargo pertenece usted?" y con solo marcar "Rector", el sistema le abriera la sala de rectoría sin pedir ningún documento.

**¿Qué puede pasar si no se corrige?**
- Una persona externa puede registrarse como Secretaria y acceder a los expedientes de todos los estudiantes, incluyendo datos personales, médicos y financieros.
- Puede ver, modificar o exportar calificaciones de todos los grados.
- Puede registrar pagos falsos en el módulo financiero.

**¿Qué debe hacerse?**
- ✅ El equipo técnico debe configurar el registro para que solo se puedan crear cuentas de Estudiante o Padre de Familia de forma autónoma.
- ✅ Las cuentas de Docente, Secretaria y Rector deben ser creadas **únicamente por el Administrador del sistema**, con verificación previa.

---

### ❌ Problema 4 de 4 — El servidor que usa el sistema no es apto para uso real

**¿Qué pasó?**
El programa que arranca ACADEMIX en la red del colegio utiliza un motor de servidor diseñado únicamente para pruebas internas de programadores. La propia documentación oficial de Django (el framework con el que está construido ACADEMIX) indica que ese servidor "no debe usarse en producción bajo ninguna circunstancia".

**Analogía:** Es como transportar a los estudiantes en el camión de obras del colegio en lugar de en un bus escolar homologado. Puede que funcione, pero no está hecho para eso, no tiene cinturones de seguridad y puede fallar en cualquier momento.

**¿Qué puede pasar si no se corrige?**
- El sistema puede caerse si varios usuarios se conectan al mismo tiempo.
- No ofrece ninguna protección contra ataques básicos de internet.
- No está preparado para manejar información sensible de forma segura.

**¿Qué debe hacerse?**
- ✅ El equipo técnico debe instalar un servidor de aplicaciones profesional (se llama **Waitress** para Windows). Es gratuito y compatible con el sistema. El cambio tarda aproximadamente una hora.

---

## 🟠 PROBLEMAS ALTOS — Corregir Esta Semana

---

### ⚠️ Problema 5 — El sistema no tiene "cerrojo automático" ante intentos de contraseña

**En términos sencillos:**
Si alguien intenta adivinar la contraseña de un usuario, el sistema lo dejará intentarlo **sin límite**, miles de veces, hasta que lo logre.

**Analogía:** Un cajero automático que nunca bloquea la tarjeta, sin importar cuántas veces se ingrese el PIN incorrecto.

**Consecuencia:** Un atacante puede usar programas automáticos que prueban millones de contraseñas hasta dar con la correcta.

**Solución:** Configurar el sistema para que **bloquee el acceso por 15 minutos** después de 5 intentos fallidos seguidos.

---

### ⚠️ Problema 6 — La firma digital del sistema es débil y está a la vista

**En términos sencillos:**
Todo sistema informático tiene una "firma secreta" que protege las sesiones de los usuarios, los formularios y los enlaces de recuperación de contraseña. Esta firma debe ser secreta y única. En ACADEMIX, esa firma tiene un valor de respaldo que es predecible y está escrita directamente en el código.

**Analogía:** Es como si la firma del Rector estuviera impresa en un sello de goma que cualquier empleado puede usar.

**Consecuencia:** Alguien podría falsificar sesiones de usuario o manipular formularios del sistema.

**Solución:** El equipo técnico debe generar una firma única y secreta y guardarla de forma segura, separada del código del sistema.

---

### ⚠️ Problema 7 — La contraseña de la base de datos está en blanco por defecto

**En términos sencillos:**
La base de datos de ACADEMIX (donde están todos los datos de estudiantes, calificaciones, pagos, etc.) tiene configurada una contraseña vacía como valor por defecto, y el acceso se hace con el usuario administrador máximo del servidor de base de datos.

**Analogía:** La caja fuerte del colegio no tiene combinación y el nombre del responsable es "administrador general".

**Consecuencia:** Si alguien accede a la red interna del colegio, puede intentar conectarse directamente a la base de datos sin contraseña.

**Solución:** Configurar una contraseña robusta para la base de datos y crear un usuario con permisos mínimos, exclusivo para ACADEMIX.

---

### ⚠️ Problema 8 — Los archivos del expediente no verifican su tipo antes de guardarse

**En términos sencillos:**
Cuando un padre de familia o secretaria sube un documento al expediente de un estudiante (por ejemplo, un certificado médico), el sistema no verifica si el archivo es realmente lo que dice ser. Alguien podría subir un archivo malicioso con extensión `.pdf`.

**Analogía:** La recepción del colegio acepta cualquier sobre sin revisar su contenido, aunque pudiera contener algo peligroso.

**Consecuencia:** Podría almacenarse contenido dañino en los servidores del colegio.

**Solución:** El sistema debe verificar que los archivos sean únicamente documentos PDF o imágenes (JPG, PNG) y que no superen los 10 MB.

---

### ⚠️ Problema 9 — No hay protecciones básicas de seguridad web activadas

**En términos sencillos:**
Los navegadores de internet tienen una serie de "normas de seguridad" que los servidores pueden activar para proteger a sus usuarios. Estas normas evitan, por ejemplo, que alguien intercepte la sesión de un docente mientras usa el sistema. En ACADEMIX, esas protecciones no están activadas.

**Solución:** El equipo técnico puede activarlas con unas pocas líneas de configuración. No requiere ningún cambio visible para los usuarios.

---

### ⚠️ Problema 10 — El registro de actividad puede ser engañado para ocultar la IP real de un atacante

**En términos sencillos:**
ACADEMIX registra todos los movimientos importantes: quién inició sesión, desde qué computadora, qué cambios hizo. Esto es muy valioso para investigar incidentes. Sin embargo, encontramos que alguien con conocimientos técnicos puede "mentirle" al sistema sobre su dirección IP real, haciendo que el registro de auditoría quede con datos falsos.

**Consecuencia:** Si ocurre un incidente de seguridad, sería más difícil rastrear al responsable.

**Solución:** Configurar el sistema para que solo confíe en la información de red cuando proviene de equipos verificados (como el router del colegio).

---

## 🟡 ASPECTOS A MEJORAR — Sin Urgencia Inmediata

---

### 📌 Mejora 1 — Cambiar el tipo de institución requiere autenticación

Actualmente, el tipo de institución del sistema (colegio, universidad, SENA, academia) puede cambiarse desde la página de inicio de sesión, sin necesidad de estar autenticado. Esto no representa un riesgo grave, pero debería ser una acción exclusiva del Rector o Administrador desde dentro del sistema.

---

### 📌 Mejora 2 — Proteger el acceso a documentos almacenados

Los documentos del expediente (PDFs, imágenes) están guardados en una carpeta del servidor. En el entorno actual de red local esto no es un problema, pero si el sistema se desplegara en internet, esa carpeta podría ser accesible sin autenticación. Se recomienda protegerla adecuadamente antes de cualquier despliegue externo.

---

### 📌 Mejora 3 — Simplificar la configuración de orígenes CSRF

Hay una configuración técnica que protege los formularios del sistema contra ataques externos. Actualmente se genera de forma automática al iniciar el servidor, lo que puede generar permisos más amplios de lo necesario en redes no controladas. Se recomienda gestionarla de forma explícita.

---

## 🟢 RECOMENDACIONES ADICIONALES

---

### 💡 Recomendación 1 — Alertas automáticas ante intentos de acceso sospechosos

El sistema ya guarda un registro de todos los intentos de inicio de sesión fallidos. Se recomienda que, cuando haya **5 o más intentos fallidos desde la misma computadora en menos de 10 minutos**, el sistema envíe automáticamente una alerta al administrador por correo electrónico.

---

### 💡 Recomendación 2 — Organizar mejor las herramientas de configuración interna

Existen varios archivos de herramientas de configuración y carga de datos que están ubicados en la carpeta principal del sistema. Si alguien los ejecuta accidentalmente en el entorno real, podrían modificar datos. Se recomienda moverlos a una carpeta separada y protegida, con una advertencia que impida su ejecución en el entorno de producción.

---

## ✅ LO QUE EL SISTEMA HACE BIEN

Es importante reconocer que ACADEMIX tiene una base de seguridad sólida. Estos son los puntos positivos encontrados durante la revisión:

| ✅ | Qué protege |
|---|---|
| **Registro de auditoría inmutable** | Guarda un historial permanente de quién hizo qué y cuándo, incluyendo intentos fallidos de acceso. No se puede borrar ni modificar. |
| **Control de acceso por roles** | Cada tipo de usuario (estudiante, docente, secretaria, rector) solo puede ver y hacer lo que le corresponde según su rol. Está aplicado en todo el sistema. |
| **Transacciones seguras en la base de datos** | Si una operación falla a mitad de camino, el sistema revierte todos los cambios automáticamente. No quedan datos a medias. |
| **Cambio de contraseña sin cerrar sesión** | Al cambiar la contraseña, la sesión activa del usuario se mantiene de forma segura, sin necesidad de volver a iniciar sesión. |
| **Contraseñas con requisitos mínimos** | El sistema exige contraseñas de al menos 8 caracteres y verifica que no sean demasiado comunes o predecibles. |
| **Protección de formularios (CSRF)** | Los formularios del sistema están protegidos contra un tipo de ataque que podría hacer que un usuario haga acciones sin darse cuenta. |
| **Cambio de contraseña obligatorio en el primer acceso** | Cuando se crea una cuenta nueva, el sistema obliga al usuario a cambiar la contraseña temporal antes de poder usar el sistema. |
| **Control de descarga de documentos del expediente** | Solo las personas autorizadas según su rol pueden descargar documentos del expediente de un estudiante. |
| **Control financiero restringido** | Solo la secretaría y administración pueden registrar pagos y ver el estado de cartera. Los estudiantes y padres solo pueden consultar su propia información. |

---

## 📅 Plan de Acción — ¿Qué hacer y cuándo?

### Esta semana — Urgente 🚨
- [ ] Cambiar la contraseña del correo de Gmail institucional
- [ ] Pedirle al equipo técnico que retire esa contraseña del archivo de configuración
- [ ] Bloquear el auto-registro de roles privilegiados (Docente, Secretaria, Rector)
- [ ] Activar el modo de producción del sistema (desactivar modo prueba)

### Esta semana — Importante 📋
- [ ] Cambiar la firma de seguridad del sistema por una robusta y secreta
- [ ] Configurar contraseña segura para la base de datos
- [ ] Activar el bloqueo automático tras intentos fallidos de contraseña

### Antes de abrir el sistema al público 🏫
- [ ] Instalar el servidor profesional (Waitress)
- [ ] Activar los headers de seguridad web
- [ ] Agregar validación de archivos subidos al expediente
- [ ] Proteger el historial de auditoría contra manipulación de IPs

### Mejoras continuas 📈
- [ ] Configurar alertas automáticas por intentos de acceso sospechosos
- [ ] Organizar y proteger las herramientas de configuración interna

---

## 📞 ¿Qué hacer ahora?

Comparta este reporte con el equipo técnico de desarrollo. Cada problema tiene una solución técnica clara y documentada. Las correcciones prioritarias (semana 1) pueden realizarse en **menos de un día de trabajo**.

Si tiene preguntas sobre algún punto específico de este reporte, no dude en consultarlas.

---

*Reporte elaborado por el Equipo de Revisión de Seguridad — ACADEMIX*
*Metodología aplicada: Revisión de código fuente, análisis de configuración, evaluación de flujos de acceso y autenticación.*
*Clasificación: Confidencial — Solo para uso institucional interno*
