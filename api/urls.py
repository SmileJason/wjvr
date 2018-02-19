# -*- coding: utf-8 -*-

from django.conf.urls import url
from api.views import get_vrmodes, get_banners, get_pagetypes, get_pages, get_pagedetail

urlpatterns = [

    url(r'^getModes/$', get_vrmodes),

    url(r'^getBanners/$', get_banners),

    url(r'^getPageTypes/$', get_pagetypes),

    url(r'^getPages/$', get_pages),

    url(r'^getPageDetail/$', get_pagedetail),

    url(r'^pagedetail/(?P<page_id>\d+)/$', get_pagedetail),

]