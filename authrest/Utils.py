from django.core.mail import EmailMessage
from rest_framework_simplejwt.tokens import RefreshToken


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(subject=data['email_subject'], body=data['email_body'], to=[data['to_email']])
        email.send()

    @staticmethod
    def RefreshToken(user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": refresh,
            "access": refresh.access_token,
        }
