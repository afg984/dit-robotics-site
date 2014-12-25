import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.core.urlresolvers import reverse
# Create your models here.

MAX_FILENAME_LENGTH = 80

def get_store_path(instance, filename):
    return os.path.join('drive', instance.user.username, filename)

class DriveFile(models.Model):
    filename = models.CharField(max_length=MAX_FILENAME_LENGTH)
    user = models.ForeignKey(User)
    file = models.FileField(upload_to=get_store_path, max_length=MAX_FILENAME_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def basename(self):
        return os.path.basename(self.file.name)

    def as_link(self):
        return format_html(
            '<a href="{url}">{filename}</a>',
            url=reverse('drive-get', args=[self.user.username, self.id, self.filename]),
            filename=self.filename,
        )
