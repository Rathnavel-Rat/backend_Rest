import base64

from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist
from rest_framework import serializers

from .models import FormsModel


class FormSaveSerializer(serializers.ModelSerializer):
    form_id = serializers.CharField()
    binaryData = serializers.CharField()

    class Meta:
        model = FormsModel
        fields = ["binaryData", "form_id"]

    def validate(self, attrs):

        try:
            form = FormsModel.objects.get(form_id=attrs.get('form_id'))
            form.binaryData = base64.b64decode(attrs.get("binaryData"))
            form.save()
        except Exception as e:
            raise FieldDoesNotExist("Form Doesnot Exists")
        return attrs


class GetStoredFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormsModel
        fields = ["form_id", "name", "date"]


class NewFormSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormsModel
        fields = ["name", "owner", "form_id", "date"]

    def validate(self, attrs):
        return attrs


class UpdateFormName(serializers.ModelSerializer):
    form_id = serializers.CharField()
    name = serializers.CharField()

    class Meta:
        model = FormsModel
        fields = ["name", "form_id"]

    def validate(self, attrs):
        form_id = attrs.get('form_id')
        try:
            form = FormsModel.objects.get(form_id=form_id)
            form.name = attrs.get('name')
            form.save()
        except Exception as e:
            raise ObjectDoesNotExist("No mathcing form found")
        return attrs


class DeleteSerializer(serializers.ModelSerializer):
    form_id = serializers.CharField()
    class Meta:
        model = FormsModel
        fields = ["form_id"]

    def validate(self, attrs):
        form_id = attrs.get('form_id')
        try:
            form = FormsModel.objects.get(form_id=form_id)
            form.delete()
        except Exception as e:
            raise ObjectDoesNotExist("No mathcing form found")
        return attrs
