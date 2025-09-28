# -------------------------
# Base image
# -------------------------
FROM python:3.11-slim

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# -------------------------
# System dependencies
# -------------------------
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
 && rm -rf /var/lib/apt/lists/*

# -------------------------
# Virtual environment
# -------------------------
RUN python3 -m venv /venv
ENV PATH="/venv/bin:$PATH"

# -------------------------
# Install dependencies
# -------------------------
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# -------------------------
# Copy project files
# -------------------------
COPY . .

# -------------------------
# Collect static files
# -------------------------
RUN python manage.py collectstatic --noinput || true

# -------------------------
# Expose port for app
# -------------------------
EXPOSE 8000

# -------------------------
# Start Gunicorn server
# -------------------------
CMD ["gunicorn", "gada_vault.wsgi:application", "--bind", "0.0.0.0:$PORT"]