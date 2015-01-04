from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import settings
from . import views

urlpatterns = patterns('',
    url(r'^$', views.AboutView.as_view(), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^drive/', include('drive.urls')),
    url(r'^message_board/', include('message_board.urls')),
    url(r'^accounts/', include('accounts.urls')),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
