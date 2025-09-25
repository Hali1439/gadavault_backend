FROM python:3.11-slim

# Prevents Python from writing .pyc and buffers stdout/stderr
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set working directory
WORKDIR /app

# Install system dependencies (Postgres client libs etc.)
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev curl && \
    rm -rf /var/lib/apt/lists/*

# Copy and install Python requirements
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files (safe to run at build time)
RUN python manage.py collectstatic --noinput || true

# Expose port for Gunicorn
EXPOSE 8080

# Default command (overridden by Railway if needed)
CMD ["gunicorn", "gada_vault.wsgi:application", "--bind", "0.0.0.0:8080"]
