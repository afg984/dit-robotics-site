import os
from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.core.urlresolvers import reverse
# Create your models here.

MAX_FILENAME_LENGTH = 100

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

    @property
    def abspath(self):
        result = []
        current = self
        while current is not None:
            result.append(current)
            current = current.parent
        result.append(DriveRootDirectory(self.user))
        return result[::-1]

    def __str__(self):
        return '{}/'.format(
            '/'.join(instance.name for instance in self.abspath)
        )

    @property
    def as_link(self):
        return format_html(
            '<a href="{url}">{name}</a>',
            name=self.name,
            url=self.reverse,
        )
        return 100

    @property
    def slashpath(self):
        return '/'.join(d.name for d in self.abspath) + '/'

    def reverse(self):
        return reverse('drive-listing',
            args=[self.slashpath]
        )


class DriveFile(models.Model):
    filename = models.CharField(max_length=MAX_FILENAME_LENGTH)
    user = models.ForeignKey(User)
    file = models.FileField(upload_to=get_store_path, max_length=MAX_FILENAME_LENGTH)
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey(DriveDirectory, null=True, related_name='files')

    @property
    def basename(self):
        return os.path.basename(self.file.name)

    @property
    def abspath(self):
        self.parent.abspath + [self]

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




class DriveRootDirectory:
    def __init__(self, user):
        self.user = user
        self.abspath = [self]
        self.slashpath = '/'
        self.shared = False
        self.public = False
        self.parent = None
        self.subdirectories = DriveDirectory.objects.filter(user=user, parent=None)
        self.files = DriveFile.objects.filter(user=user, parent=None)

    @property
    def name(self):
        return '{}'.format(self.user.username)

    @property
    def as_link(self):
        return format_html(
            '<a href="{url}">{name}</a>',
            url=self.reverse,
            name=self.name
        )

    def reverse(self):
        return reverse('drive-listing', args=[self.user.username + '/'])
