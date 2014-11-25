from django.db import models

# Create your models here.
class Message(models.Model):
    nickname = models.CharField(max_length=31)
    message = models.CharField(max_length=127)
    created_at = models.DateTimeField(auto_now_add=True)
