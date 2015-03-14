from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from projects.models import Project


class ProjectIndex(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/index.html'


class ProjectCreate(CreateView):
    model = Project
    fields = '__all__'
    context_object_name = 'project'
    template_name = 'projects/edit.html'
