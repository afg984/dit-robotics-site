from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from .forms import UploadFileForm
# Create your views here.

@login_required
def drive(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            drive_file = form.save(commit=False)
            drive_file.filename = 'NotImplemented'
            drive_file.save()
            return redirect('drive')
    else:
        form = UploadFileForm()
    context['form'] = form
    return render_to_response('drive.html', context)
