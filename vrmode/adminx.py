# -*- coding: utf-8 -*-
import os
import shutil
import zipfile
import xadmin
from vrmode.models import VRMode
from django.db import transaction
from xadmin import views
from common import LOG

class VRModeAdmin(object):
	list_display = ('title', 'intro')
	search_fields = ('title', 'intro')
	fieldsets = (
		(u'基本信息', {'fields': ('title', 'intro', 'create_time')}),
		(u'文件管理', {'fields': ('cover', 'vrzip', 'vrlink')}),
	)
	show_detail_fields = ['title', ]
	# data_charts = {
 #    "vrmode": {'title': u"VR方案统计", "x-field": "create_time", "y-field": ("create_time",),
 #                   "order": ('create_time',)},
 #    }

	@transaction.atomic
	def save_models(self):
		obj = self.new_obj
		super(VRModeAdmin, self).save_models()
		if obj.vrzip:
			file = obj.vrzip.path
			if os.path.exists(file):
				name = os.path.basename(file)
				path = './media/uploads/vrzip/'+name[:-4]
				if not os.path.exists(path):
					z = zipfile.ZipFile(file, 'r')
					z.extractall(path='./media/uploads/vrzip/'+name[:-4])
					z.close()
					obj.vrlink = '/media/	uploads/vrzip/'+name[:-4]+'/vtour/vtour.html'
					obj.save()

	@transaction.atomic
	def delete_models(self, queryset):
		for vr in queryset.all():
			file = vr.cover.path
			vrzip = vr.vrzip
			# vr.delete()
			if os.path.exists(file):
				os.remove(file)
			if vrzip:
				file = vrzip.path
				if os.path.exists(file):
					os.remove(file)
				file = vrzip.path[:-4]
				if os.path.exists(file):
					shutil.rmtree(file)
		super(VRModeAdmin, self).delete_models(queryset)
    # def save_models(self):
		# obj = self.new_obj
		# LOG.error(obj.cover)
		# obj.save()
		# LOG.error(obj.title)
		# request = self.request
		# obj.author = str(request.user)
		# obj.save()
		# super().save_models()

	# @transaction.atomic
	# def delete_models(self, queryset):
		# LOG.error('+++++++++++++')
		# for vr in queryset.all():
		# 	LOG.error(vr.title)
		# 	file = vr.cover.path
		# 	if os.path.exists(file):
		# 		LOG.error('--------------')
		# 		os.remove(file)
		# 	if vr.vrzip:
		# 		LOG.error('-------adsadsa---')
		# 		file = vr.vrzip.path
		# 		if os.path.exists(file):
		# 			os.remove(file)

xadmin.site.register(VRMode, VRModeAdmin)