# apps/products/urls.py
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, ArtisanViewSet

router = DefaultRouter()
router.register(r'artisans', ArtisanViewSet, basename='artisan')
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = router.urls
