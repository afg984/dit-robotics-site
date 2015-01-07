import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.core.urlresolvers import reverse
# Create your models here.

MAX_FILENAME_LENGTH = 80

def get_store_path(instance, filename):
    return os.path.join('drive', instance.user.username, filename)


class DriveDirectory(models.Model):
    parent = models.ForeignKey(
        'self',
        null=True,
        related_name='subdirectories')
    name = models.CharField(max_length=MAX_FILENAME_LENGTH)
    user = models.ForeignKey(User, related_name='+')
    shared = models.BooleanField(default=False)
    public = models.BooleanField(default=False)
    class Meta:
        unique_together = ('parent', 'name', 'user')


class DriveFile(models.Model):
    filename = models.CharField(max_length=MAX_FILENAME_LENGTH)
    user = models.ForeignKey(User)
    file = models.FileField(upload_to=get_store_path, max_length=MAX_FILENAME_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(DriveDirectory, null=True)

    @property
    def basename(self):
        return os.path.basename(self.file.name)

    @property
    def path(self):
        result = list()
        current = self
        while current.parent is not None:
            current = current.parent
            result.append(current)
        return result[::-1]

    def as_link(self):
        return format_html(
            '<a href="{url}">{filename}</a>',
            url=reverse('drive-get', args=[self.id, self.filename]),
            filename=self.filename,
        )

    @property
    def shared(self):
        if self.parent is not None and self.parent.shared:
            return True
        return False
