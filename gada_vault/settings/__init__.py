# gada_vault/settings/__init__.py
"""
Auto-detect environment (Railway vs Local) and load settings.
"""

import os

# Railway sets this automatically in containers
if os.getenv("RAILWAY_ENVIRONMENT"):
    from .prod import *
else:
    from .dev import *
