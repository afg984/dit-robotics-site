from django.shortcuts import render_to_response
from django.template import RequestContext

# Create your views here.

def home(request):
    return render_to_response('home.html', RequestContext(request))
