from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Workgroup(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(User, through='Membership')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tracker:workgroup', kwargs={'pk': self.pk})


class Membership(models.Model):
    user = models.ForeignKey(User)
    workgroup = models.ForeignKey(Workgroup)
    administrative = models.BooleanField(default=False)


class Task(models.Model):
    name = models.CharField('名稱', max_length=128)
    workgroup = models.ForeignKey(Workgroup)
    created = models.DateTimeField('建立時間', auto_now_add=True)
    started = models.DateField('開始日期', null=True)
    ended = models.DateField('結束日期', null=True)
    due = models.DateField('截止日期', null=True)

    def __str__(self):
        return self.name
