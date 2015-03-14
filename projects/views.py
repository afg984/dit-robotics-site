from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

from projects.models import Project


class ProjectIndex(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/index.html'


class ProjectEditCommon:
    model = Project
    fields = '__all__'
    context_object_name = 'project'


class ProjectCreate(ProjectEditCommon, CreateView):
    template_name = 'projects/create.html'


class ProjectUpdate(ProjectEditCommon, UpdateView):
    template_name = 'projects/update.html'
