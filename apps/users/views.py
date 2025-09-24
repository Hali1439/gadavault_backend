from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import UserSerializer, ContactSerializer
from .models import Contact

User = get_user_model()

# --- USER MANAGEMENT ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == "create":  # signup
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        # Admins can see all users; others can only see themselves
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)

    def perform_update(self, serializer):
        """
        Ensure password is hashed on update if changed.
        """
        if 'password' in serializer.validated_data:
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        return super().perform_update(serializer)

# --- CONTACT FORM ENDPOINT ---
class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        contact = serializer.save()
        subject = f"New contact form from {contact.name}"
        body = (
            f"New contact received\n\n"
            f"Name: {contact.name}\n"
            f"Email: {contact.email}\n"
            f"Message:\n{contact.message}\n\n"
            f"Received at: {contact.created_at}\n"
        )
        recipient = getattr(settings, "CONTACT_RECEIVER_EMAIL", settings.EMAIL_HOST_USER)

        try:
            # Use Celery task to send email asynchronously
            from .tasks import send_contact_email
            send_contact_email.delay(
                contact.id,
                contact.name,
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

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        if "password" in data:
            data["password"] = make_password(data["password"])
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
