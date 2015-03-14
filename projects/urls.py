from django.conf.urls import url, patterns

from projects import views


urlpatterns = patterns('',
    url(r'^$', views.ProjectIndex.as_view(), name='index'),
)
