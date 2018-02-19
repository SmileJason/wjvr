# -*- coding: utf-8 -*-

from django.conf.urls import url
from api.views import get_vrmodes, get_banners

urlpatterns = [

    url(r'^getModes/$', get_vrmodes),

    url(r'^getBanners/$', get_banners),

]