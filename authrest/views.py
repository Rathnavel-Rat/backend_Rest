from datetime import datetime

import jwt
from django.utils.encoding import smart_bytes, smart_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status, permissions
from rest_framework.generics import *
from rest_framework.permissions import *
from rest_framework.response import Response
from django.http import HttpResponsePermanentRedirect
from backend_Rest import settings
from .Utils import Util

from .serializers import *
from django.shortcuts import reverse
from django.contrib.sites.shortcuts import get_current_site
from rest_framework_simplejwt.tokens import RefreshToken
import os
import datetime


# Create your views here.
def email_send_verification(complete_url, user):
    email_body = "hai " + user.username + " Use the link below to verify \n " + complete_url
    data = {"email_body": email_body, "to_email": user.email, "email_subject": "email verification"}
    Util.send_email(data)


def getUserSendVerification(email, domain_name):
    user = User.objects.get(email=email)
    token = str(RefreshToken.for_user(user).access_token)
    urls = reverse("emailVerification")
    complete_url = "http://" + str(domain_name) + urls + "?token=" + str(token)
    email_send_verification(complete_url, user)


class Register(GenericAPIView):
    serializer_class = RegistrationSerailaizers

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()
        data = serializers.data
        domain_name = get_current_site(request).domain
        getUserSendVerification(data.get("email"), domain_name)
        url = os.environ.get("FRONTEND_URL") + "/Login"
        return HttpResponsePermanentRedirect(url)


class ResendEmailVerfication(views.APIView):
    serializers_class = ResendEmailVerficationSerializer

    def post(self, request):
        serializer = self.serializers_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        domain_name = get_current_site(request).domain
        getUserSendVerification(request.data.get('email'), domain_name)
        url = os.environ.get("FRONTEND_URL") + "/Login"
        return HttpResponsePermanentRedirect(url)


class VerfiyUsingEmail(views.APIView):
    serializer_class = EamilVerifiactionSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])
            if not user.is_verified:
                user.is_verified = True
                user.is_active = True
                user.save()
                url = os.environ.get("FRONTEND_URL") + "/Login"
                return HttpResponsePermanentRedirect(url)
            return Response({"message": "successfully verified"}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as e:
            return Response({'error': 'Activations link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as e:
            return Response({'error': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class LoginApiView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        data = serializers.data
        response = Response()
        response.set_cookie(key="accesstoken", value=data.get("access_token"), max_age=6 * 24 * 60 * 60,httponly=True)
        response.set_cookie(key="refreshtoken", value=data.get("refresh_token"), max_age=6 * 24 * 60 * 60,httponly=True)
        data.pop("access_token")#added
        data.pop("refresh_token")#added
        final_data = {"success": True, "data": data}
        response.data = final_data
        response.status = status.HTTP_200_OK
        return response


class RequestChangingPassword(GenericAPIView):
    serializer_class = ChangePasswordRequestSerializers

    def post(self, request):
        serializers = self.serializer_class(data=request.data)
        serializers.is_valid(raise_exception=True)
        user = User.objects.get(email=request.data['email'])
        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)
        current_site = get_current_site(request).domain
        relativelink = reverse("RECV", kwargs={'uidb64': uidb64, "token": token})
        complete_url = "http://" + current_site + relativelink
        email_send_verification(complete_url, user)
        return Response({"success": True})


class RequestPasswordChangeEmailVerifiacation(GenericAPIView):
    serializer_class = PasswordTokenCheckSerailizer
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)
            url = os.environ.get("FRONTEND_URL") + "/passwordReset" + '?token_valid=True&message=CredentialsValid&uidb64=' + uidb64 + '&token=' + token

            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                url = os.environ.get(
                    "FRONTEND_URL") + "/passwordReset" + '?token_valid=False&message=CredentialsInValid'
                return HttpResponsePermanentRedirect(url)
                # Response({"error": "token is not valid ,please request another "})

            return HttpResponsePermanentRedirect(url)
            # Response({"success": True, "message": "valid ", "uid": id, "token": token})
        except DjangoUnicodeDecodeError as e:
            if not PasswordResetTokenGenerator().check_token(user=user, token=token):
                url = os.environ.get(
                    "FRONTEND_URL") + "passwordReset/" + '?token_valid=False&message=CredentialsInValid'
                return HttpResponsePermanentRedirect(url)


class SetNewPasswordApi(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    permission_classes = (permissions.AllowAny,)

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success': True, "message": "Password reset successful"})


class LogoutAPIView(GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
