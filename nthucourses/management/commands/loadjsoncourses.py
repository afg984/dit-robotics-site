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
                capabilities=course['capabilities'],
                credit=course['credit'],
                enrollment=course['enrollment'],
                instructor=course['instructor'],
                room=course['room'],
                title_en=course['title_en'],
                title_zh=course['title_zh'],
                note=course['note'],
            )
        
