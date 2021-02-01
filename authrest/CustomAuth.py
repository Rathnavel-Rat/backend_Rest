import jwt
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from authrest.models import User
from backend_Rest import settings


class AuthToken(BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES['accesstoken']
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
        except jwt.ExpiredSignatureError as e:
            return AuthenticationFailed("Expired Token")
        except jwt.exceptions.DecodeError as e:
            return AuthenticationFailed("Invalid Token")

        return user, token

