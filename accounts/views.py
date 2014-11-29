from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import login as django_login_view
from django.contrib.auth import login, authenticate
from django.http import Http404

# Create your views here.

def login_view(request):
    if request.user.is_authenticated():
        return redirect('profile')
    else:
        return django_login_view(request, template_name='login.html')


def registration_view(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            login(request,
                authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                )
            )
            return redirect('profile')
    else:
        form = UserCreationForm()
    context['form'] = form
    return render_to_response('registration.html', context)

def profile(request, username=None):
    context = RequestContext(request)
    if username is None:
        if request.user.is_authenticated():
            context['profileuser'] = request.user
        else:
            return redirect('login')
    else:
         context['profileuser'] = get_object_or_404(User, username=username)
    return render_to_response('profile.html', context)

