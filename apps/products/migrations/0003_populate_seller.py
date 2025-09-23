# apps/products/migrations/0003_populate_seller.py

from django.db import migrations
from django.contrib.auth.hashers import make_password


def set_default_seller(apps, schema_editor):
    User = apps.get_model("users", "User")
    Product = apps.get_model("products", "Product")

    # Create or fetch a minimal "system" user.
    # Only use fields that *already exist* in User at this migration point.
    system_user, created = User.objects.get_or_create(
        username="system",
        defaults={
            "email": "system@gada.dev",
            # Hash password directly — never store raw in migrations.
            "password": make_password("supersecureplaceholder123"),
        },
    )

    # Assign system user to all products without a seller
    Product.objects.filter(seller__isnull=True).update(seller=system_user)


def reverse_func(apps, schema_editor):
    User = apps.get_model("users", "User")
    Product = apps.get_model("products", "Product")

    try:
        system_user = User.objects.get(username="system")
        Product.objects.filter(seller=system_user).update(seller=None)
    except User.DoesNotExist:
        pass


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0002_alter_product_category_remove_product_created_at_and_more"),
        ("users", "0002_contact"),  # adjust if your users app has a different latest migration
    ]

    operations = [
        migrations.RunPython(set_default_seller, reverse_func),
    ]
