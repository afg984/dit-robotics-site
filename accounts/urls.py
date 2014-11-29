from django.contrib.urls import url
from . import views

urlpatterns = [
    url(r'^/login/$', 'django.contrib.auth.views.login', dict(template_name='login.html'), name='login'),
    url(r'^/logout/$', 'django.contrib.auth.views.loguot', dict(template_name='home.html'),
    #url(r'^/login/$', views.login_view, name='login'),
    #url(r'^/logout/$', views.logout_view, name='logout'),
]
