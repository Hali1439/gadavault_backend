from rest_framework import serializers
from .models import DesignerProfile

class DesignerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignerProfile
        fields = "__all__"
        read_only_fields = ['id', 'user', 'created_at']