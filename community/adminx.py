# -*- coding: utf-8 -*-
import os
import xadmin
from community.models import PublishType, Publish, PublishComment
from xadmin import views
from django.db import transaction
from common import LOG

class PublishAdmin(object):
	list_display = ('title', 'type', 'content', 'user', 'create_time')
	search_fields = ('title', )
	show_detail_fields = ['title', ]

	@transaction.atomic
	def delete_models(self, queryset):
		for publish in queryset.all():
			if publish.pic1:
				file = publish.pic1.path
				if os.path.exists(file):
					os.remove(file)
			if publish.pic2:
				file = publish.pic2.path
				if os.path.exists(file):
					os.remove(file)
			if publish.pic3:
				file = publish.pic3.path
				if os.path.exists(file):
					os.remove(file)
			if publish.pic4:
				file = publish.pic4.path
				if os.path.exists(file):
					os.remove(file)
		super(PublishAdmin, self).delete_models(queryset)

xadmin.site.register(Publish, PublishAdmin)

class PublishCommentAdmin(object):
	list_display = ('publish', 'user', 'text', 'create_time')
	search_fields = ('publish.title', )

xadmin.site.register(PublishComment, PublishCommentAdmin)

class PublishTypeAdmin(object):
	list_display = ('name', 'status', 'order')
	search_fields = ('name', )

xadmin.site.register(PublishType, PublishTypeAdmin)