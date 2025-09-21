# apps/designers/views.py
from rest_framework import viewsets, permissions
from .models import DesignerProfile
from .serializers import DesignerProfileSerializer

class DesignerProfileViewSet(viewsets.ModelViewSet):
    queryset = DesignerProfile.objects.select_related('user').all()
    serializer_class = DesignerProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
