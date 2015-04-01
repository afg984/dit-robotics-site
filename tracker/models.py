from django.db import models
from django.contrib.auth.models import User


class Workgroup(models.Model):
    name = models.CharField(max_length=128)
    members = models.ManyToManyField(User, through='Membership')

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.ForeignKey(User)
    workgroup = models.ForeignKey(Workgroup)
    administrative = models.BooleanField(default=False)


class Task(models.Model):
    name = models.CharField('名稱', max_length=128)
    created = models.DateTimeField('建立於', auto_now_add=True)
    started = models.DateTimeField('開始於', null=True)
    ended = models.DateTimeField('結束於', null=True)
    due = models.DateTimeField('截止於', null=True)
