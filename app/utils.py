from django.core.mail import send_mail
from django.conf import settings

def send_email_to_clint(email):
    subject="DJANGO_EMAIL"
    message = "Thank you for your feedback"
    from_email = settings.EMAIL_HOST_USER
    gmail = [email]

    send_mail(subject, message, from_email, gmail)