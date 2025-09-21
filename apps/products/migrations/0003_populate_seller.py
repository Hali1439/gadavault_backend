from django.db import migrations

def set_default_seller(apps, schema_editor):
    User = apps.get_model("users", "User")
    Product = apps.get_model("products", "Product")

    # Create or fetch a minimal "system" user
    system_user, created = User.objects.get_or_create(
        username="system"
    )

    if created:
        # Only set fields guaranteed to exist at this historical point
        system_user.email = "system@gada.dev"
        # DO NOT touch 'role' here, it may not exist yet
        system_user.set_password("supersecureplaceholder123")
        system_user.save()

    # Assign system user to all products missing seller
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
        ("users", "0002_contact"),  # match your last users migration
    ]

    operations = [
        migrations.RunPython(set_default_seller, reverse_func),
    ]
