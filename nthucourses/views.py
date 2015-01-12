from django.shortcuts import render_to_response
from django.template import RequestContext

from .forms import CourseFilterForm
from .models import Department, Time

def index(request):
    context = RequestContext(request)
    if request.GET:
        form = CourseFilterForm(request.GET)
    else:
        form = CourseFilterForm()
    if form.is_valid():
        courses = Department.objects.get(abbr=form.cleaned_data['department']).courses.all()
        if form.cleaned_data['operation'] == 'except':
            not_time = Time.objects.filter(value__in=form.cleaned_data['times'])
        else:
            not_time = Time.objects.exclude(value__in=form.cleaned_data['times'])
        courses = courses.exclude(time__in=not_time)
        context['courses'] = courses
    context['form'] = form
    return render_to_response('courses.html', context)
