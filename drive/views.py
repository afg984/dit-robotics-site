from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponse

from drs import settings

from .forms import UploadFileForm
from .models import DriveFile
# Create your views here.

def require_member(*args, **kw):
    def is_member(user):
        return user.is_authenticated() and user.profile.access_level > 1
    return user_passes_test(is_member)(*args, **kw)

@require_member
def drive(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            drive_file = form.save(commit=False)
            drive_file.filename = request.FILES['file']
            drive_file.user = request.user
            drive_file.save()
            return redirect('drive')
    else:
        form = UploadFileForm()
    context['form'] = form
    files = DriveFile.objects.filter(user=request.user)
    context['files'] = files
    context['usage'] = sum(drive_file.file.size for drive_file in files)
    return render_to_response('drive.html', context)

def get(request, id):
    drive_file = get_object_or_404(DriveFile, id=id)
    if drive_file.user != request.user:
        return render_to_response('drive_denied.html', RequestContext(request))
    response = HttpResponse()
    response['Content-Disposition'] = 'attachment; filename={}'.format(drive_file.filename)
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
