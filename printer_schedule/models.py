import os

from django.db import models
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.core.urlresolvers import reverse


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

    def gcode_link(self):
        if not self.gcode_file:
            return ''
        gcode_filename = os.path.basename(self.gcode_file.name)
        return format_html(
            '<a href="{url}">{name}</a>',
            url=reverse(
                'printer_schedule:gcode_file',
                kwargs={
                    'pk': self.pk,
                    'fn': gcode_filename,
                }
            ),
            name=gcode_filename
        )
