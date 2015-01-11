from django.db import models

# Create your models here.

class Course(models.Model):
    time = CharField(max_length=20)
    number = CharField(max_length=20)
    capabilities = TextField()
    credit = PositiveSmallIntegerField(null=True)
    enrollment = PositiveSmallIntegerField()
    instructor = CharField(max_length=20)
    room = CharField(max_length=20)
    title_en = CharField(max_length=40)
    title_zh = CharField(max_length=40)
    note = TextField()


class Syllabus(models.Model):
    course = models.OneToOneField(Course)
    has_attachment = models.BooleanField()
