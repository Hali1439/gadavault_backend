# apps/users/models.py
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
    bio = models.TextField(null=True, blank=True)

    def full_name(self):
        """Return full name combining first_name and last_name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        elif self.last_name:
            return self.last_name
        return self.username

    def is_buyer(self):
        return self.role == "buyer"

    def is_seller(self):
        return self.role == "seller"

    def is_designer(self):
        return self.role == "designer"

    def is_artist(self):
        return self.role == "artist"

    def __str__(self):
        return f"{self.full_name()} ({self.role})"


class Contact(models.Model):
    first_name = models.CharField(max_length=150, blank=True, default="")
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def full_name(self):
        """Return contact's full name."""
        if self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.first_name

    def __str__(self):
        return f"Contact from {self.full_name()} - {self.subject}"
