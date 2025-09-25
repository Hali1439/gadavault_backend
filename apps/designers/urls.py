# apps/designers/urls.py
from rest_framework.routers import DefaultRouter
from .views import DesignerProfileViewSet

router = DefaultRouter()
# Use blank prefix to avoid duplicate 'designers' in URL
router.register(r'', DesignerProfileViewSet, basename='designer')

urlpatterns = router.urls