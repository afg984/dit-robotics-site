from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login', dict(template_name='login.html'), name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', dict(template_name='home.html'), name='logout'),
    url(r'^registration/$', views.registration_view, name='registration'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^profile/([\w.@+-]+)/$', views.profile, name='profile'),
    #url(r'^/login/$', views.login_view, name='login'),
    #url(r'^/logout/$', views.logout_view, name='logout'),
]
