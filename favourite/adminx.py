# -*- coding: utf-8 -*-
import os
import xadmin
from vrmode.models import VRMode, Page
from vrauth.models import VRAuth
from favourite.models import FavoritePage, FavoriteVRMode
from django.db import transaction
from xadmin import views
from common import LOG

class FavoritePageAdmin(object):
	list_display = ('user', 'page', )
	search_fields = ('user', 'page')

xadmin.site.register(FavoritePage, FavoritePageAdmin)

class FavoriteVRModeAdmin(object):
	list_display = ('user', 'vrmode', )
	search_fields = ('user', 'vrmode')

xadmin.site.register(FavoriteVRMode, FavoriteVRModeAdmin)