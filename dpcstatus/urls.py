from django.conf.urls import url

from dpcstatus import views


urlpatterns = [
    url(r'^$', views.index, kwargs={'template_name': 'dpcstatus/summary.html'}, name='index'),
    url(r'^details/$', views.index, kwargs={'template_name': 'dpcstatus/detail.html'}, name='details'),
    url(r'^status-block/$', views.index, kwargs={'template_name': 'dpcstatus/pretty-status.html'}, name='status-block'),
]
