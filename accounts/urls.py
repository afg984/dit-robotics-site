from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^profile/$', views.profile_redirect, name='profile'),
    url(r'^profile/([\w.@+-]+)/$', views.profile, name='profile'),
    url(r'^userlist/$',
        login_required(views.UserList.as_view()),
        name='userlist'),
]
