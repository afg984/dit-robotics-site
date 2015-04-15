from django.views.generic.list import ListView

from printer_schedule.models import PrinterSchedule


class ScheduleIndex(ListView):
    template_name = 'printer_schedule/listing.html'
    queryset = PrinterSchedule.objects.filter(time_ended__isnull=False)
    context_object_name = 'schedule_list'
