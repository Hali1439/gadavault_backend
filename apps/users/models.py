import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    ROLE_CHOICES = [
        ("buyer", "Buyer"),
        ("seller", "Seller"),
        ("designer", "Designer"),
        ("artist", "Artist"),
        ("admin", "Admin"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="buyer")

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

    def str(self):
        return f"{self.username} ({self.role})"

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def str(self):
        return f"Contact from {self.name} - {self.subject}"