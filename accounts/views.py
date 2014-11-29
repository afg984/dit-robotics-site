from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.http import Http404
from django.contrib.auth.models import User

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
    context['form'] = form
    return render_to_response('registeration.html', context)

def profile(request, username=None):
    context = RequestContext(request)
    if username is None:
        if request.user.is_authenticated:
            context['profileuser'] = request.user
        else:
            return redirect('login')
    else:
         context['profileuser'] = get_object_or_404(Users, username=username)
    return render_to_response('profile.html', context)

