from rest_framework import serializers
from .models import DesignerProfile

class DesignerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DesignerProfile
        fields = 'all'
        read_only_fields = ['id', 'user', 'created_at']