from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, SignupView, ContactCreateView

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")  # ✅ /api/users/

urlpatterns = [
    path("", include(router.urls)),
    path("signup/", SignupView.as_view(), name="signup"),       # /api/users/signup/
    path("contact/", ContactCreateView.as_view(), name="contact"),  # /api/users/contact/
]
