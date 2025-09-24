# gada_vault/settings/dev.py
from .base import *

# Development settings
DEBUG = True

# Local debugging hosts
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Allow React dev server origin for CORS
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# CSRF trusted origins should include scheme (no trailing slash)
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]