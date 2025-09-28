# gada_vault/settings/dev.py
from .base import *


DEBUG = True

SECRET_KEY = config("DJANGO_SECRET_KEY", default="insecure-dev-key")

ALLOWED_HOSTS = ["*"]

# Use local SQLite for dev unless DATABASE_URL is set
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR}/db.sqlite3",
        conn_max_age=0,
    )
}

# Faster password hashing for dev
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Debug toolbar or other dev-only apps
INSTALLED_APPS += [
    # "debug_toolbar",
]

MIDDLEWARE += [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
]# gada_vault/settings/dev.py
from .base import *

DEBUG = True
SECRET_KEY = config("DJANGO_SECRET_KEY", default="insecure-dev-key")

ALLOWED_HOSTS = ["*"]

# Dev database: default to SQLite unless DATABASE_URL is set
import dj_database_url

DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR}/db.sqlite3",
        conn_max_age=0,
    )
}

# Faster password hashing in dev
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Explicitly inherit INSTALLED_APPS and MIDDLEWARE from base
INSTALLED_APPS = list(INSTALLED_APPS)  # now Pylance sees it
MIDDLEWARE = list(MIDDLEWARE)          # same here

# Optional dev tools (uncomment if installed)
# INSTALLED_APPS += ["debug_toolbar"]
# MIDDLEWARE = ["debug_toolbar.middleware.DebugToolbarMiddleware"] + MIDDLEWARE

# CORS and CSRF for dev
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS

# Security relaxed for dev
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

print("💻 Development settings loaded successfully")

