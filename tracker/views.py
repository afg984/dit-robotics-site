from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from generic.views import LoginRequiredMixin
from tracker.models import Workgroup


class TrackerIndex(ListView):
    model = Workgroup
    template_name = 'tracker/index.html'
    context_object_name = 'workgroups'


class WorkgroupCreate(LoginRequiredMixin, CreateView):
    model = Workgroup
    template_name = 'tracker/workgroup_create.html'
    fields = ('name',)
