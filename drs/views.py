from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import ListView
from django.contrib.auth.models import User

# Create your views here.

def home(request):
    return render_to_response('home.html', RequestContext(request))


class AboutView(ListView):
    template_name = 'about.html'
    queryset = User.objects.filter(is_superuser=True)
    context_object_name = 'maintainers'
