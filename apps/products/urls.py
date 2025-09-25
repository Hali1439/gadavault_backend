# apps/products/urls.py
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ArtisanViewSet

router = DefaultRouter()
# Use blank prefix for products to avoid '/products/products/'
router.register(r'', ProductViewSet, basename='product')
router.register(r'artisans', ArtisanViewSet, basename='artisan')

urlpatterns = router.urls