from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.shortcuts import redirect

from generic.views import LoginRequiredMixin
from tracker.models import Workgroup, Membership


class TrackerIndex(ListView):
    model = Workgroup
    template_name = 'tracker/index.html'
    context_object_name = 'workgroups'


class WorkgroupCreate(LoginRequiredMixin, CreateView):
    model = Workgroup
    template_name = 'tracker/workgroup_create.html'
    fields = ('name',)

    def form_valid(self, form):
        workgroup = form.save()
        Membership.objects.create(
            user=self.request.user,
            workgroup=workgroup,
            administrative=True,
        )
        return redirect(workgroup)


class WorkgroupDetail(LoginRequiredMixin, DetailView):
    model = Workgroup
    template_name = 'tracker/workgroup_detail.html'
