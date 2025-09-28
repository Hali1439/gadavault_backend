# gada_vault/settings/dev.py
from .base import *

DEBUG = True

print("💻 Loading development settings")

# Development-specific allowed hosts
ALLOWED_HOSTS = ["127.0.0.1", "localhost", "0.0.0.0", "192.168.1.100"]

# Developer-friendly CORS for local development
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000", 
    "http://127.0.0.1:8000",
]

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
]

# Relax security for development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Enhanced logging for development
LOGGING['root']['level'] = 'DEBUG'
LOGGING['loggers']['django']['level'] = 'INFO'

# Optional: Add debug toolbar if available, but don't break if not
try:
    # Try to import and configure debug toolbar
    import django
    from django.conf import settings
    
    if 'debug_toolbar' not in settings.INSTALLED_APPS:
        settings.INSTALLED_APPS += ['debug_toolbar']
        settings.MIDDLEWARE = ['debug_toolbar.middleware.DebugToolbarMiddleware'] + settings.MIDDLEWARE
        settings.INTERNAL_IPS = ['127.0.0.1', 'localhost']
        print("🔧 Django Debug Toolbar configured")
except (ImportError, Exception) as e:
    print(f"⚠️ Django Debug Toolbar not available: {e}")
    print("💡 Run: pip install django-debug-toolbar to enable debugging features")

# Database configuration for development
if 'default' in DATABASES and DATABASES['default'].get('ENGINE', '').endswith('postgresql'):
    DATABASES['default']['OPTIONS'] = {
        'options': '-c search_path=public',
        'connect_timeout': 10,
    }

print("✅ Development settings configured successfully")