# gada_vault/settings/base.py
"""
Base Django settings for GadaVault - Multi-platform support for Railway & Render
"""

import os
import sys
from pathlib import Path
from datetime import timedelta

from decouple import config

# Optional dj_database_url used to parse DATABASE_URL if present
try:
    import dj_database_url
except Exception:
    dj_database_url = None

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# -----------------------------
# Platform Detection
# -----------------------------
IS_RAILWAY = bool(os.getenv("RAILWAY_ENVIRONMENT"))
IS_RENDER = bool(os.getenv("RENDER"))
IS_PRODUCTION = IS_RAILWAY or IS_RENDER

# -----------------------------
# Core Settings
# -----------------------------
SECRET_KEY = config("DJANGO_SECRET_KEY", default="dummy-secret-key-for-builds") 
DEBUG = config("DJANGO_DEBUG", default=not IS_PRODUCTION, cast=bool)
APPEND_SLASH = False

# Dynamic ALLOWED_HOSTS - will be extended in prod.py
ALLOWED_HOSTS = []

# -----------------------------
# Installed Apps & Middleware
# -----------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework.authtoken",
    "drf_yasg",
    "cloudinary",
    "corsheaders",
    "drf_spectacular",

    "apps.users.apps.UsersConfig",
    "apps.products.apps.ProductsConfig",
    "apps.designers.apps.DesignersConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "gada_vault.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "gada_vault.wsgi.application"

# -----------------------------
# Database Configuration
# -----------------------------
CONN_MAX_AGE = config("CONN_MAX_AGE", cast=int, default=600)
DATABASE_URL = config("DATABASE_URL", default="")

# Use SQLite for testing
if 'test' in sys.argv or 'pytest' in sys.argv or os.environ.get('DJANGO_TEST') == 'true':
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": ":memory:",
        }
    }
else:
    # Use PostgreSQL for development/production
    if DATABASE_URL and dj_database_url:
        # Parse DATABASE_URL (works for both Railway and Render)
        db_config = dj_database_url.parse(DATABASE_URL, conn_max_age=CONN_MAX_AGE)
        db_config.setdefault("ENGINE", "django.db.backends.postgresql")
        
        # Set SSL mode for production
        opts = db_config.setdefault("OPTIONS", {})
        if IS_PRODUCTION and "sslmode" not in opts and "sslmode=require" not in DATABASE_URL.lower():
            opts["sslmode"] = "require"
        
        opts.setdefault("options", "-c search_path=public")
        DATABASES = {"default": db_config}
        print(f"🔗 Using DATABASE_URL from environment for {'Railway' if IS_RAILWAY else 'Render' if IS_RENDER else 'production'}")
    else:
        # Local/dev fallback
        DATABASES = {
            "default": {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": config("POSTGRES_DB", default="gada_vault_db"),
                "USER": config("POSTGRES_USER", default="gada_user"),
                "PASSWORD": config("POSTGRES_PASSWORD", default=""),
                "HOST": config("POSTGRES_HOST", default="localhost"),
                "PORT": config("POSTGRES_PORT", default="5432"),
                "CONN_MAX_AGE": CONN_MAX_AGE,
                "OPTIONS": {"options": "-c search_path=public"},
            }
        }
        print("💾 Using local PostgreSQL configuration")

# Explicit auth user
AUTH_USER_MODEL = "users.User"

# -----------------------------
# DRF & JWT Configuration
# -----------------------------
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ),
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# -----------------------------
# Cloudinary Configuration
# -----------------------------
import cloudinary
cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME", default=""),
    api_key=config("CLOUDINARY_API_KEY", default=""),
    api_secret=config("CLOUDINARY_API_SECRET", default=""),
)

# -----------------------------
# Email Configuration
# -----------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config("EMAIL_HOST", default="smtp.gmail.com")
EMAIL_PORT = config("EMAIL_PORT", cast=int, default=587)
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default=True, cast=bool)
EMAIL_USE_SSL = config("EMAIL_USE_SSL", default=False, cast=bool)

DEFAULT_FROM_EMAIL = config("DEFAULT_FROM_EMAIL", default="no-reply@example.com")
CONTACT_RECEIVER_EMAIL = config("CONTACT_RECEIVER_EMAIL", default=EMAIL_HOST_USER)

# -----------------------------
# Redis / Celery Configuration
# -----------------------------
REDIS_URL = config("REDIS_URL", default=None)
CELERY_BROKER_URL = REDIS_URL or "memory://"
CELERY_RESULT_BACKEND = REDIS_URL or "cache+memory://"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

# -----------------------------
# Static & Media Files
# -----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# Storage configuration - will be overridden in prod for Whitenoise
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
    },
}

# -----------------------------
# Security (base level - enhanced in prod)
# -----------------------------
if IS_PRODUCTION:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True

# -----------------------------
# Sentry (Optional)
# -----------------------------
SENTRY_DSN = config("SENTRY_DSN", default="")
if IS_PRODUCTION and SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        send_default_pii=True,
        traces_sample_rate=1.0,
        environment="railway" if IS_RAILWAY else "render" if IS_RENDER else "production",
    )

# -----------------------------
# Logging Configuration
# -----------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        }
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO" if IS_PRODUCTION else "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO" if IS_PRODUCTION else "DEBUG",
            "propagate": False,
        },
    },
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"