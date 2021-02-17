from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from DynamicForms.serializers import FormSaveSerializer
from authrest.CustomAuth import AuthToken
from authrest.models import User


class SaveForm(GenericAPIView):
    serializer_class = FormSaveSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (AuthToken,)

    def get(self, request):
        user = User.objects.get(email=request.user)
        data = {"binaryData": request.data["binaryData"], "access_id": "Sadsad", "admin": user}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True}, status=status.HTTP_200_OK)
