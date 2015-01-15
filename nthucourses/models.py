import os

from django.db import models
from django.utils.encoding import iri_to_uri

# Create your models here.

class MetaData(models.Model):
    timestamp = models.DateTimeField()
    semester = models.CharField(max_length=5)

    @property
    def semester_hr(self):
        return '{} 學年度第 {} 學期'.format(
            self.semester[:3],
            self.semester[4]
        )


class Time(models.Model):
    weekdays = 'MTWRFS'
    hours = '1234n56789abc'
    value = models.CharField(max_length=2, unique=True, db_index=True)

    def __str__(self):
        return self.value


class Course(models.Model):
    pdf_dir = 'static/syllabus-pdf/'
    time = models.ManyToManyField(Time)
    number = models.CharField(max_length=20, db_index=True)
    capabilities = models.TextField()
    credit = models.PositiveSmallIntegerField()
    size_limit = models.PositiveSmallIntegerField(null=True)
    enrollment = models.PositiveSmallIntegerField()
    instructor = models.CharField(max_length=20)
    room = models.CharField(max_length=20)
    title_en = models.CharField(max_length=40)
    title_zh = models.CharField(max_length=40)
    title_geinfo = models.CharField(max_length=50)
    is_gec = models.BooleanField(default=False)
    note = models.TextField()
    outline = models.TextField()
    attachment = models.PositiveIntegerField(null=True)
    credit_density = models.FloatField(null=True, db_index=True)
    enrollment_density = models.FloatField(null=True, db_index=True)

    class Meta:
        ordering = ('number',)
        index_together = (('is_gec', 'title_geinfo'),)

    def __str__(self):
        return self.number

    @property
    def time_string(self):
        return ''.join(map(str, self.time.all()))

    @property
    def pdf_url(self):
        return iri_to_uri('/{}{}.pdf'.format(self.pdf_dir, self.number))

    @property
    def has_attachment(self):
        return self.attachment is not None

    @staticmethod
    def _float_division(a, b):
        if a is None or not b:
            return -1.
        return a / b

    def save(self):
        self.credit_density = self._float_division(self.credit, self.time.count())
        self.enrollment_density = self._float_division(self.enrollment, self.size_limit)
        self.is_gec = 'Core' in self.title_geinfo
        super().save()

    @property
    def getag(self):
        return self.title_geinfo.replace('Elective GE course: ', '')


class Department(models.Model):
    abbr = models.CharField(max_length=4, unique=True)
    name_zh = models.CharField(max_length=20)
    name_en = models.CharField(max_length=40)
    courses = models.ManyToManyField(Course)

    class Meta:
        ordering = ('abbr',)

    def __str__(self):
        return self.abbr
