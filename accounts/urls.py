from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    url(r'^login/$', views.login_view, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', dict(next_page='login'), name='logout'),
    url(r'^registration/$', views.registration_view, name='registration'),
    url(r'^profile/$', views.profile_redirect, name='profile'),
    url(r'^profile/([\w.@+-]+)/$', views.profile, name='profile'),
    url(r'^email/get-token/$', views.get_email_token, name='get_email_token'),
    url(r'^email/verify/([0-9A-Za-z]{64})/$', views.verify_email, name='verify_email'),
    url(r'^userlist/$',
        login_required(views.UserList.as_view()),
        name='userlist'),
]
