from django.shortcuts import render_to_response
from django.template import RequestContext

from .data import data
from .forms import CourseFilterForm

def index(request):
    context = RequestContext(request)
    form = CourseFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['operation'] == 'except':
            ddata = data.except_times(form.cleaned_data['times'])
        else:
            ddata = data.within_times(form.cleaned_data['times'])
        context['courses'] = ddata.values()
    else:
        form = CourseFilterForm()
    context['form'] = form
    return render_to_response('courses.html', context)