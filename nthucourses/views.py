from django.shortcuts import render
from django.db.models import Min

from .forms import CourseFilterForm
from .models import Department, Time, Course, MetaData, Prerequisite


def update_protect(view):
    def _view(request, *args, **kwargs):
        if MetaData.objects.last().is_updating:
            return render(request, 'nthucourses/updating.html')
        return view(request, *args, **kwargs)
    return _view

@update_protect
def index(request):
    context = {}
    if request.GET:
        form = CourseFilterForm(request.GET)
    else:
        form = CourseFilterForm()
    if form.is_valid():
        courses = Course.objects.filter(department__in=Department.objects.filter(abbr__in=form.cleaned_data['department']))
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
    context['metadata'] = MetaData.objects.last()
    return render(request, 'courses.html', context)

@update_protect
def syllabus(request, number):
    course = Course.objects.get(number=number)
    context = {}
    context['course'] = course
    context['metadata'] = MetaData.objects.last()
    return render(request, 'syllabus.html', context)

@update_protect
def prerequisites(request):
    context = dict()
    context['prerequisites'] = Prerequisite.objects.order_by('course_title')
    return render(
        request,
        'prerequisites.html',
        context,
    )
