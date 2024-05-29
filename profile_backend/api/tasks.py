from django.core.mail import send_mail
from celery import shared_task

from profile_backend.settings import DEFAULT_FROM_EMAIL


@shared_task
def send_feedback_email_task(email_address, message):
    send_mail(
        subject='Код подтверждения',
        message=message,
        from_email=DEFAULT_FROM_EMAIL,
        recipient_list=[email_address],
        fail_silently=True,
        )
