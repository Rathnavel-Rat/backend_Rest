import base64
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist
from rest_framework import serializers
from .models import FormsModel, FormResponses, FormFileResponses


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
        fields = ["form_id", "name", "date", "access_id", "isPublish"]


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
    owner = serializers.CharField()

    class Meta:
        model = FormsModel
        fields = ["form_id", "owner"]

    def validate(self, attrs):
        form_id = attrs.get('form_id')
        user_id = attrs.get('owner')
        try:
            form = FormsModel.objects.get(form_id=form_id, owner=user_id)
            form.delete()
        except FormsModel.DoesNotExist:
            raise serializers.ValidationError("No Such Form is Found")
        except Exception as e:
            raise ObjectDoesNotExist("No mathcing form found")
        return attrs


class SaveResponse(serializers.ModelSerializer):
    Form = serializers.CharField()
    Responded_user = serializers.CharField()
    MailName = serializers.CharField()

    class Meta:
        model = FormResponses
        fields = ("Form", "Responded_user", "MailName")

    def validate(self, attrs):
        try:
            f = FormsModel.objects.get(access_id=attrs.get("Form"))
            if FormResponses.objects.filter(Form=f.pk, Responded_user=attrs.get("Responded_user")).exists():
                if FormResponses.objects.get(Form=f.pk, Responded_user=attrs.get("Responded_user")).is_done:
                    raise serializers.ValidationError("Already Responded")

        except FormsModel.DoesNotExist:
            raise serializers.ValidationError("No Such Form is Found")
        except User.DoesNotExist:
            raise serializers.ValidationError("unauthorized user")
        return attrs


class ResponsesSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormResponses
        fields = ("Responses", "MailName")


class GetResponsesSerializer(serializers.Serializer):
    Form = serializers.CharField(write_only=True)
    List = ResponsesSerializer(many=True, read_only=True)
    FormName = serializers.CharField(read_only=True)

    def validate(self, attrs):
        try:
            _f = FormsModel.objects.get(form_id=attrs.get("Form"))
            form = FormResponses.objects.filter(Form=_f.pk)
            attrs["List"] = form
            attrs["FormName"] = _f.name
        except FormsModel.DoesNotExist:
            raise serializers.ValidationError("No Such Form  Found")
        except FormResponses.DoesNotExist:
            raise serializers.ValidationError("No Such Responses  Found")
        except Exception as e:
            raise serializers.ValidationError("Try again Later")
        return attrs


class FileSaveSerializer(serializers.ModelSerializer):
    Form = serializers.CharField()
    MailName = serializers.CharField()

    class Meta:
        model = FormFileResponses
        fields = ["Form", "MailName"]

    def validate(self, attrs):
        try:
            f = FormsModel.objects.get(access_id=attrs.get("Form"))
            if FormResponses.objects.filter(Form=f.pk, MailName=attrs.get("MailName")).exists():
                if FormResponses.objects.get(Form=f.pk, MailName=attrs.get("MailName")).is_done:
                    raise serializers.ValidationError("Already Responded")
            attrs["Form"] = f.form_id
        except FormsModel.DoesNotExist:
            raise serializers.ValidationError("No Such Form  Found")
        return attrs


class MakeFormVisibleSerializer(serializers.ModelSerializer):
    form_id = serializers.CharField()
    owner = serializers.CharField()
    isPublish = serializers.BooleanField()

    class Meta:
        model = FormsModel
        fields = ["form_id", "owner", "isPublish"]

    def validate(self, attrs):
        form_id = attrs.get('form_id')
        user_id = attrs.get('owner')
        try:
            form = FormsModel.objects.get(form_id=form_id, owner=user_id)
            form.isPublish = attrs.get("isPublish")
            form.save()
        except FormsModel.DoesNotExist:
            raise serializers.ValidationError("No Such Form is Found")
        except Exception as e:
            raise ObjectDoesNotExist("No mathcing form found")
        return attrs


class AccessFormSerializer(serializers.ModelSerializer):
    access_id = serializers.CharField()

    class Meta:
        model = FormsModel
        fields = ["access_id"]

    def validate(self, attrs):
        access_id = attrs.get("access_id")
        print(access_id)
        try:
            form = FormsModel.objects.get(access_id=access_id)
        except FormsModel.DoesNotExist:
            raise serializers.ValidationError("No Such Form is Found")
        except Exception as e:
            raise ObjectDoesNotExist("No mathcing form found")
        return attrs
