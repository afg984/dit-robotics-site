from django.conf.urls import patterns, include, url
from django.contrib import admin

from . import settings

urlpatterns = patterns('',
    url(r'^$', 'drs.views.home', name='home'),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^drive/', include('drive.urls')),
    url(r'^chinesc/', include('chinesc.urls')),
)

if settings.DEBUG:
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()
