from rest_framework import serializers
from .models import Product, Category, Artisan

class ArtisanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artisan
        fields = ['id', 'name', 'bio', 'country', 'profile_image', 'metadata', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    artisan = ArtisanSerializer(read_only=True)
    artisan_id = serializers.UUIDField(write_only=True, required=False, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'artisan', 'artisan_id', 'category', 'name', 'slug',
            'description', 'price', 'stock', 'attributes', 'images',
            'provenance', 'story_markdown', 'origin_region',
            'royalty_percent', 'published', 'created_at'
        ]
        read_only_fields = ['id', 'seller', 'provenance', 'created_at']

    def create(self, validated_data):
        artisan_id = validated_data.pop('artisan_id', None)
        seller = self.context['request'].user
        if artisan_id:
            validated_data['artisan_id'] = artisan_id
        validated_data['seller'] = seller
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Prevent others from modifying provenance
        if 'provenance' in validated_data and instance.seller_id != self.context['request'].user.id:
            validated_data.pop('provenance', None)
        return super().update(instance, validated_data)