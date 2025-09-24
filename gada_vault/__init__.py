# gada_vault/__init__.py
from .celery import app as celery_app

# Expose Celery app for celery -A gada_vault
all = ("celery_app",)