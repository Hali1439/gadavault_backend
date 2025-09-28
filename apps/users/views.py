# apps/users/views.py
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import generics, status, viewsets, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import action
from .serializers import UserSerializer, ContactSerializer
from .models import Contact

User = get_user_model()

# --- USER MANAGEMENT ---
class UserViewSet(viewsets.GenericViewSet, 
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.ListModelMixin):
    """
    User viewset that doesn't allow creation (use SignupView instead)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'list':
            # Only admin can list all users
            return [IsAdminUser()]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            # Users can view/update their own profile
            return [IsAuthenticated()]
        return [IsAuthenticated()]  # Default

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        # Users can only see their own profile
        return User.objects.filter(id=user.id)

    def retrieve(self, request, *args, **kwargs):
        # Users can only retrieve their own profile
        if int(kwargs['pk']) != request.user.id and not request.user.is_staff:
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)
        return super().retrieve(request, *args, **kwargs)

    def perform_update(self, serializer):
        """
        Ensure password is hashed on update if changed.
        """
        if "password" in serializer.validated_data:
            serializer.validated_data["password"] = make_password(
                serializer.validated_data["password"]
            )
        return super().perform_update(serializer)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """Get current user profile"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)


# --- CONTACT FORM ENDPOINT ---
class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def perform_create(self, serializer):
        contact = serializer.save()
        subject = f"New contact form from {contact.full_name()}"
        body = (
            f"New contact received\n\n"
            f"Name: {contact.full_name()}\n"
            f"Email: {contact.email}\n"
            f"Message:\n{contact.message}\n\n"
            f"Received at: {contact.created_at}\n"
        )
        recipient = getattr(settings, "CONTACT_RECEIVER_EMAIL", settings.EMAIL_HOST_USER)

        try:
            # Try Celery for async
            from .tasks import send_contact_email
            send_contact_email.delay(
                contact.id,
                contact.full_name(),
                contact.email,
                contact.message,
                str(contact.created_at),
            )
        except Exception as e:
            print("⚠️ Celery task failed, fallback to sync email:", e)
            try:
                send_mail(
                    subject,
                    body,
                    settings.DEFAULT_FROM_EMAIL,
                    [recipient],
                    fail_silently=False,
                )
            except Exception as inner_e:
                print("⚠️ Failed to send contact email:", inner_e)


# --- SIGNUP ENDPOINT ---
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    authentication_classes = []

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        
        # Handle password hashing
        if "password" in data:
            data["password"] = make_password(data["password"])
        
        # Ensure username exists (use email if not provided)
        if "username" not in data and "email" in data:
            data["username"] = data["email"]
            
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Generate JWT tokens after signup
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "user": serializer.data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            },
            status=status.HTTP_201_CREATED,
        )