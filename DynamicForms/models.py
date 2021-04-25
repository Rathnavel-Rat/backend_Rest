import uuid
from django.db import models
from authrest.models import User

import os

import random as r


def generate_uuid():
    random_string = ''
    random_str_seq = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    uuid_format = [8, 4, 4, 4, 12]
    for n in uuid_format:
        for i in range(0, n):
            random_string += str(random_str_seq[r.randint(0, len(random_str_seq) - 1)])
        if n != 12:
            random_string += '-'
    return random_string


def get_upload_path(instance, filename):
    return os.path.join("media/%s" % instance.Form.pk, instance.MailName, filename)


class FormsModel(models.Model):
    form_id = models.CharField(primary_key=True, max_length=255, unique=True, auto_created=True, default=uuid.uuid1,
                               editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    collaborators = models.ManyToManyField(User, through="FormResponses", related_name="collabs")
    binaryData = models.BinaryField(blank=True)
    access_id = models.CharField(default =uuid.uuid4,auto_created=True,unique=True, max_length=255)
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


class FormImageUpload(models.Model):
    File = models.FileField(upload_to="Images")
