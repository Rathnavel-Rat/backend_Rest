from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from .models import User
from django.contrib.auth.hashers import check_password


class UserBackend(ModelBackend):
    @staticmethod
    def authenticate(self, **kwargs):
        email = kwargs['email']
        password = kwargs['password']
        try:
            customer = User.objects.get(email=email)
            if check_password(encoded=customer.password, password=password):
                return customer
        except User.DoesNotExist:
            pass
