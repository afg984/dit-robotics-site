import os
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

def get_store_path(instance, filename):
    return os.path.join('drive', instance.user, filename)

class DriveFile(models.Model):
    filename = models.CharField(max_length=64)
    user = models.ForeignKey(User)
    file = models.FileField(upload_to=get_store_path)
