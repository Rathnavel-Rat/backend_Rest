from rest_framework import serializers
from .models import  FormsModel
class FormSaveSerializer(serializers.ModelSerializer):

    class Meta:
        model=FormsModel
        fields=["admin","binaryData","access_id"]


