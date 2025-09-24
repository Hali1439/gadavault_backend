# gada_vault/settings/__init__.py
import os

# Decide which settings to load based on environment variable.
# On Railway set RAILWAY_ENVIRONMENT (or set DJANGO_SETTINGS_MODULE explicitly).
if os.getenv("RAILWAY_ENVIRONMENT") or os.getenv("DJANGO_SETTINGS_MODULE", "").endswith(".prod"):
    # Production: import from prod which itself imports base
    from .prod import *
else:
    # Default to development settings for local work.
    from .dev import *
