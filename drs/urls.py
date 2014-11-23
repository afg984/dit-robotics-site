from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'drs.views.home', name='home'),
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^drive/', include('drive.urls')),
)
