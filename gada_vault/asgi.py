import os
from django.core.asgi import get_asgi_application

# Set the default settings module for the 'asgi' process.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gada_vault.settings")
application = get_asgi_application()