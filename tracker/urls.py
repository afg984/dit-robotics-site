from django.conf.urls import patterns, url

from tracker import views

urlpatterns = patterns('',
    url(r'^$', views.TrackerIndex.as_view(), name='index'),
    url(r'^workgroups/$', views.WorkgroupCreate.as_view(), name='create_workgroup'),
)
