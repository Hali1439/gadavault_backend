from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        # keep it open for now, expose all fields (even email/password hashes)
        # ⚠️ in production you’d want to hide sensitive stuff
        fields = "__all__"
