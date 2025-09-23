# apps/users/migrations/0003_set_system_role.py
from django.db import migrations

def set_system_role(apps, schema_editor):
    User = apps.get_model("users", "User")
    try:
        system_user = User.objects.get(username="system")
    except User.DoesNotExist:
        return

    # only set role if historical model includes that field
    if hasattr(system_user, "role"):
        system_user.role = "seller"
        system_user.save()

class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_contact"),
    ]

    operations = [
        migrations.RunPython(set_system_role, migrations.RunPython.noop),
    ]
