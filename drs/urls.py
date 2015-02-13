from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import settings
from . import views

urlpatterns = patterns('',
    url(r'^$', views.AboutView.as_view(), name='home'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^drive/', include('drive.urls')),
    url(r'^message_board/', include('message_board.urls')),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^nthucourses/', include('nthucourses.urls', namespace='nthucourses')),
    url(r'^dpcstatus/', include('dpcstatus.urls', namespace='dpcstatus')),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
