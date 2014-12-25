from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404

import itertools

from drs import settings

from .forms import UploadFileForm
from .models import DriveFile
# Create your views here.

def errors_to_string(errors):
    return '; '.join(
        map(
            str,
            itertools.chain(
                *itertools.chain(
                    *errors.as_data().values()
                )
            )
        )
    )

@login_required
def drive(request):
    context = RequestContext(request)
    if request.user.profile.access_level < 2:
        return render_to_response('drive_member_required.html', context)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            drive_file = form.save(commit=False)
            drive_file.filename = request.FILES['file']
            drive_file.user = request.user
            drive_file.save()
            return redirect('drive')
        else:
            if request.META.get('HTTP_DROPZONE_IDENTIFIER', None) == 'driveDropzone':
                return HttpResponse(
                    errors_to_string(form.errors),
                    status=422
                )
    else:
        form = UploadFileForm()
    context['form'] = form
    files = DriveFile.objects.filter(user=request.user).order_by('filename', 'created_at')
    context['files'] = files
    context['usage'] = sum(drive_file.file.size for drive_file in files)
    return render_to_response('drive.html', context)

def get(request, username, id, filename):
    drive_file = get_object_or_404(DriveFile, id=id, filename=filename)
    if drive_file.user != request.user:
        return render_to_response('drive_denied.html', RequestContext(request))
    if drive_file.user.username != username:
        raise Http404
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment'
    if settings.DEBUG:
        response.content = drive_file.file.read()
    else:
        response['X-Accel-Redirect'] = drive_file.file.url
    return response

def delete(request, id):
    drive_file = get_object_or_404(DriveFile, id=id)
    if drive_file.user != request.user:
        return render_to_response('drive_denied.html', RequestContext(request))
    drive_file.delete()
    return redirect('drive')
