from django.views.generic.list import ListView

from tracker.models import Workgroup


class TrackerIndex(ListView):
    model = Workgroup
    template_name = 'tracker/index.html'
    context_object_name = 'workgroups'
