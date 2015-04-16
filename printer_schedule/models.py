from django.db import models
from django.contrib.auth.models import User


class PrinterSchedule(models.Model):
    est_duration = models.DurationField('估計時間', null=True, blank=True)
    time_started = models.DateTimeField(null=True)
    time_ended = models.DateTimeField(null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    gcode_file = models.FileField('.gcode 檔案', upload_to='gcode', blank=True)
    done = models.BooleanField(default=False)
    submitter = models.ForeignKey(
        User,
        related_name='printer_schedule_submitted')
    started_by = models.ForeignKey(
        User,
        null=True,
        related_name='printer_schedule_started')
    ended_by = models.ForeignKey(
        User,
        null=True,
        related_name='printer_schedule_ended')
    purpose = models.CharField('名稱', max_length=256)
    important = models.BooleanField('急件', default=False)

    class Meta:
        ordering = ('time_created',)
