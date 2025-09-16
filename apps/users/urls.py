from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ContactCreateView, SignupView

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("", include(router.urls)),
    path("contact/", ContactCreateView.as_view(), name="contact"),
    path("signup/", SignupView.as_view(), name="signup"),
]
