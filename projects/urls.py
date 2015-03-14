from django.conf.urls import url, patterns

from projects import views


urlpatterns = patterns('',
    url(r'^$', views.ProjectIndex.as_view(), name='index'),
    url(r'^create/$', views.ProjectCreate.as_view(), name='create'),
    url(r'^(?P<pk>\d+)/$', views.ProjectUpdate.as_view(), name='update'),
)
