import os

from rest_framework import status, permissions, generics
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from DynamicForms.serializers import FormSaveSerializer, GetStoredFormSerializer, NewFormSerializer, UpdateFormName, \
    DeleteSerializer, SaveResponse, GetResponsesSerializer, FileSaveSerializer, MakeFormVisibleSerializer, \
    AccessFormSerializer
from authrest.CustomAuth import AuthToken
from .models import FormsModel, FormResponses, FormFileResponses, FormImageUpload
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
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)
    serializer_class = UpdateFormName

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(status=status.HTTP_200_OK)


class BinaryFormData(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)

    def get(self, request):
        Form = FormsModel.objects.get(form_id=request.GET.get('form_id'))
        if Form.binaryData is None:
            return Response({"success": True, "data": "", "form_id": request.GET.get('form_id'), "name": Form.name},
                            status=status.HTTP_200_OK)
        print(base64.b64encode(Form.binaryData), "l")
        data = {"success": True, "data": base64.b64encode(Form.binaryData), "form_id": request.GET.get('form_id'),
                "name": Form.name}
        return Response(data, status=status.HTTP_200_OK)


class AccessForm(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)
    serializer_class = AccessFormSerializer

    def get(self, request):
        data = {"access_id": request.GET.get('access_id')}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        Form = FormsModel.objects.get(access_id=request.GET.get('access_id'))
        if Form.isPublish:
            return Response({"success": True, "message": "Success", "data": base64.b64encode(Form.binaryData)},
                            status=status.HTTP_200_OK)
        return Response({"success": False, "message": "This form don't support any responses"},
                        status=status.HTTP_200_OK)


class DeleteForm(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)
    serializer_class = DeleteSerializer

    def delete(self, request):
        data = {"form_id": str(request.GET.get("form_id")), "owner": str(request.user.pk)}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response({"success": True}, status=status.HTTP_200_OK)


class SaveResponses(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)
    serializer_class = SaveResponse

    def post(self, request):
        try:
            FormsModel.objects.get(access_id=request.data["access_id"])
        except FormsModel.DoesNotExist:
            return Response({"success": False}, status=status.HTTP_406_NOT_ACCEPTABLE)
        data = {"Form": str(request.data["access_id"]), "Responded_user": str(request.user.pk),
                "MailName": str(request.user.email + ",(" + request.user.username + ")")}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        _FormModel = FormsModel.objects.get(access_id=serializer.data["Form"])
        FormResponses(Form=_FormModel, Responded_user=request.user, is_done=True, results="",
                      Responses=request.data["Responses"], MailName=serializer.data["MailName"]).save()
        return Response({"success": True}, status=status.HTTP_200_OK)


class GetResponses(generics.ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)
    serializer_class = GetResponsesSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        Form = FormsModel.objects.get(form_id=request.data["Form"])
        data = {"binaryData": base64.b64encode(Form.binaryData), "data": serializer.data}
        return Response({"success": True, "message": "Success", "data": data},
                        status=status.HTTP_200_OK)


class FileSave(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)
    serializer_class = FileSaveSerializer

    def post(self, request):
        data = {"Form": str(request.data["access_id"]),
                "MailName": str(request.user.email + ",(" + request.user.username + ")")}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        Form = FormsModel.objects.get(form_id=serializer.data["Form"])
        filepath = {}
        for i in request.FILES:
            File = FormFileResponses()
            File.Form = Form
            File.MailName = serializer.data["MailName"]
            File.File = request.FILES[i]
            File.save()
            filepath[i] = File.File.url
        return Response({"success": True, "filepath": filepath}, status=status.HTTP_200_OK)


class MakeFormVisible(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)
    serializer_class = MakeFormVisibleSerializer

    def post(self, request):
        data = {"form_id": str(request.data["form_id"]), "owner": str(request.user.pk),
                "isPublish": request.data["isPublish"]}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        return Response({"success": True}, status=status.HTTP_200_OK)


class ImageFileUpload(GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)

    def post(self, request):
        File = FormImageUpload()
        File.File = request.FILES["file"]
        File.save()
        return Response({"success": True, "link": os.environ.get("BACKEND_DOMAIN") + File.File.url},
                        status=status.HTTP_200_OK)
