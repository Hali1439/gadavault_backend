import os
from celery import Celery

# Use default Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gada_vault.settings")
app = Celery("gada_vault")

# Load Celery config from Django settings (CELERY_ namespace)
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

# Example debug task; can be removed or left for testing purposes
@app.task(bind=True)
def debug_task(self):
    print(f"Celery debug task called. Request: {self.request!r}")