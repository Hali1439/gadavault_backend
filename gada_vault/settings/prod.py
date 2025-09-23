# gada_vault/settings/prod.py
from .base import *

DEBUG = False

ALLOWED_HOSTS = ["https://gadavaultbackend-production.up.railway.app", ".railway.app"]

CORS_ALLOWED_ORIGINS = [
    "https://gadavault.vercel.app/",
]

CSRF_TRUSTED_ORIGINS = [
    "https://gadavault.vercel.app/",
]
