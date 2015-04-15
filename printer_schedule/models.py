from django.db import models
from django.contrib.auth.models import User


class PrinterSchedule(models.Model):
    est_duration = models.DurationField(null=True)
    time_started = models.DateTimeField(null=True)
    time_ended = models.DateTimeField(null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    gcode_file = models.FileField(blank=True)
    done = models.BooleanField(default=False)
    submitter = models.ForeignKey(
        User,
        related_name='printer_schedule_submitted')
    started_by = models.ForeignKey(
        User,
        related_name='printer_schedule_started')
    ended_by = models.ForeignKey(
        User,
        related_name='printer_schedule_ended')
    propose = models.CharField(max_length=256)
    important = models.BooleanField(default=False)

    class Meta:
        ordering = ('time_created',)
