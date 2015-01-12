import os
import shutil

from django.core.management.base import BaseCommand

from nthucourses.models import Course


class Command(BaseCommand):
    args = '<pdf-dir>'
    help = 'deploy course pdf files'
    def handle(self, pdfdir, **options):
        target_dir = os.path.join('nthucourses', 'static', 'syllabus-pdf')
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
                self.stdout.write('copied file {}'.format(dst))
