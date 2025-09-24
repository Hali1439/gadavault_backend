from .base import *

# Production settings
DEBUG = False

# Allowed hosts must be hostnames (no scheme or trailing slash)
ALLOWED_HOSTS = ["gadavaultbackend-production.up.railway.app"]  # e.g. Railway domain

# Frontend on Vercel
CORS_ALLOWED_ORIGINS = [
    "https://gadavault.vercel.app",
]

# CSRF trusted origins (include https)
CSRF_TRUSTED_ORIGINS = [
    "https://gadavault.vercel.app",
]

# Security settings (in addition to base)
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True