from django.db import migrations

def set_system_role(apps, schema_editor):
    User = apps.get_model("users", "User")
    try:
        system_user = User.objects.get(username="system")
        system_user.role = "seller"
        system_user.save()
    except User.DoesNotExist:
        pass

def reverse_func(apps, schema_editor):
    User = apps.get_model("users", "User")
    try:
        system_user = User.objects.get(username="system")
        system_user.role = None
        system_user.save()
    except User.DoesNotExist:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ("users", "0003_populate_seller"),  # <- points to the previous users migration
    ]

    operations = [
        migrations.RunPython(set_system_role, reverse_func),
    ]
