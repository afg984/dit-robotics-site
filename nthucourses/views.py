from django.shortcuts import render_to_response
from django.template import RequestContext

from .data import data


def index(request):
    context = RequestContext(request)
    context['courses'] = data.values()
    return render_to_response('courses.html', context)