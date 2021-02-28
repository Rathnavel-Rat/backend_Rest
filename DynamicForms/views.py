from psycopg2._json import Json
from rest_framework import status, permissions, generics
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from DynamicForms.serializers import FormSaveSerializer, GetStoredFormSerializer
from authrest.CustomAuth import AuthToken
from authrest.models import User
from rest_framework.parsers import FormParser, MultiPartParser
from .models import FormsModel
import base64
from .Fields_pb2 import ListFields


class SaveForm(GenericAPIView):
    serializer_class = FormSaveSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)

    def post(self, request):
        user = User.objects.get(email=request.user)
        ser_data = {"admin": user, "binaryData": base64.b64decode(request.data["data"]), }
        form = FormsModel()
        form.admin = user
        form.binaryData = base64.b64decode(request.data["data"])
        form.save()
        # use in resonsing f = base64.b64encode(base64.b64decode(request.data["data"]))
        return Response({"success": True}, status=status.HTTP_200_OK)


class GetStoredForms(generics.ListAPIView):
    serializer_class = GetStoredFormSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)

    def get_queryset(self):
        print("sdsd")
        return FormsModel.objects.filter(admin=self.request.user)