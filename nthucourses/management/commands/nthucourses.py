import os
import sys
import shutil
import json
import itertools

from django.core.management.base import BaseCommand, CommandError
from django.utils.dateparse import parse_datetime

from nthucourses.models import MetaData, Time, Course, Department, Prerequisite


class Command(BaseCommand):
    args = '<commane> <path>'
    help = '''\
loadjson: load json course data from path
 copypdf: copy pdf attachments from path
 loaddir: load all data from directory'''

    def handle(self, *args, **options):
        try:
            command, path = args
        except ValueError:
            raise CommandError('usage: {} nthucourses <command> <path>'.format(sys.argv[0]))
        if command == 'loadjson':
            self.loadjson(path, **options)
        elif command == 'copypdf':
            self.copypdf(path, **options)
        elif command == 'loaddir':
            self.loadjson(os.path.join(path, 'courses.json'))
            self.copypdf(os.path.join(path, 'attachments'))
        else:
            raise CommandError('Unknown command %r' % command)

    def copypdf(self, pdfdir, **options):
        target_dir = os.path.join('nthucourses', Course.pdf_dir)
        if os.path.isdir(target_dir):
            shutil.rmtree(target_dir)
        os.makedirs(target_dir)
        for course in Course.objects.all():
            if course.attachment is not None:
                src = os.path.join(
                    pdfdir,
                    '{}-{}'.format(
                        course.number, course.attachment
                    )
                )
                dst = os.path.join(
                    target_dir,
                    '{}.pdf'.format(course.number)
                )
                shutil.copyfile(src, dst)
                self.stdout.write('copied file %r' % dst)

    def loadjson(self, jsonfile, **options):
        with open(jsonfile) as file:
            self.jsondata = json.load(file)
        self.write_metadata()
        self.update_prerequisites()
        self.set_time()
        self.update_courses()
        self.update_departments()
        self.set_update_done()

    def write_metadata(self):
        dt = parse_datetime(self.jsondata['metadata']['timestamp'])
        semester = self.jsondata['metadata']['semester']
        MetaData.objects.create(timestamp=dt, semester=semester)
        self.stdout.write('Data timestamp: {}, Semester: {}'.format(
            dt.isoformat(), semester))

    def set_update_done(self):
        target = MetaData.objects.last()
        target.is_updating = False
        target.save()

    def progress_iter(self, seq, msg):
        total = len(seq)
        width = len(str(total))
        format_string = '{msg}({n:{width}}/{total:{width}})'
        for n, item in enumerate(seq):
            self.stdout.write(
                format_string.format(
                    msg=msg, n=n, width=width, total=total,
                ),
                ending='\r',
            )
            yield item
        self.stdout.write(format_string.format(
            msg=msg, n=total, width=width, total=total,
        ))

    def delete_all(self, model):
        model.objects.all().delete()
        self.stdout.write('{} deletion completed.'.format(model.__name__))

    def set_time(self):
        self.delete_all(Time)
        Time.objects.bulk_create(
            Time(value=''.join(timep))
            for timep in itertools.product(Time.weekdays, Time.hours)
        )
        self.stdout.write('Time creation done.')

    def update_prerequisites(self):
        Prerequisite.objects.all().delete()
        bulk_targets = list()
        for course_title, info in self.progress_iter(
            self.jsondata['prerequisites'].items(),
            'Loading prerequisites...',
        ):
            bulk_targets.append(Prerequisite(
                course_title=course_title,
                info=json.dumps(info),
            ))
        Prerequisite.objects.bulk_create(bulk_targets)
        self.stdout.write('Written prerequisites.')


    def update_courses(self):
        self.delete_all(Course)
        bulk_targets = list()
        time_targets = list()
        for no, course in self.progress_iter(
            self.jsondata['courses'].items(),
            'Loading courses...'
        ):
            courow = Course(
                number=no,
                capabilities=course['capabilities'],
                credit=course['credit'],
                size_limit=course.get('size', None),
                enrollment=course['enrollment'],
                instructor=course['instructor'],
                room=course['room'],
                title_en=course['title_en'],
                title_zh=course['title_zh'],
                title_geinfo=course['title_geinfo'],
                note=course['note'],
                outline=course['outline'],
                attachment=course['attachment'],
                has_prerequisite=course['has_prerequisite'],
            )
            bulk_targets.append(courow)
            time_targets.append((no,
                [Time.objects.get(value=time) for time in course['time']]
            ))
        self.stdout.write('Writing courses...')
        Course.objects.bulk_create(bulk_targets)
        for number, time in self.progress_iter(
            time_targets,
            'Writing time info for courses...'
        ):
            course = Course.objects.get(number=number)
            course.time = time
            course.save()


    def update_departments(self):
        self.delete_all(Department)
        bulk_targets = list()
        course_targets = list()
        for abbr, department in self.progress_iter(
            self.jsondata['departments'].items(),
            'Loading departments...',
        ):
            deprow = Department(
                abbr=abbr,
                name_zh=department['name'],
                name_en=department['name_en'],
            )
            bulk_targets.append(deprow)
            course_targets.append((abbr, [
                Course.objects.get(number=course_number)
                for course_number in department['curriculum']
            ]))
        self.stdout.write('Writing departments...')
        Department.objects.bulk_create(bulk_targets)
        for abbr, courses in self.progress_iter(
            course_targets,
            'Writing course data for departments...'
        ):
            department = Department.objects.get(abbr=abbr)
            department.courses = courses
            department.save()
