# apps/users/tasks.py
from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task

@shared_task
def send_contact_email(contact_id, name, email, message, created_at):
    subject = f"New contact form from {name}"
    body = (
        f"New contact received\n\n"
        f"Name: {name}\n"
        f"Email: {email}\n"
        f"Message:\n{message}\n\n"
        f"Received at: {created_at}\n"
    )
    recipient = getattr(settings, "CONTACT_RECEIVER_EMAIL", settings.EMAIL_HOST_USER)

    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [recipient],
        fail_silently=False,
    )
    return f"Contact {contact_id} email sent!"
