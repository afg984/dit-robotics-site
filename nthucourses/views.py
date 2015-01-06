from django.shortcuts import render_to_response
from django.template import RequestContext

from .data import data
from .forms import CourseFilterForm

def index(request):
    context = RequestContext(request)
    context['courses'] = data.values()
    form = CourseFilterForm(request.GET)
    if not form.is_valid():
        form = CourseFilterForm()
    context['form'] = form
    return render_to_response('courses.html', context)