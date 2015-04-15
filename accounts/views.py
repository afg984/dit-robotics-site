from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView

from .models import Profile


@login_required
def profile_redirect(request):
    return redirect(Profile.objects.get_or_create(user=request.user)[0])


def profile(request, username):
    context = {}
    context['profileuser'] = get_object_or_404(User, username=username)
    context['isself'] = (request.user == context['profileuser'])
    return render(request, 'accounts/profile.html', context)


class UserList(ListView):
    context_object_name = 'all_users'
    queryset = User.objects.all()
    template_name = 'accounts/userlist.html'
