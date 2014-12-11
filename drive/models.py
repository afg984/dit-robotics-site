from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class DriveFile(models.Model):
    filename = models.CharField(max_length=64)
    user = models.ForeignKey(User)
    file = models.FileField()
