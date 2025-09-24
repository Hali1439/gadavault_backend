from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="GadaVault API",
        default_version="v1",
        description="GadaVault — products, designers, escrow, and payments API.",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),  # Consider stricter permissions in prod
)

urlpatterns = [
    path("admin/", admin.site.urls),

    # App endpoints (no version prefix)
    path("api/users/", include("apps.users.urls")),
    path("api/products/", include("apps.products.urls")),
    path("api/designers/", include("apps.designers.urls")),

    # Versioned endpoints (using /api/v1/ as alias)
    path("api/v1/users/", include("apps.users.urls")),
    path("api/v1/products/", include("apps.products.urls")),
    path("api/v1/designers/", include("apps.designers.urls")),

    # Swagger / Redoc documentation
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
