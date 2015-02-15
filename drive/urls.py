from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.drive, name='drive'),
    url(r'^l/(.+/)$', views.listing, name='drive-listing'),
    url(r'^lt/(.+/)$', views.listingtable, name='drive-listingtable'),
    url(r'^g/(\d+)/(.+)$', views.get, name='drive-get'),
    url(r'^delete/(\d+)$', views.delete, name='drive-delete'),
    url(r'^mkdir/(.+/)$', views.mkdir, name='drive-mkdir'),
    url(r'^rmdir/(\d+)$', views.rmdir, name='drive-rmdir'),
]
