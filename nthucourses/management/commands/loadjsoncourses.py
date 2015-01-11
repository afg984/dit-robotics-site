import json

from django.core.management.base import BaseCommand, CommandError

from nthucourses.models import Course, Syllabus


class Command(BaseCommand):
    args = '<jsonfile>'
    help = 'Update course data from json file'

    def handle(self, jsonfile, **options):
        with open(jsonfile) as file:
            jsondata = json.load(file)
        Course.objects.all().delete()
        for course in jsondata['courses'].values():
            Course.objects.create(
                time=''.join(course['time']),
                number=course['no'],
                capabilities=courses['capabilities'],
                credit=courses['credit'],
                enrollment=courses['enrollment'],
                instructor=courses['instructor'],
                room=courses['room'],
                title_en=courses['title_en'],
                title_zh=courses['title_zh'],
                note=courses['note'],
            )
        
