from django.db import models

# Create your models here.

class DriveFile(models.Model):
    filename = models.CharField(max_length=64)
    file = models.FileField()
