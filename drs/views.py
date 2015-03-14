from django.views.generic import TemplateView, ListView

from projects.models import Project


class AboutView(ListView):
    template_name = 'home.html'
    queryset = Project.objects.filter(on_homepage=True)
    context_object_name = 'projects'
