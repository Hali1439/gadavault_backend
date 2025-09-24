from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Contact

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            "password", "is_superuser", "is_staff",
            "groups", "user_permissions"
        )

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "all"