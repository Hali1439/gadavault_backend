web: gunicorn gada_vault.wsgi:application --bind 0.0.0.0:$PORT --workers=4
worker: celery -A gada_vault worker --loglevel=info
beat: celery -A gada_vault beat --loglevel=info
