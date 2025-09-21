import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # marketplace roles
    ROLE_CHOICES = [
        ("buyer", "Buyer"),
        ("seller", "Seller"),
        ("designer", "Designer"),
        ("artist", "Artist"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="buyer")

    # shared profile info
    avatar = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=128, blank=True, null=True)
    bio = models.TextField(blank=True)

    def is_buyer(self):
        return self.role == "buyer"

    def is_seller(self):
        return self.role == "seller"

    def is_designer(self):
        return self.role == "designer"

    def is_artist(self):
        return self.role == "artist"

    def __str__(self):
        return f"{self.username} ({self.role})"


class Contact(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="contacts"
    )
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.subject}"
