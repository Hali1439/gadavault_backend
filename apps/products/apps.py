# apps/products/apps.py
from django.apps import AppConfig


class ProductsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.products"
    label = "products"  # short label used for migrations etc.
    verbose_name = "Products"
