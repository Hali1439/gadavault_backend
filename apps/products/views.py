from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    """
    Full CRUD API for Products
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
