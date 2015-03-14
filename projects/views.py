from django.views.generic.list import ListView

from projects.models import Project


class ProjectIndex(ListView):
    model = Project
    context_object_name = 'projects'
    template_name = 'projects/index.html'
