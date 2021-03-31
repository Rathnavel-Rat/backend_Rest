import uuid
from django.db import models
from authrest.models import User

import os


def get_upload_path(instance, filename):
    return os.path.join("media/%s" % instance.Form.pk, instance.MailName, filename)


def hex_uuid():
    return uuid.uuid4().hex


class FormsModel(models.Model):
    form_id = models.CharField(primary_key=True, max_length=255, unique=True, auto_created=True, default=uuid.uuid1,
                               editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, through="FormResponses", related_name="collabs")
    binaryData = models.BinaryField(blank=True)
    access_id = models.CharField(default=hex_uuid(), max_length=255)
    isPublish = models.BooleanField(default=False)
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now=True)


class FormResponses(models.Model):
    Form = models.ForeignKey(FormsModel, on_delete=models.CASCADE)
    Responded_user = models.ForeignKey(User, on_delete=models.CASCADE)
    MailName = models.CharField(max_length=256)
    Responses = models.JSONField(blank=True, null=True)
    is_done = models.BooleanField(default=False)
    results = models.CharField(default="waiting", max_length=255)


class FormFileResponses(models.Model):
    Form = models.ForeignKey(FormsModel, on_delete=models.CASCADE)
    MailName = models.CharField(max_length=256)
    File = models.FileField(upload_to=get_upload_path)
    date = models.DateTimeField(auto_now=True)
