from django.db import models

# Create your models here.

class Course(models.Model):
    time = models.CharField(max_length=20)
    number = models.CharField(max_length=20)
    capabilities = models.TextField()
    credit = models.PositiveSmallIntegerField(null=True)
    enrollment = models.PositiveSmallIntegerField()
    instructor = models.CharField(max_length=20)
    room = models.CharField(max_length=20)
    title_en = models.CharField(max_length=40)
    title_zh = models.CharField(max_length=40)
    note = models.TextField()


class Syllabus(models.Model):
    course = models.OneToOneField(Course)
    has_attachment = models.BooleanField(default=False)


class Department(models.Model):
    abbr = models.CharField(max_length=4)
    name_zh = models.CharField(max_length=20)
    name_en = models.CharField(max_length=40)
    courses = models.ManyToManyField(Course)
