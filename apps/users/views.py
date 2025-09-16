from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from rest_framework import generics, status, viewsets
from rest_framework.response import Response

from .serializers import UserSerializer, ContactSerializer
from .models import Contact

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# --- CONTACT FORM ENDPOINT ---
class ContactCreateView(generics.CreateAPIView):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def perform_create(self, serializer):
        contact = serializer.save()

        # Prepare email
        subject = f"New contact form from {contact.name}"
        body = (
            f"New contact received\n\n"
            f"Name: {contact.name}\n"
            f"Email: {contact.email}\n"
            f"Message:\n{contact.message}\n\n"
            f"Received at: {contact.created_at}\n"
        )
        recipient = getattr(settings, "CONTACT_RECEIVER_EMAIL", settings.EMAIL_HOST_USER)

        # Send email synchronously (simple version)
        try:
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [recipient],
                fail_silently=False,
            )
        except Exception as e:
            # Contact saved even if email fails
            print("⚠️ Failed to send contact email:", e)


# --- SIGNUP ENDPOINT ---
class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        # Hash password before saving
        if "password" in data:
            data["password"] = make_password(data["password"])

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
