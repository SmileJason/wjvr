# -*- coding: utf-8 -*-

from django.conf.urls import url
from api.views import get_vrmodes

urlpatterns = [

    url(r'^getvrs/$', get_vrmodes),

]