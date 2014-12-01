from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.views import login as django_login_view
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.core.urlresolvers import reverse
from django.http import Http404

from .models import Profile
from .forms import EmailForm

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
        email_form = EmailForm(request.POST)
        if form.is_valid() and email_form.is_valid():
            user = form.save()
            login(request,
                authenticate(
                    username=form.cleaned_data['username'],
                    password=form.cleaned_data['password1'],
                )
            )
            user.email = email_form.cleaned_data['email']
            user.save()
            Profile.objects.create(user=user)
            return redirect('profile')
    else:
        form = UserCreationForm()
        email_form = EmailForm()
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
    return render_to_response('profile.html', context)

@login_required
def get_email_token(request):
    context = RequestContext(request)
    if request.user.profile.email_verified:
        context['error'] = 'Your email is already verified.'
    else:
        if request.user.email:
            token = request.user.profile.gen_email_token()
            success = send_mail(
                'ditrobotics.tw email verification',
                'Dear {username},\n'
                'Please visit the link below to verifiy your email:\n'
                '{link}'.format(
                    username=request.user.username,
                    link=request.META.get('SERVER_NAME', 'SERVER_NAME') + reverse('verify_email') + '?token=' + token
                ),
                'noreply.ditrobotics@gmail.com',
                [request.user.email],
            )
            if not success:
                context['error'] = 'The server failed to send an email to {}'.format(request.user.email)
        else:
            context['error'] = 'You have not set your email yet!'
    return render_to_response('sent-email.html', context)

def verify_email(request):
    context = RequestContext(request)
    token = request.GET.get('token', None)
    if token is None:
        raise Http404
    vuser = get_object_or_404(Profile, email_token=token).user
    context['vuser'] = vuser
    if vuser.profile.email_token_expire > timezone.now():
        return render_to_response('email-verified.html', context)
    else:
        return render_to_response('email-link-expired.html', context)
