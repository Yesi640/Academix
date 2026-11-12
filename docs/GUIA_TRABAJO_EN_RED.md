# 🌐 Guía de Trabajo en Red Local para ACADEMIX

Esta guía explica cómo utilizar el sistema **ACADEMIX** en una red de área local (LAN, Wi-Fi o red cableada de la institución escolar) para que múltiples directivos, profesores, estudiantes y secretarias puedan conectarse de forma concurrente desde diferentes computadoras, laptops, teléfonos móviles o tablets.

---

## 🚀 1. Inicio Rápido (En la computadora Servidor)

La computadora principal donde está guardado el proyecto actuará como el **Servidor de ACADEMIX**.

1. Abre la carpeta del proyecto `c:\Academix`.
2. Haz doble clic sobre:
   👉 **`iniciar_servidor_red.bat`**
3. El lanzador inteligente:
   - Detectará automáticamente tu dirección IP en la red local (ejemplo: `10.8.182.30` o `192.168.1.50`).
   - Iniciará el servidor escuchando para toda la red (`0.0.0.0:8000`).
   - Mostrará en pantalla la URL exacta que debes compartir con los demás usuarios.

---

## 📱 2. Acceso desde otros Dispositivos (Clientes)

Cualquier dispositivo conectado a la **misma red Wi-Fi o red cableada** puede ingresar de la siguiente manera:

1. Abre cualquier navegador moderno (Google Chrome, Firefox, Safari, Edge, Brave).
2. En la barra de direcciones, escribe la URL del servidor que apareció en consola:
   ```text
   http://<IP_DEL_SERVIDOR>:8000/
   ```
   *Ejemplo real:* `http://10.8.182.30:8000/`

3. Aparecerá la pantalla oficial de inicio de sesión de **ACADEMIX**.

---

## 🛡️ 3. Configuración del Firewall de Windows (Paso Único)

Si los otros dispositivos no logran conectarse (la página carga indefinidamente o dice "No se puede conectar"):
1. En la computadora servidor, haz doble clic sobre:
   👉 **`firewall.bat`**
2. Se solicitarán permisos de Administrador y se habilitará automáticamente el puerto TCP 8000 en el Firewall de Windows Defender.
3. ¡Listo! Los equipos de la red tendrán libre acceso.

---

## 👥 4. Usuarios y Roles de Prueba Disponibles

El sistema cuenta con cuentas preconfiguradas para pruebas en red:

| Rol | Usuario | Contraseña | Propósito |
| :--- | :--- | :--- | :--- |
| **Administrador** | `admin` / `yurle` | *(Configurada)* | Control total, configuración y auditoría |
| **Rector / Directivo** | `rector` | `DemoPassword123*` | Tableros de mando, alertas y estadísticas |
| **Secretaría** | `secretaria` / `nurys` | `nurys123` *(para nurys)* | Matrículas, cursos, asignaturas y expedientes |
| **Docente** | `docente` / `dulce` | `dulce123` *(para dulce)* | Registro de notas, calificaciones y asistencia |
| **Estudiante** | `estudiante` / `yesi` | `yesi123` *(para yesi)* | Consulta de boletines, notas y tareas |
| **Acudiente** | `acudiente` | `DemoPassword123*` | Seguimiento académico y asistencias de acudidos |

---

## ⚙️ 5. Opciones Avanzadas de Arquitectura de Red

### A. Concurrencia con Base de Datos SQLite (Por Defecto)
- ACADEMIX incluye optimizaciones automáticas para red local con SQLite:
  - **Modo WAL (Write-Ahead Logging):** Permite lecturas simultáneas mientras se realizan escrituras.
  - **Timeout de espera (30s):** Evita el error `database is locked` cuando dos docentes guardan calificaciones al mismo tiempo.
  - Recomendado para pruebas, laboratorios y colegios pequeños (hasta 20-30 usuarios simultáneos).

### B. Escalabilidad con Servidor MySQL Dedicado
Si la institución educativa cuenta con un servidor de base de datos MySQL centralizado en la red:
1. Abre el archivo `.env` en la raíz del proyecto.
2. Desactiva el fallback de SQLite:
   ```env
   USE_SQLITE_FALLBACK=False
   DB_ENGINE=mysql
   DB_NAME=academix_db
   DB_USER=academix_user
   DB_PASSWORD=tu_password_seguro
   DB_HOST=192.168.1.100   # <-- IP del servidor MySQL en la red
   DB_PORT=3306
   ```

---

## ❓ 6. Preguntas Frecuentes y Solución de Problemas

#### 1. ¿Por qué otros dispositivos no pueden conectarse?
- **Verifica la red Wi-Fi:** Asegúrate de que el celular o la otra PC esté conectada al **mismo router/red Wi-Fi** que la computadora servidor (no en datos móviles ni en la red "Invitados").
- **Tipo de red en Windows:** En la computadora servidor, abre Configuración de Windows > Red e Internet y asegúrate de que el perfil de red esté en **Red privada** (en red pública Windows aplica bloqueos más estrictos).
- **Ejecuta `firewall.bat`:** Abre el puerto 8000 en el Firewall.

#### 2. Mi dirección IP cambió (IP dinámica)
- Los routers asignan direcciones IP por DHCP que pueden variar al reiniciar.
- El script `iniciar_servidor_red.bat` detecta automáticamente la nueva IP cada vez que lo ejecutas y te mostrará la URL actualizada en pantalla.
