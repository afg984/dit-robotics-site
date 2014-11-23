from django.conf.urls import url

from . import views

urlpattens = [
    url('^$', views.drive, name='drive'),
]
