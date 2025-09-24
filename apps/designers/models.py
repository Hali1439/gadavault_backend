import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

class DesignerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="designer_profile"
    )
    display_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    portfolio = models.JSONField(default=list, blank=True)
    skills = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def str(self):
        return f"{self.display_name} ({self.user.username})"