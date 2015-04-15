from django.conf.urls import patterns, url

from printer_schedule import views

urlpatterns = patterns('',
    url(r'^$', views.ScheduleIndex.as_view(), name='index'),
)
