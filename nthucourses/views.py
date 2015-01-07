from django.shortcuts import render_to_response
from django.template import RequestContext

from .data import courses as data
from .forms import CourseFilterForm

def index(request):
    context = RequestContext(request)
    form = CourseFilterForm(request.GET)
    if form.is_valid():
        courses = data
        courses = courses.within_departments(form.cleaned_data['department'])
        if form.cleaned_data['operation'] == 'except':
            courses = courses.except_times(form.cleaned_data['times'])
        else:
            courses = courses.within_times(form.cleaned_data['times'])
        context['courses'] = courses.values()
    else:
        form = CourseFilterForm()
    context['form'] = form
    return render_to_response('courses.html', context)