from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Min

from .forms import CourseFilterForm
from .models import Department, Time, Course, TimeStamp

def index(request):
    context = RequestContext(request)
    if request.GET:
        form = CourseFilterForm(request.GET)
    else:
        form = CourseFilterForm()
    if form.is_valid():
        courses = Department.objects.get(abbr=form.cleaned_data['department']).courses
        if form.cleaned_data['operation'] == 'except':
            not_time = Time.objects.filter(value__in=form.cleaned_data['time'])
        else:
            not_time = Time.objects.exclude(value__in=form.cleaned_data['time'])
        courses = courses.exclude(time__in=not_time)
        ordering = form.cleaned_data['ordering']
        if ordering != 'number':
            if ordering == 'title_geinfo':
                courses = courses.order_by('-is_gec', ordering, 'number')
            else:
                if ordering == 'firsttime':
                    courses = courses.annotate(firsttime=Min('time'))
                courses = courses.order_by(ordering, 'number')
        context['courses'] = courses.distinct()
    context['form'] = form
    context['timestamp'] = TimeStamp.objects.last().stamp
    return render_to_response('courses.html', context)

def syllabus(request, number):
    course = Course.objects.get(number=number)
    context = RequestContext(request)
    context['course'] = course
    context['timestamp'] = TimeStamp.objects.last().stamp
    return render_to_response('syllabus.html', context)
