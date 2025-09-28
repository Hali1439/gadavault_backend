# gada_vault/settings/prod.py
from .base import *

DEBUG = False

# Automatically include Railway domain
railway_domain = os.getenv("RAILWAY_STATIC_URL", "").replace("static.", "")
if railway_domain and railway_domain not in ALLOWED_HOSTS:
    ALLOWED_HOSTS.append(railway_domain)

# Also include the generic Railway domain
if "railway.app" not in " ".join(ALLOWED_HOSTS):
    ALLOWED_HOSTS.append(".railway.app")

# Your existing CORS settings...
CORS_ALLOWED_ORIGINS = [o.strip() for o in config("CORS_ALLOWED_ORIGINS", default="").split(",") if o.strip()]
CSRF_TRUSTED_ORIGINS = [o.strip() for o in config("CSRF_TRUSTED_ORIGINS", default="").split(",") if o.strip()]