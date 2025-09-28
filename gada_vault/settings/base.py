# gada_vault/settings/base.py
"""
Base Django settings for GadaVault.
- Uses python-decouple for environment variables.
- If DATABASE_URL is present (Railway), it will be parsed and used.
- Falls back to POSTGRES_* for local development.
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
# Core
# -----------------------------
SECRET_KEY = config("DJANGO_SECRET_KEY")  # required in production; keep it secret
DEBUG = config("DJANGO_DEBUG", default=False, cast=bool)
APPEND_SLASH = False

# ALLOWED_HOSTS read from env (comma-separated)
ALLOWED_HOSTS = [h.strip() for h in config("DJANGO_ALLOWED_HOSTS", default="*").split(",") if h.strip()]

# -----------------------------
# Installed apps / middleware (unchanged, tidy)
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
    "rest_framework.authtoken",  # Added for token authentication
    "drf_yasg",
    "cloudinary",
    "corsheaders",
     "drf_spectacular",


    "apps.users.apps.UsersConfig",
    "apps.products.apps.ProductsConfig",
    "apps.designers.apps.DesignersConfig",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # keep CORS first
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
# Database: Use SQLite for testing, PostgreSQL otherwise
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
        # Use DATABASE_URL when available (this is the Railway pattern).
        db_config = dj_database_url.parse(DATABASE_URL, conn_max_age=CONN_MAX_AGE)
        db_config.setdefault("ENGINE", "django.db.backends.postgresql")
        opts = db_config.setdefault("OPTIONS", {})
        if "sslmode" not in opts and "sslmode=require" not in DATABASE_URL.lower():
            opts["sslmode"] = "require"
        opts.setdefault("options", "-c search_path=public")
        DATABASES = {"default": db_config}
    else:
        # Local/dev fallback: use POSTGRES_* env vars
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

# Explicit auth user
AUTH_USER_MODEL = "users.User"

# -----------------------------
# DRF & JWT
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
# Cloudinary
# -----------------------------
import cloudinary
cloudinary.config(
    cloud_name=config("CLOUDINARY_CLOUD_NAME", default=""),
    api_key=config("CLOUDINARY_API_KEY", default=""),
    api_secret=config("CLOUDINARY_API_SECRET", default=""),
)

# -----------------------------
# Email
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
# Redis / Celery
# -----------------------------
REDIS_URL = config("REDIS_URL", default=None)
CELERY_BROKER_URL = REDIS_URL or "memory://"
CELERY_RESULT_BACKEND = REDIS_URL or "cache+memory://"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "UTC"

# -----------------------------
# Static / Media
# -----------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STORAGES = {
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"}
}
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

# -----------------------------
# Security for production
# -----------------------------
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True

# -----------------------------
# Sentry (optional)
# -----------------------------
SENTRY_DSN = config("SENTRY_DSN", default="")
if not DEBUG and SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        send_default_pii=True,
        traces_sample_rate=1.0,
    )

# -----------------------------
# Logging
# -----------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": "INFO"},
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"