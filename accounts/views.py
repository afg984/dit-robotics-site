from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import login as django_login_view
from django.contrib.auth import login, authenticate
from django.http import Http404

from .models import get_profile
from .forms import ProfileEmailForm

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
        email_form = ProfileEmailForm(request.POST)
        if form.is_valid() and email_form.is_valid():
            user = form.save()
            login(request,
                authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                )
            )
            profile = email_form.save(commit=False)
            profile.user = user
            profile.save()
            return redirect('profile')
    else:
        form = UserCreationForm()
        email_form = ProfileEmailForm()
    context['form'] = form
    context['email_form'] = email_form
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
    context['profile'] = get_profile(context['profileuser'])
    return render_to_response('profile.html', context)

