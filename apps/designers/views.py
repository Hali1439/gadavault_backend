from rest_framework import viewsets, permissions
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import DesignerProfile
from .serializers import DesignerProfileSerializer

class IsOwnerOrReadOnly(BasePermission):
    """
    Custom permission: only profile owner (or staff) can modify; others can only read.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.user_id == request.user.id or request.user.is_staff

class DesignerProfileViewSet(viewsets.ModelViewSet):
    queryset = DesignerProfile.objects.select_related('user').all()
    serializer_class = DesignerProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        # Set the creator as the user
        serializer.save(user=self.request.user)