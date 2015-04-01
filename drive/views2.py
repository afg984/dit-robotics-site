from django.http import JsonResponse
from django.views.generic.base import View


from drive.models import DriveDirectory as Directory, DriveFile as File


class DirectoryView(View):
    def get(self, request, pk=None):
        return JsonResponse({
            'directories': {d.name: d.pk for d in Directory.objects.filter(parent=pk)},
            'file': {f.filename: f.pk for f in File.objects.filter(parent=pk)},
        })
