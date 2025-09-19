# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system deps (Postgres client, etc.)
RUN apt-get update && apt-get install -y \
    libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

# Install pipenv / poetry if needed
RUN pip install --upgrade pip

# Copy requirements first (layer caching)
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy project code
COPY . .

# Set environment
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=gada_vault.settings

# Run Django (default CMD)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "gada_vault.wsgi:application"]
