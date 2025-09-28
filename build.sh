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

# Platform-specific dependency installation
case $PLATFORM in
    "railway")
        echo "🚄 Installing Railway-specific dependencies..."
        # Add any Railway-specific packages if needed
        ;;
    "render")
        echo "🎨 Installing Render-specific dependencies..."
        # Add any Render-specific packages if needed
        ;;
    "local")
        echo "💻 Installing local development dependencies..."
        # pip install -r requirements-dev.txt  # Uncomment if you have dev requirements
        ;;
esac

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput --clear

# Run migrations for production platforms
if [ "$PLATFORM" != "local" ]; then
    echo "🗃️ Running database migrations..."
    python manage.py migrate --noinput
    
    # Platform-specific data seeding
    case $PLATFORM in
        "railway")
            echo "🚄 Running Railway-specific data setup..."
            # python manage.py seed_products  # Uncomment if you have seed commands
            ;;
        "render")
            echo "🎨 Running Render-specific data setup..."
            # python manage.py seed_products  # Uncomment if you have seed commands
            ;;
    esac
fi

# Create superuser for local development (optional)
if [ "$PLATFORM" = "local" ] && [ "$CREATE_SUPERUSER" = "true" ]; then
    echo "👤 Creating superuser..."
    python manage.py createsuperuser --noinput || true
fi

echo "✅ Build completed successfully for $PLATFORM"