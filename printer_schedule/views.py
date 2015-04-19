from django.shortcuts import redirect, get_object_or_404
from django.core.urlresolvers import reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.utils import timezone
from django.core.exceptions import PermissionDenied

from generic.views import LoginRequiredMixin
from drive.http import AttachmentResponse
from printer_schedule.models import PrinterSchedule


class ScheduleIndex(LoginRequiredMixin, ListView):
    template_name = 'printer_schedule/listing.html'
    queryset = PrinterSchedule.objects.filter(time_ended__isnull=True)
    context_object_name = 'schedule_list'


class ScheduleArchive(LoginRequiredMixin, ListView):
    template_name = 'printer_schedule/archive.html'
    queryset = PrinterSchedule.objects.filter(time_ended__isnull=False)
    context_object_name = 'schedule_list'


class ScheduleCreate(LoginRequiredMixin, CreateView):
    template_name = 'printer_schedule/create.html'
    model = PrinterSchedule
    fields = ('purpose', 'important', 'gcode_file', 'est_duration')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.submitter = self.request.user
        instance.save()
        return redirect('printer_schedule:index')


class ScheduleStart(LoginRequiredMixin, UpdateView):
    model = PrinterSchedule
    fields = ()

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.time_started = timezone.now()
        instance.started_by = self.request.user
        instance.save()
        return redirect('printer_schedule:index')


class ScheduleEnd(LoginRequiredMixin, UpdateView):
    model = PrinterSchedule
    fields = ()

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.time_ended = timezone.now()
        instance.ended_by = self.request.user
        instance.save()
        return redirect('printer_schedule:index')


class ScheduleEdit(LoginRequiredMixin, UpdateView):
    model = PrinterSchedule
    fields = ('purpose', 'important', 'gcode_file', 'est_duration')
    template_name = 'printer_schedule/edit.html'
    success_url = reverse_lazy('printer_schedule:index')


class ScheduleGCodeFile(LoginRequiredMixin, DetailView):
    model = PrinterSchedule

    def get(self, request, pk, fn=None):
        schedule = get_object_or_404(self.model, pk=pk)
        return AttachmentResponse(file=schedule.gcode_file)
