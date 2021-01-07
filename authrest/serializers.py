from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .backends import UserBackend


class RegistrationSerailaizers(serializers.ModelSerializer):
    password = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username']

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get("username", '')

        if not username.isalnum():
            raise serializers.ValidationError('the username should  only alphanumeric ')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EamilVerifiactionSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=555)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True, max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    id = serializers.CharField(read_only=True)
    tokens = serializers.CharField(max_length=555, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'id', 'username', 'tokens']

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs['password']
        user = UserBackend.authenticate(self, email=email, password=password)
        if not user:
            raise AuthenticationFailed("not an user")
        if not user.is_verified:
            raise AuthenticationFailed('Email is not verified')
        return {
            "username": user.username,
            "email": user.email,
            'id': user.id,
            "tokens": user.tokens()
        }


class ChangePasswordRequestSerializers(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        email = attrs['email']
        if not User.objects.filter(email=email).exists():
            raise NotFound("check ur email id")
        user = User.objects.get(email=email)
        return attrs


class PasswordTokenCheckSerailizer(serializers.Serializer):
    token = serializers.CharField(max_length=555)
    uid = serializers.CharField(max_length=255)


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, write_only=True)
    token = serializers.CharField(max_length=555, write_only=True)
    uid = serializers.CharField(max_length=255, write_only=True)

    class Meta:
        fields = ['password', 'token', 'uidb64']

    def validate(self, attrs):
            try:
                password = attrs.get('password')
                token = attrs.get('token')
                id= attrs.get('uid')
                user = User.objects.get(id=id)
                if not PasswordResetTokenGenerator().check_token(user, token):
                    raise AuthenticationFailed('The reset link is invalid', 401)

                user.set_password(password)
                user.save()
                return user
            except Exception as e:
                raise AuthenticationFailed('The reset is invalid', 401)



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    token = ""

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            self.fail('bad_token')
