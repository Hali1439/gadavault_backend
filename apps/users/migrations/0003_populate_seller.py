from django.db import migrations

def set_default_seller(apps, schema_editor):
    User = apps.get_model("users", "User")
    Product = apps.get_model("products", "Product")

    # Only username exists in historical model
    system_user, created = User.objects.get_or_create(username="system")
    
    # Assign system_user to existing products
    Product.objects.filter(seller__isnull=True).update(seller=system_user)

class Migration(migrations.Migration):

    dependencies = [
        ("products", "0002_alter_product_category_remove_product_created_at_and_more"),
        ("users", "0002_contact"),  # must point to last users migration that exists
    ]

    operations = [
        migrations.RunPython(set_default_seller),
    ]
