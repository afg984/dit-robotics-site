import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
# Create your models here.

def get_store_path(instance, filename):
    return os.path.join('drive', instance.user.username, filename)

class DriveFile(models.Model):
    filename = models.CharField(max_length=64)
    user = models.ForeignKey(User)
    file = models.FileField(upload_to=get_store_path)

    def as_link(self):
        return format_html(
            '<a href="{url}">{filename}</a>',
            url=self.file.url,
            filename=os.path.basename(self.file.name),
        )
