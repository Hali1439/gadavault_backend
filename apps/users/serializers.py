from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Contact

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'avatar', 'country', 'bio', 'is_staff', 'is_active', 'date_joined')
        read_only_fields = ('id', 'is_staff', 'is_active', 'date_joined')
        
    def create(self, validated_data):
        # Ensure username exists
        if 'username' not in validated_data and 'email' in validated_data:
            validated_data['username'] = validated_data['email']
        return super().create(validated_data)

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"