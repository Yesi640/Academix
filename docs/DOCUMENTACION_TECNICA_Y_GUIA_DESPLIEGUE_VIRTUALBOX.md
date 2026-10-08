# 📘 DOCUMENTACIÓN TÉCNICA Y GUÍA DE DESPLIEGUE EN SERVIDOR (VIRTUALBOX & PUTTY)
**Sistema de Gestión Académica y Control Escolar — ACADEMIX**  
*Versión: 2.5 Institucional • Fecha de Actualización: Octubre 2026*

---

## PARTE 1: RESUMEN DE CAMBIOS Y MEJORAS IMPLEMENTADAS

### 1. 📄 Reingeniería del Boletín Oficial de Calificaciones (1 Sola Hoja)
* **Formato Estrictamente Compacto (1 Sola Hoja)**:
  * Se rediseñó [`templates/reports/boletin_pdf.html`](file:///c:/Academix/templates/reports/boletin_pdf.html) y [`templates/reports/partials/single_bulletin.html`](file:///c:/Academix/templates/reports/partials/single_bulletin.html) con calibración de página (`size: letter portrait; margin: 7mm 9mm`).
  * Se eliminaron los bloques que desbordaban la hoja (tablas redundantes de la escala nacional, recuadros sobredimensionados de estadísticas y comentarios extensos por materia).
  * La **Ficha del Estudiante** se condensó en **2 filas limpias** (Estudiante, Documento, Código, Grado/Curso, Puesto y Director).
  * La **Tabla de Calificaciones** presenta Áreas y Asignaturas con formato sobrio, horas, fallas, nota definitiva y nivel de desempeño (Decreto 1290).
  * **Barra Resumen Integrada**: Promedio del periodo, asignaturas aprobadas/reprobadas, inasistencias y estado final en una sola línea horizontal.
  * **Botón de Impresión Directa**: Se integró una barra flotante en pantalla (`no-print`) para imprimir o exportar a PDF (`Ctrl + P`) de forma directa desde el navegador.

### 2. 🏛️ Automatización y Dinamismo de Firmas (Rector y Director de Grupo)
* **Eliminación Total de "María Rectora"**:
  * Se retiró el texto fijo que existía en las plantillas y en el modal de cierre.
* **Rector Dinámico de Base de Datos**:
  * La lógica en [`apps/reports/services.py`](file:///c:/Academix/apps/reports/services.py) consulta de manera automática al usuario activo con rol `RECTOR` en la base de datos (`CustomUser.objects.filter(role=CustomUser.Role.RECTOR, is_active=True)`).
  * Si la institución registra un nuevo rector o actualiza el nombre del directivo, el sistema estampa de inmediato su nombre real tanto en la rúbrica manuscrita como en el pie de página de todos los boletines.
* **Director de Grupo Dinámico**:
  * Vinculado directamente con el docente asignado a la dirección del curso (`section.homeroom_teacher`).

### 3. 📧 Motor Asíncrono de Notificaciones por Correo Electrónico (Gmail SMTP)
Implementado en [`apps/accounts/email_service.py`](file:///c:/Academix/apps/accounts/email_service.py) con soporte para plantillas HTML corporativas y fallback en texto plano:
* **Credenciales de Acceso Automáticas**: Al registrar un nuevo alumno o docente, el sistema envía un correo institucional con:
  * 📋 Su número de registro / ID único (`EST-XXXXXX`)
  * 👤 Su nombre de usuario institucional
  * 🔐 Su contraseña inicial temporal
* **Alertas de Inasistencia / Faltas**: Cada vez que se registra una falta (injustificada, justificada o tardanza) en [`apps/attendance/`](file:///c:/Academix/apps/attendance/), se envía un correo inmediato al alumno y a su acudiente con la asignatura, fecha y estado.
* **Nuevas Tareas Asignadas (Filtro Estricto por Curso)**: Cada vez que un profesor publica una tarea en [`apps/homework/`](file:///c:/Academix/apps/homework/), se notifica **exclusivamente a los estudiantes matriculados en ese curso específico**, evitando notificaciones cruzadas a otros salones.
* **Comunicados de Rectoría y Secretaría**: Al publicar una actividad institucional en [`apps/alerts/`](file:///c:/Academix/apps/alerts/), se despacha el correo según el público objetivo seleccionado (*Solo Estudiantes*, *Solo Docentes* o *Toda la Comunidad*).
* **Observador del Estudiante y Citaciones**: Notificación automática al registrar situaciones convivenciales o compromisos en [`apps/discipline/`](file:///c:/Academix/apps/discipline/).
* **Despacho Asíncrono en Segundo Plano**: Todos los envíos se procesan mediante hilos daemon (`threading.Thread`), garantizando que la plataforma nunca se demore ni se bloquee al guardar notas o asistencias.

### 4. 📝 Matriz de Tareas y Calificaciones para Docentes
* Celdas y botones compactos en [`apps/homework/`](file:///c:/Academix/apps/homework/) para mejorar el espacio de trabajo del docente.
* Restricción de permisos: Cada docente únicamente visualiza y califica las actividades de sus asignaturas.

---

## PARTE 2: GUÍA DE DESPLIEGUE EN SERVIDOR (VIRTUALBOX + PUTTY)

### Requisitos Previos:
1. Máquina Virtual en **VirtualBox** con Linux instalado (Ubuntu Server 22.04 / 24.04 LTS o Debian 12 recomendado).
2. Cliente **PuTTY** instalado en tu computadora Windows.
3. Conexión a Internet en la máquina virtual.

---

### PASO 1: Configurar la Red en VirtualBox

Para poder conectarte desde PuTTY y que otros dispositivos accedan a ACADEMIX, debes configurar la tarjeta de red de la máquina virtual:

1. En VirtualBox, selecciona tu máquina virtual y entra a **Configuración** ⚙️ ➔ **Red**.
2. **Opción A (Recomendada - Adaptador Puente / Bridged):**
   * En *Conectado a*, selecciona: **Adaptador Puente** (Bridged Adapter).
   * En *Nombre*, selecciona tu tarjeta de red física (tu tarjeta Wi-Fi o Ethernet de la laptop/PC).
   * Haz clic en **Aceptar**.
   * *Ventaja:* La máquina virtual obtiene una dirección IP propia dentro de tu red local (ejemplo: `192.168.1.50` o `10.8.x.x`), permitiendo que cualquier celular o PC del colegio o casa entre al sistema.
3. **Opción B (Alternativa - NAT con Reenvío de Puertos):**
   * Si estás en una red restringida, mantén *Conectado a:* **NAT**.
   * Haz clic en **Avanzadas** ➔ **Reenvío de puertos**.
   * Agrega dos reglas:
     * Regla 1 (SSH): IP anfitrión: `127.0.0.1` | Puerto anfitrión: `2222` | Puerto invitado: `22`
     * Regla 2 (Web): IP anfitrión: `127.0.0.1` | Puerto anfitrión: `8000` | Puerto invitado: `8000`

---

### PASO 2: Obtener la IP de la Máquina Virtual

1. Inicia la máquina virtual en VirtualBox e inicia sesión en la consola negra de Linux con tu usuario y contraseña.
2. Ejecuta el comando:
   ```bash
   ip a
   ```
3. Busca la interfaz de red (usualmente llamada `enp0s3`, `eth0` o similar) y copia la dirección `inet` (ejemplo: `192.168.1.85`).

---

### PASO 3: Conectar mediante PuTTY desde Windows

1. Abre **PuTTY** en tu computadora con Windows.
2. En el campo **Host Name (or IP address)**:
   * Si usaste **Adaptador Puente**: Escribe la IP de la máquina virtual (ejemplo: `192.168.1.85`). Puerto: `22`.
   * Si usaste **NAT con Reenvío de Puertos**: Escribe `127.0.0.1` y en Puerto escribe `2222`.
3. En *Saved Sessions*, escribe `Academix-Server` y haz clic en **Save** para guardar la sesión.
4. Haz clic en **Open**.
5. Si aparece una advertencia de seguridad de la clave SSH (*PuTTY Security Alert*), haz clic en **Accept**.
6. Escribe tu usuario de Linux y presiona Enter, luego escribe tu contraseña (los caracteres no se mostrarán al escribir por seguridad) y presiona Enter.

---

### PASO 4: Preparar el Entorno en el Servidor Linux

Una vez dentro de la terminal de PuTTY, actualiza el sistema e instala Python, Git y dependencias de compilación ejecutando los siguientes comandos:

```bash
# 1. Actualizar repositorios del sistema
sudo apt update && sudo apt upgrade -y

# 2. Instalar herramientas necesarias
sudo apt install -y python3 python3-pip python3-venv git build-essential libssl-dev libffi-dev ufw curl
```

---

### PASO 5: Descargar el Código desde GitHub

Clona el repositorio oficial de ACADEMIX con todas las actualizaciones:

```bash
# 1. Ir a la carpeta raíz de aplicaciones o directorio de usuario
cd ~

# 2. Clonar el repositorio
git clone https://github.com/Yesi640/Academix.git

# 3. Entrar a la carpeta del proyecto
cd Academix
```

---

### PASO 6: Configurar el Entorno Virtual de Python

Crea el entorno virtual e instala los paquetes requeridos por el sistema:

```bash
# 1. Crear entorno virtual
python3 -m venv venv

# 2. Activar el entorno virtual
source venv/bin/activate

# 3. Actualizar pip e instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn
```

---

### PASO 7: Configurar el Archivo de Variables de Entorno (`.env`)

Crea el archivo `.env` en la raíz de `~/Academix`:

```bash
nano .env
```

Pega la siguiente configuración (ajustada para el servidor):

```env
DEBUG=False
SECRET_KEY=academix-super-secure-production-key-2026!#sena
ALLOWED_HOSTS=*
USE_SQLITE_FALLBACK=True
CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://127.0.0.1:8000

# CONFIGURACIÓN DE CORREO INSTITUCIONAL (GMAIL SMTP)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=yesirethsena317@gmail.com
EMAIL_HOST_PASSWORD=cbji jrue guiq buki
DEFAULT_FROM_EMAIL=ACADEMIX <yesirethsena317@gmail.com>
```

> **Para guardar en nano:** Presiona `Ctrl + O`, presiona `Enter`, y luego sal con `Ctrl + X`.

---

### PASO 8: Ejecutar Migraciones y Recolectar Archivos Estáticos

Con el entorno virtual activado (`(venv)`):

```bash
# 1. Aplicar migraciones de la base de datos
python manage.py migrate

# 2. Recolectar archivos CSS, JS e imágenes
python manage.py collectstatic --noinput

# 3. (Opcional) Si necesitas crear un nuevo superusuario administrador:
# python manage.py createsuperuser
```

---

### PASO 9: Abrir el Firewall del Servidor

Asegúrate de permitir el tráfico en los puertos de conexión:

```bash
sudo ufw allow 22/tcp
sudo ufw allow 8000/tcp
sudo ufw allow 80/tcp
sudo ufw --force enable
```

---

### PASO 10: Iniciar el Servidor en Producción

#### Opción A: Prueba Inmediata en Primer Plano (Para verificar)
```bash
python manage.py runserver 0.0.0.0:8000
```
*Abre el navegador en Windows e ingresa a: `http://<IP_DE_TU_MAQUINA_VIRTUAL>:8000`.*

---

#### Opción B: Servicio Permanente en Segundo Plano con Systemd (Recomendado para Producción)
Para que el servidor se mantenga funcionando aunque cierres la ventana de PuTTY o se reinicie la máquina virtual:

1. Crea el archivo de servicio:
   ```bash
   sudo nano /etc/systemd/system/academix.service
   ```

2. Pega la siguiente definición (ajusta `tu_usuario` por tu nombre de usuario en Linux):
   ```ini
   [Unit]
   Description=Servidor Web ACADEMIX Gunicorn
   After=network.target

   [Service]
   User=tu_usuario
   Group=tu_usuario
   WorkingDirectory=/home/tu_usuario/Academix
   ExecStart=/home/tu_usuario/Academix/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 config.wsgi:application
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```

3. Habilita e inicia el servicio:
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl start academix
   sudo systemctl enable academix
   ```

4. Verificar estado del servicio:
   ```bash
   sudo systemctl status academix
   ```

---

### 🌐 ¿Cómo Acceder al Sistema desde Cualquier Dispositivo?

Desde cualquier computador, tablet o celular conectado a la misma red Wi-Fi o red cableada, abre el navegador web y digita:

```text
http://<IP_DEL_SERVIDOR_VIRTUALBOX>:8000
```
*(Ejemplo: `http://192.168.1.85:8000`)*

---

### 🔄 Cómo Actualizar el Servidor en el Futuro
Cada vez que hagamos cambios en el código y los subamos a GitHub, simplemente entra por PuTTY a la máquina virtual y corre:

```bash
cd ~/Academix
git pull origin main
source venv/bin/activate
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart academix
```
