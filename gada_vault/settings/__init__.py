# gada_vault/settings/__init__.py
import os

# Determine which settings to use based on environment
if os.getenv("RAILWAY_ENVIRONMENT"):
    # Railway deployment
    from .prod import *
    print("🚄 Loading Railway production settings")
elif os.getenv("RENDER"):
    # Render deployment
    from .prod import *  
    print("🎨 Loading Render production settings")
elif os.getenv("DJANGO_SETTINGS_MODULE", "").endswith(".prod"):
    # Explicit production request
    from .prod import *
    print("🔧 Loading explicit production settings")
else:
    # Default to development
    from .dev import *
    print("💻 Loading development settings")

# Clean up
del os