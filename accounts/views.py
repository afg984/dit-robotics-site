from django.shortcuts import render_to_response
from django.templates import RequestContext
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def registeration_view(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = UserCreationForm()
    return render_to_response('registeration.html')

