from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView
from django.http import Http404
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404 as go4

from drive.http import AttachmentResponse
from projects.models import Project


class ProjectEditCommon:
    model = Project
    fields = '__all__'
    context_object_name = 'project'

    def post(self, request, *args, **kwargs):
        if (not request.user.is_authenticated()) or request.user.profile.access_level < 2:
            raise PermissionDenied
        else:
            return super().post(request, *args, **kwargs)


class ProjectCreate(ProjectEditCommon, CreateView):
    template_name = 'projects/create.html'


class ProjectUpdate(ProjectEditCommon, UpdateView):
    template_name = 'projects/update.html'


def cover_photo(request, pk):
    project = go4(Project, pk=pk)
    if project.cover_photo:
        return AttachmentResponse(file=project.cover_photo)
    else:
        raise Http404('This project does not have a cover photo.')
