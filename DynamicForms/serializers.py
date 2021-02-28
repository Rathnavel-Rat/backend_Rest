from rest_framework import serializers

from authrest.models import User
from .models import FormsModel


class FormSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormsModel
        fields = ["admin", "binaryData", "access_id"]

    def validate(self, attrs):
        pass


class GetStoredFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormsModel
        fields = ["access_id","name","date"]
