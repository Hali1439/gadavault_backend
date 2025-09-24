# gada_vault/settings/prod.py
from .base import *

DEBUG = False

if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ["gadavaultbackend-production.up.railway.app"]

# Comma-separated env vars
CORS_ALLOWED_ORIGINS = [o.strip() for o in config("CORS_ALLOWED_ORIGINS", default="").split(",") if o.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in config("CSRF_TRUSTED_ORIGINS", default="").split(",") if o.strip()]
