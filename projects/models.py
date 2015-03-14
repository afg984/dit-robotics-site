from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse


class Project(models.Model):
    title = models.CharField('標題', max_length=48)
    intro = models.CharField('簡介', max_length=48, blank=True)
    content = models.TextField('內容')
    on_homepage = models.BooleanField('在首頁顯示', default=False)
    members = models.ManyToManyField(User, verbose_name='成員')
    cover_photo = models.ImageField('封面照片',
        upload_to='projects/',
        blank=True,
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('projects:update',
            kwargs={'pk': self.pk}
        )
