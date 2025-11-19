"""
Django settings for HidroZen project (Django 5.1.x)
Listo para desarrollo local (SQLite por defecto) y Postgres por variables de entorno.
"""

from pathlib import Path
import os

# ==============================
# BASE & ENV
# ==============================
BASE_DIR = Path(__file__).resolve().parent.parent

# Carga .env (opcional). No falla si python-dotenv no está instalado.
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv(BASE_DIR / ".env")
except Exception:
    pass

# ==============================
# CORE & SECURITY
# ==============================
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "django-insecure-please-change-me-for-dev-only"
)

DEBUG = os.getenv("DEBUG", "True").strip().lower() == "true"

# Ej: ALLOWED_HOSTS=127.0.0.1,localhost
ALLOWED_HOSTS = [
    h.strip() for h in os.getenv("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if h.strip()
]

# Para pruebas con http://localhost:8000
# Ej: CSRF_TRUSTED_ORIGINS=http://127.0.0.1:8000,http://localhost:8000
CSRF_TRUSTED_ORIGINS = [
    o.strip() for o in os.getenv("CSRF_TRUSTED_ORIGINS", "http://127.0.0.1:8000,http://localhost:8000").split(",")
    if o.strip()
]

# ==============================
# APPS
# ==============================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Tu app
    "AppHidroZen",
]

# ==============================
# MIDDLEWARE
# ==============================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==============================
# URLS / WSGI
# ==============================
ROOT_URLCONF = "HidroZen.urls"
WSGI_APPLICATION = "HidroZen.wsgi.application"

# ==============================
# TEMPLATES
# ==============================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",                 # carpeta global de templates (opcional)
            BASE_DIR / "AppHidroZen" / "templates"  # templates de tu app
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ==============================
# DATABASES
# ==============================
# Desarrollo: SQLite por defecto.
# Producción / pruebas con Postgres: setear USE_SQLITE=False en .env y definir DB_*
USE_SQLITE = os.getenv("USE_SQLITE", "True").strip().lower() == "true"

if USE_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }
else:
    # Variables esperadas en .env (ejemplo):
    # DB_NAME=HidroZen_Data
    # DB_USER=postgres
    # DB_PASSWORD=admin123
    # DB_HOST=localhost
    # DB_PORT=5432
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("DB_NAME", "HidroZen_Data"),
            "USER": os.getenv("DB_USER", "postgres"),
            "PASSWORD": os.getenv("DB_PASSWORD", ""),
            "HOST": os.getenv("DB_HOST", "127.0.0.1"),
            "PORT": os.getenv("DB_PORT", "5432"),
            # Fuerza cliente en UTF-8 para evitar errores de decodificación en Windows
            "OPTIONS": {"options": "-c client_encoding=UTF8"},
        }
    }

# ==============================
# PASSWORD VALIDATION
# ==============================
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ==============================
# I18N / L10N / TZ
# ==============================
LANGUAGE_CODE = "es-co"
TIME_ZONE = "America/Bogota"
USE_I18N = True
USE_TZ = True

# ==============================
# STATIC & MEDIA
# ==============================
# Archivos estáticos (CSS/JS/IMG)
STATIC_URL = "/static/"
STATICFILES_DIRS = [
    BASE_DIR / "static",  # opcional: carpeta de estáticos del proyecto
]
STATIC_ROOT = BASE_DIR / "staticfiles"  # para collectstatic en despliegue

# Archivos subidos por usuarios
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# ==============================
# DEFAULTS
# ==============================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
