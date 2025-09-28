from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, Category, Artisan
from .serializers import ProductSerializer, ArtisanSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsSellerOrReadOnly(BasePermission):
    """
    Only the seller (owner) of a product or staff can modify it; others can read.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.seller_id == getattr(request.user, 'id', None) or request.user.is_staff

class ArtisanViewSet(viewsets.ModelViewSet):
    queryset = Artisan.objects.all().order_by('-created_at')
    serializer_class = ArtisanSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('artisan','category','seller').filter(is_deleted=False).order_by('-created_at')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsSellerOrReadOnly]
    lookup_field = 'slug'

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated])
    def publish(self, request, slug=None):
        product = self.get_object()
        if product.seller_id != request.user.id:
            return Response({"detail":"Only the seller may publish."}, status=status.HTTP_403_FORBIDDEN)

        ipfs_hash = pin_product_to_ipfs(product)
        product.provenance = {
            "ipfs_hash": ipfs_hash,
            "published_at": product.updated_at.isoformat()
        }
        product.published = True
        product.save(update_fields=['provenance','published'])
        serializer = self.get_serializer(product)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        """
        Override delete to perform a soft-delete by setting is_deleted=True.
        Only the seller or staff can delete.
        """
        product = self.get_object()
        if product.seller_id != request.user.id and not request.user.is_staff:
            return Response(status=status.HTTP_403_FORBIDDEN)
        product.is_deleted = True
        product.save(update_fields=['is_deleted'])
        return Response(status=status.HTTP_204_NO_CONTENT)