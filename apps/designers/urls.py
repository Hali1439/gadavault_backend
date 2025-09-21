# apps/designers/urls.py
from rest_framework.routers import DefaultRouter
from .views import DesignerProfileViewSet

router = DefaultRouter()
router.register(r'designers', DesignerProfileViewSet, basename='designer')

urlpatterns = router.urls
