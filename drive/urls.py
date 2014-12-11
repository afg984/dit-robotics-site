from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.drive, name='drive'),
    url(r'^get/(\d+)/', views.get, name='drive-get'),
    url(r'^delete/(\d+)/', views.delete, name='drive-delete'),
]
