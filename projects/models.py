from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    title = models.CharField('標題', max_length=48)
    intro = models.CharField('簡介', max_length=48, blank=True)
    content = models.TextField('內容')
    on_homepage = models.BooleanField('在首頁顯示', default=False)
    collaborators = models.ManyToManyField(User, verbose_name='成員')
    cover_photo = models.ImageField('封面照片',
        upload_to='projects/',
        blank=True,
    )
