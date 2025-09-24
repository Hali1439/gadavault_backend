# gada_vault/settings/__init__.py
import os

# Initialize Django settings depending on environment: use production settings on Railway.
if os.getenv("RAILWAY_ENVIRONMENT"):
    from .prod import *
else:
    from .dev import *