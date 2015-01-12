from django.db import models

# Create your models here.

class Time(models.Model):
    weekdays = 'MTWRFS'
    hours = '1234n56789abc'
    value = models.CharField(max_length=2, unique=True)

    def __str__(self):
        return self.value


class Course(models.Model):
    time = models.ManyToManyField(Time)
    number = models.CharField(max_length=20)
    capabilities = models.TextField()
    credit = models.PositiveSmallIntegerField()
    size_limit = models.PositiveSmallIntegerField(null=True)
    enrollment = models.PositiveSmallIntegerField()
    instructor = models.CharField(max_length=20)
    room = models.CharField(max_length=20)
    title_en = models.CharField(max_length=40)
    title_zh = models.CharField(max_length=40)
    note = models.TextField()
    outline = models.TextField()
    attachment = models.PositiveIntegerField(null=True)

    class Meta:
        ordering = ('number',)

    def __str__(self):
        return self.number

    @property
    def time_string(self):
        return ''.join(map(str, self.time.all()))


class Department(models.Model):
    abbr = models.CharField(max_length=4, unique=True)
    name_zh = models.CharField(max_length=20)
    name_en = models.CharField(max_length=40)
    courses = models.ManyToManyField(Course)

    class Meta:
        ordering = ('abbr',)

    def __str__(self):
        return self.abbr
