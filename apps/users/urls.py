# apps/users/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserViewSet, SignupView, ContactCreateView

router = DefaultRouter()
router.register(r"", UserViewSet, basename="user")

urlpatterns = [
    path("auth/signup/", SignupView.as_view(), name="signup"),
    path("signup/", SignupView.as_view(), name="signup_alias"),  # Alias for incorrect client requests
    path("contact/", ContactCreateView.as_view(), name="contact"),

    # JWT
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # router stuff LAST
    path("", include(router.urls)),
]
