from psycopg2._json import Json
from rest_framework import status, permissions, generics
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from DynamicForms.serializers import FormSaveSerializer, GetStoredFormSerializer, NewFormSerializer, UpdateFormName, \
    GetFormBinaryData
from authrest.CustomAuth import AuthToken

from .models import FormsModel
import base64



class SaveForm(GenericAPIView):
    serializer_class = FormSaveSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)

    def post(self, request):
        ser_data = {"binaryData": request.data["data"], "form_id": request.data["form_id"]}
        serializer = self.serializer_class(data=ser_data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response({"success": True}, status=status.HTTP_200_OK)


class GetStoredForms(generics.ListAPIView):
    serializer_class = GetStoredFormSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)

    def get_queryset(self):
        return FormsModel.objects.filter(owner=self.request.user)


class NewForm(GenericAPIView):
    serializer_class = NewFormSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)

    def post(self, request):
        data = dict(request.data)
        data["name"] = request.data.get("name")
        data["owner"] = request.user.pk
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        queryset = FormsModel.objects.filter(owner=request.user)
        ser = self.serializer_class(queryset, many=True)
        return Response({"success": True, "data": ser.data}, status=status.HTTP_201_CREATED)


class UpdateName(GenericAPIView):
    serializer_class = UpdateFormName

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)


class BinaryFormData(APIView):
    serializer_class = GetFormBinaryData

    def get(self, request):
        Form = FormsModel.objects.get(form_id=request.GET.get('form_id'))
        if Form.binaryData is None:
            return Response({"success": True, "data": "", "form_id": request.GET.get('form_id'),"name":Form.name},status=status.HTTP_200_OK)
        data = {"success": True, "data": base64.b64encode(Form.binaryData), "form_id": request.GET.get('form_id'),"name":Form.name}
        return Response(data, status=status.HTTP_200_OK)
