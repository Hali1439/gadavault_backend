# gada_vault/settings/dev.py
from .base import INSTALLED_APPS as BASE_APPS, MIDDLEWARE as BASE_MIDDLEWARE, BASE_DIR, config

DEBUG = True
SECRET_KEY = config("DJANGO_SECRET_KEY", default="insecure-dev-key")

ALLOWED_HOSTS = ["*"]

# Copy base apps and middleware so linter knows they exist
INSTALLED_APPS = list(BASE_APPS)
MIDDLEWARE = list(BASE_MIDDLEWARE)

# Dev database: SQLite fallback
import dj_database_url
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR}/db.sqlite3",
        conn_max_age=0,
    )
}

# Dev CORS and CSRF
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# Relax security
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

print("💻 Development settings loaded successfully")
