# gada_vault/settings/prod.py
from .base import *

DEBUG = False

print(f"🏗️ Configuring production settings for {'Railway' if IS_RAILWAY else 'Render'}")

# -----------------------------
# Platform-Specific Domain Configuration
# -----------------------------
ALLOWED_HOSTS = []

if IS_RAILWAY:
    # Railway domain configuration
    RAILWAY_PUBLIC_DOMAIN = os.getenv('RAILWAY_PUBLIC_DOMAIN', '')
    RAILWAY_STATIC_URL = os.getenv('RAILWAY_STATIC_URL', '')
    
    if RAILWAY_PUBLIC_DOMAIN:
        ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)
        print(f"🚄 Added Railway public domain: {RAILWAY_PUBLIC_DOMAIN}")
    
    if RAILWAY_STATIC_URL:
        # Remove 'static.' prefix to get main domain
        main_domain = RAILWAY_STATIC_URL.replace('static.', '').replace('https://', '').replace('http://', '').split('/')[0]
        if main_domain and main_domain not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(main_domain)
            print(f"🚄 Added Railway static domain: {main_domain}")
    
    # Always include Railway domains
    RAILWAY_DOMAINS = ['.railway.app', '.up.railway.app']
    for domain in RAILWAY_DOMAINS:
        if domain not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(domain)
    print("🚄 Added generic Railway domains")

elif IS_RENDER:
    # Render domain configuration
    RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME', '')
    if RENDER_EXTERNAL_HOSTNAME:
        ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)
        print(f"🎨 Added Render external hostname: {RENDER_EXTERNAL_HOSTNAME}")
    
    # Always include Render domains
    RENDER_DOMAINS = ['.onrender.com']
    for domain in RENDER_DOMAINS:
        if domain not in ALLOWED_HOSTS:
            ALLOWED_HOSTS.append(domain)
    print("🎨 Added generic Render domains")

# Add any manually specified hosts from environment
env_hosts = [h.strip() for h in config("DJANGO_ALLOWED_HOSTS", default="").split(",") if h.strip()]
for host in env_hosts:
    if host not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(host)
        print(f"📝 Added manual host: {host}")

print(f"🌐 Final ALLOWED_HOSTS: {ALLOWED_HOSTS}")

# -----------------------------
# Enhanced Security Settings
# -----------------------------
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# -----------------------------
# Static Files with Whitenoise
# -----------------------------
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# -----------------------------
# CORS & CSRF Settings
# -----------------------------
CORS_ALLOWED_ORIGINS = []
CSRF_TRUSTED_ORIGINS = []

# Add platform-specific origins
for host in ALLOWED_HOSTS:
    if not host.startswith('.'):
        # For specific domains
        if not host.startswith(('http://', 'https://')):
            https_origin = f"https://{host}"
            CORS_ALLOWED_ORIGINS.append(https_origin)
            CSRF_TRUSTED_ORIGINS.append(https_origin)
    else:
        # For wildcard domains
        CORS_ALLOWED_ORIGIN_REGEXES = [
            rf"^https://\w+{host}$",
        ]

# Add any manual CORS origins from environment
env_cors_origins = [o.strip() for o in config("CORS_ALLOWED_ORIGINS", default="").split(",") if o.strip()]
for origin in env_cors_origins:
    if origin not in CORS_ALLOWED_ORIGINS:
        CORS_ALLOWED_ORIGINS.append(origin)
        print(f"🎯 Added manual CORS origin: {origin}")

# Add any manual CSRF origins from environment  
env_csrf_origins = [o.strip() for o in config("CSRF_TRUSTED_ORIGINS", default="").split(",") if o.strip()]
for origin in env_csrf_origins:
    if origin not in CSRF_TRUSTED_ORIGINS:
        CSRF_TRUSTED_ORIGINS.append(origin)
        print(f"🛡️ Added manual CSRF origin: {origin}")

print(f"🎯 CORS allowed origins: {CORS_ALLOWED_ORIGINS}")
print(f"🛡️ CSRF trusted origins: {CSRF_TRUSTED_ORIGINS}")

# -----------------------------
# Database Optimization for Production
# -----------------------------
if 'default' in DATABASES:
    DATABASES['default']['CONN_MAX_AGE'] = 600
    DATABASES['default']['DISABLE_SERVER_SIDE_CURSORS'] = True

print("✅ Production settings configured successfully")