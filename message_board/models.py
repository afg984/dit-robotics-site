from django.db import models

# Create your models here.
class Message(models.Model):
    nickname = models.CharField(max_length=31)
    message = models.TextField(max_length=255)
