from django.conf.urls import patterns, url

from tracker import views

urlpatterns = patterns('',
    url(r'^$', views.TrackerIndex.as_view(), name='index'),
    url(r'^workgroups/$', views.WorkgroupCreate.as_view(), name='create_workgroup'),
    url(r'^workgroups/(?P<pk>\d+)/$', views.WorkgroupDetail.as_view(), name='workgroup'),
    url(r'^workgroups/(?P<workgroup>\d+)/create-task/$', views.TaskCreate.as_view(), name='create_task'),
)
