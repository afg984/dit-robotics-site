from django.views.generic import TemplateView

from projects.models import Project


class AboutView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        return {
            'projects': Project.objects.all(),
            'cover_projects': Project.objects.filter(on_homepage=True)
        }
