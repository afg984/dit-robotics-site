from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login/$', 'django.contrib.auth.views.login', dict(template_name='login.html'), name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.loguot', dict(template_name='home.html'), name='logout'),
    #url(r'^/login/$', views.login_view, name='login'),
    #url(r'^/logout/$', views.logout_view, name='logout'),
]
