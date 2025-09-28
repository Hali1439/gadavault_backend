#!/bin/bash

# build.sh - Multi-platform build script for Django deployment
set -e  # Exit on any error

echo "🔨 Starting Django project build..."

# Platform detection
if [ ! -z "$RAILWAY_ENVIRONMENT" ]; then
    PLATFORM="railway"
    echo "🚄 Building for Railway platform"
elif [ ! -z "$RENDER" ]; then
    PLATFORM="render" 
    echo "🎨 Building for Render platform"
else
    PLATFORM="local"
    echo "💻 Building for local development"
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run migrations if not in local development
if [ "$PLATFORM" != "local" ]; then
    echo "🗃️ Running database migrations..."
    python manage.py migrate --noinput
fi

# Platform-specific build steps
case $PLATFORM in
    "railway")
        echo "🚄 Applying Railway-specific configurations..."
        # Railway-specific setup if needed
        ;;
    "render")
        echo "🎨 Applying Render-specific configurations..."
        # Render-specific setup if needed  
        ;;
    "local")
        echo "💻 Local build complete"
        ;;
esac

echo "✅ Build completed successfully for $PLATFORM"