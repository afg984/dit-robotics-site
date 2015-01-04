from django.views.generic import TemplateView, ListView
from django.contrib.auth.models import User

class AboutView(ListView):
    template_name = 'about.html'
    queryset = User.objects.filter(is_superuser=True)
    context_object_name = 'maintainers'
