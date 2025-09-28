# gada_vault/settings/__init__.py
import os

# Default to dev if nothing else is set
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gada_vault.settings.dev")
