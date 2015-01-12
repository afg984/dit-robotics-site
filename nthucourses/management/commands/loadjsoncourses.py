import json
import itertools

from django.core.management.base import BaseCommand

from nthucourses.models import Time, Course, Department


class Command(BaseCommand):
    args = '<jsonfile>'
    help = 'Update course data from json file'

    def progress_iter(self, seq, msg):
        total = len(seq)
        width = len(str(total))
        for n, item in enumerate(seq, start=1):
            yield item
            self.stdout.write(
                '{msg}({n:{width}}/{total:{width}})'.format(
                    msg=msg, n=n, width=width, total=total,
                ),
                ending='\r',
            )
        self.stdout.write('')

    def delete_all(self, model):
        while model.objects.count() > 999:
            model.objects.filter(id__gt=max(model.objects.last.id() - 999, model.objects.all()[998].id)).delete()
            self.stdout.write('Deleteing...{:5}'.format(model.objects.count()), ending='\r')
        model.objects.all().delete()
        self.stdout.write('Deletion completed.')

    def handle(self, jsonfile, **options):
        with open(jsonfile) as file:
            self.jsondata = json.load(file)
        self.set_time()
        self.update_courses()
        self.update_departments()

    def set_time(self):
        self.delete_all(Time)
        Time.objects.bulk_create(
            Time(value=''.join(timep))
            for timep in itertools.product(Time.weekdays, Time.hours)
        )
        self.stdout.write('Time creation done.')

    def update_courses(self):
        self.delete_all(Course)
        for course in self.progress_iter(
            self.jsondata['courses'].values(),
            'Writing courses...'
        ):
            courow = Course.objects.create(
                number=course['no'],
                capabilities=course['capabilities'],
                credit=course['credit'],
                enrollment=course['enrollment'],
                instructor=course['instructor'],
                room=course['room'],
                title_en=course['title_en'],
                title_zh=course['title_zh'],
                note=course['note'],
                outline=course['outline'],
                attachment=course['attachment'],
            )
            courow.time = [
                Time.objects.get(value=time) for time in course['time']
            ]
            courow.save()

    def update_departments(self):
        self.delete_all(Department)
        for abbr, department in self.progress_iter(
            self.jsondata['departments'].items(),
            'Writing departments...',
        ):
            deprow = Department.objects.create(
                abbr=abbr,
                name_zh=department['name'],
                name_en=department['name_en'],
            )
            deprow.courses = [
                Course.objects.get(number=course_number)
                for course_number in department['curriclum']
            ]
            deprow.save()
