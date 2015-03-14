from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.drive, name='index'),
    url(r'^l/(.+/)$', views.listing, name='dir'),
    url(r'^lt/(.+/)$', views.listingtable, name='dirtable'),
    url(r'^g/(\d+)/(.+)$', views.get, name='file'),
    url(r'^delete/(\d+)$', views.delete, name='rm'),
    url(r'^mkdir/(.+/)$', views.mkdir, name='mkdir'),
    url(r'^rmdir/(\d+)$', views.rmdir, name='rmdir'),
]
