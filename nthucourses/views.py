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
        courses = Department.objects.get(abbr=form.cleaned_data['department']).courses
        time = Time.objects.filter(value__in=cleaned_data['times'])
        if form.cleaned_data['operation'] == 'except':
            for sect in time:
                course = course.exclude(time__contains=sect)
        else:
            courses = courses.filter(time__in=time)
        context['courses'] = courses
    context['form'] = form
    return render_to_response('courses.html', context)
