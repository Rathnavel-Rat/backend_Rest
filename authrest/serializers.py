from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, smart_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
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

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError("the email id is already exits")

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class EamilVerifiactionSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=555)


class ResendEmailVerficationSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)

    def validate(self, attrs):
        email = attrs.get('email', '')
        if User.objects.filter(email=email).exits:
            raise serializers.ValidationError("the email id is already exits")
        return attrs


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    password = serializers.CharField(write_only=True, max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    id = serializers.CharField(read_only=True)
    access_token = serializers.CharField(max_length=555, read_only=True)
    refresh_token = serializers.CharField(max_length=555, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'id', 'username', 'access_token', "refresh_token"]

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
            'id': urlsafe_base64_encode(smart_bytes(user.id)),
            "access_token": user.tokens()["access"],
            "refresh_token": user.tokens()['refresh']
        }


class ChangePasswordRequestSerializers(serializers.Serializer):
    email = serializers.EmailField(write_only=True)

    def validate(self, attrs):
        email = attrs['email']
        if not User.objects.filter(email=email).exists():
            raise NotFound("email id is not registered")
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
        password = attrs.get('password')
        token = attrs.get('token')
        uidb64 = attrs.get('uid')
        id = smart_str(urlsafe_base64_decode(uidb64))

        try:
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()
            return user
        except Exception as e:
            raise AuthenticationFailed('The reset is invalid', 401)


class LogoutSerializer(serializers.Serializer):
   pass
