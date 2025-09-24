# gada_vault/settings/dev.py
from .base import *

# Keep DEBUG on for local development
DEBUG = True

# Local defaults if not provided
ALLOWED_HOSTS = ["127.0.0.1", "localhost"]

# Developer-friendly CORS for local React dev server
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
