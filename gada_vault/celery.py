import os
from celery import Celery

# Default Django settings module for 'celery'
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gada_vault.settings")

app = Celery("gada_vault")

# Load config from Django settings, using namespace CELERY_
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f"Request: {self.request!r}")
