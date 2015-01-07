from django.shortcuts import render_to_response
from django.template import RequestContext

from .data import courses as data
from .forms import CourseFilterForm

def index(request):
    context = RequestContext(request)
    form = CourseFilterForm(request.GET)
    if form.is_valid():
        if form.cleaned_data['operation'] == 'except':
            courses = data.except_times(form.cleaned_data['times'])
        else:
            courses = data.within_times(form.cleaned_data['times'])
        courses = courses.within_departments(form.cleaned_data['department'])
        context['courses'] = courses.values()
    else:
        form = CourseFilterForm()
    context['form'] = form
    return render_to_response('courses.html', context)