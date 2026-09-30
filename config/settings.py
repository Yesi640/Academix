"""
Django settings for ACADEMIX project.
Sistema Integral de Gestión Académica, Control de Calificaciones, Asistencia y Auditoría Escolar.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cargar variables de entorno desde .env
load_dotenv(BASE_DIR / '.env')

# SEGURIDAD
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-academix-key-2026-sena-adsi')
DEBUG = os.getenv('DEBUG', 'True').lower() in ('true', '1', 'yes')

# Hosts permitidos (acepta '*' para red local y lee desde .env)
_raw_allowed_hosts = os.getenv('ALLOWED_HOSTS', '*').split(',')
ALLOWED_HOSTS = [host.strip() for host in _raw_allowed_hosts if host.strip()]
if not ALLOWED_HOSTS or '*' in ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['*']

# ORÍGENES DE CONFIANZA CSRF (Imprescindible para formularios y login en red local en Django 4 y 5)
_raw_csrf = os.getenv('CSRF_TRUSTED_ORIGINS', '')
CSRF_TRUSTED_ORIGINS = [origin.strip() for origin in _raw_csrf.split(',') if origin.strip()]

# Detección automática de IPs locales del servidor para evitar bloqueos CSRF (403) en la red
import socket
try:
    _hostname = socket.gethostname()
    _local_ips = socket.gethostbyname_ex(_hostname)[2]
except Exception:
    _local_ips = []

for _host in ['localhost', '127.0.0.1'] + _local_ips:
    for _scheme in ['http://', 'https://']:
        for _port in ['', ':8000', ':8080']:
            _origin = f"{_scheme}{_host}{_port}"
            if _origin not in CSRF_TRUSTED_ORIGINS:
                CSRF_TRUSTED_ORIGINS.append(_origin)


# APLICACIONES INSTALADAS
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

# 13 Aplicaciones Modulares de ACADEMIX
LOCAL_APPS = [
    'apps.accounts',      # Sprint 1: Usuarios, Roles, Perfiles, Autenticación
    'apps.audit',         # Sprint 1: Trazabilidad inmutable de eventos
    'apps.alerts',        # Sprint 1: Motor de alertas y semaforización
    'apps.courses',       # Sprint 2: Años lectivos, Grados y Secciones
    'apps.subjects',      # Sprint 2: Áreas de conocimiento, Asignaturas e Intensidades
    'apps.periods',       # Sprint 2: Periodos lectivos
    'apps.teachers',      # Sprint 2: Ficha docente y Asignación académica
    'apps.students',      # Sprint 2: Expediente estudiantil y Matrículas
    'apps.attendance',    # Sprint 3: Control diario de asistencia y faltas
    'apps.grades',        # Sprint 4: Planillas de notas y promedios
    'apps.homework',      # Sprint 4: Tareas y entregas
    # Módulos del Sprint 5
    'apps.rules',         # Sprint 5: Motor de validaciones académicas, promociones y cierres
    'apps.reports',       # Sprint 5: Boletines oficiales, consolidados y estadísticas
    'apps.discipline',    # Observador del Estudiante y Convivencia Escolar (Ley 1620)
    'apps.finance',       # Gestión Financiera, Cartera y Pensiones (Modo Privado)
]

THIRD_PARTY_APPS = [
    # Librerías de terceros (se pueden añadir según necesidad)
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MODELO DE USUARIO PERSONALIZADO (RESTRICCIÓN CRÍTICA)
AUTH_USER_MODEL = 'accounts.CustomUser'

# MIDDLEWARE
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # Middleware de Auditoría Inmutable para capturar usuario e IP de cada petición
    'apps.audit.middleware.AuditMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.courses.context_processors.institution_context',
                'apps.accounts.context_processors.global_theme',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# BASE DE DATOS
# Configuración MySQL (InnoDB, UTF8MB4, Transacciones Atómicas) con soporte para fallback
use_sqlite = os.getenv('USE_SQLITE_FALLBACK', 'False').lower() in ('true', '1', 'yes')
db_engine = os.getenv('DB_ENGINE', 'mysql')

if use_sqlite or db_engine == 'sqlite':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
            'ATOMIC_REQUESTS': True,
            'OPTIONS': {
                'timeout': 30,  # Espera hasta 30 segundos antes de lanzar error de bloqueo
            },
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('DB_NAME', 'academix_db'),
            'USER': os.getenv('DB_USER', 'root'),
            'PASSWORD': os.getenv('DB_PASSWORD', ''),
            'HOST': os.getenv('DB_HOST', '127.0.0.1'),
            'PORT': os.getenv('DB_PORT', '3306'),
            'ATOMIC_REQUESTS': True,  # Todas las peticiones HTTP envueltas en transacción atómica
            'OPTIONS': {
                'charset': 'utf8mb4',
                'connect_timeout': 60,
                'init_command': "SET sql_mode='STRICT_TRANS_TABLES,NO_ENGINE_SUBSTITUTION'",
            },
        }
    }

# Concurrencia SQLite para Red Local (Modo WAL - Write-Ahead Logging)
if use_sqlite or db_engine == 'sqlite':
    from django.db.backends.signals import connection_created
    from django.dispatch import receiver

    @receiver(connection_created)
    def configure_sqlite_wal(sender, connection, **kwargs):
        """Habilitar modo WAL y busy_timeout en SQLite para soporte concurrente multiusuario."""
        if connection.vendor == 'sqlite':
            try:
                cursor = connection.cursor()
                cursor.execute('PRAGMA journal_mode=WAL;')
                cursor.execute('PRAGMA busy_timeout=30000;')
            except Exception:
                pass


# VALIDACIÓN DE CONTRASEÑAS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# INTERNACIONALIZACIÓN Y ZONA HORARIA
LANGUAGE_CODE = 'es-co'
TIME_ZONE = 'America/Bogota'
USE_I18N = True
USE_TZ = True

# ARCHIVOS ESTÁTICOS Y MULTIMEDIA
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# RUTAS DE AUTENTICACIÓN
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'accounts:login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CONFIGURACIÓN DE CORREO ELECTRÓNICO INSTITUCIONAL
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() in ('true', '1', 't')
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'ACADEMIX <notificaciones@academix.edu.co>')
