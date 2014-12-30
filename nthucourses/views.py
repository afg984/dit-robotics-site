import os
import json

from django.shortcuts import render_to_response
from django.template import RequestContext

with open(os.path.join(os.path.dirname(__file__), 'courses.json')) as file:
    data = json.load(file)


def index(request):
    context = RequestContext(request)
    context['courses'] = data.values()
    return render_to_response('courses.html', context)
