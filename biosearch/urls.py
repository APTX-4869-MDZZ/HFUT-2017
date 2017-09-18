# -*- coding:utf-8 -*-
from django.conf.urls import *
from . import views

urlpatterns = [
    url(r'^randomPage', views.randomPage),
    url(r'^turnPage', views.turnPage),
    url(r'^getDetail', views.getDetail),
    url(r'^bioSearchFirst', views.bioSearchFirst),
    url(r'^getCache', views.getCache),
]