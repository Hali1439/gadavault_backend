# apps/designers/models.py
import uuid
from django.db import models
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class DesignerProfile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='designer_profile')
    display_name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    portfolio = models.JSONField(default=list, blank=True)  # items: [{title, image_url, product_slug?}]
    skills = models.JSONField(default=list, blank=True)
    tags = models.JSONField(default=list, blank=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.display_name} ({self.user})"
