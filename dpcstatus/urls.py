from django.conf.urls import url

from dpcstatus import views


urlpatterns = [
    url(r'$', views.index, name='index'),
]
