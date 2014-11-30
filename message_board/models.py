from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(User, null=True)
    nickname = models.CharField(max_length=31)
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
