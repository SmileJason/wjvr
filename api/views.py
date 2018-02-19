# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import simplejson as json
# from datetime import datetime
from vrmode.models import VRMode, VRBanner, PageType, Page, PAGE_STATUS_ACTIVE
from common import LOG

def get_vrmodes(request):
	# LOG.error(request.get_host())
	host = request.get_host()
	page = int(request.GET.get('page', 1))
	if page < 1:
		page = 1
	size = int(request.GET.get('size', 2))
	if size < 1:
		size = 1
	vrmodes = VRMode.objects.all()[(page-1)*size:(page)*size]
	data = []
	for vr in vrmodes.all():
		data.append({'cover': host+vr.cover.url, 'title': vr.title, 'intro': vr.intro, 'vrlink': host+vr.vrlink})
	result = {'data': data}
	return HttpResponse(json.dumps(result), content_type='application/json')

def get_banners(request):
	page = int(request.GET.get('page', 1))
	if page < 1:
		page = 1
	size = int(request.GET.get('size', 2))
	if size < 1:
		size = 1
	banners = VRBanner.objects.all()[(page-1)*size:(page)*size]
	data = []
	for vr in banners.all():
		data.append({'cover': host+vr.cover.url, 'title': vr.title, 'intro': vr.intro, 'vrlink': host+vr.vrlink})
	result = {'data': data}
	return HttpResponse(json.dumps(result), content_type='application/json')

def get_pagetypes(request):
	types = PageType.objects.filter(status=PAGE_STATUS_ACTIVE).order_by('order')[:6]
	data = []
	for pagetype in types.all():
		data.append({'name': pagetype.name, 'id': pagetype.id, 'order': pagetype.order})
	result = {'data': data}
	return HttpResponse(json.dumps(result), content_type='application/json')

def get_pages(request):
	host = request.get_host()
	type = request.GET.get('type')
	page = int(request.GET.get('page', 1))
	if page < 1:
		page = 1
	size = int(request.GET.get('size', 5))
	if size < 1:
		size = 1
	pages = Page.objects.filter(status=PAGE_STATUS_ACTIVE, type__id=type).order_by('order')[(page-1)*size:(page)*size]
	data = []
	for page in pages.all():
		data.append({'title': page.title, 'intro': page.intro, 'order': page.order, 'id': page.id, 'cover': host + page.thumb.url, 'time': page.time_display.strftime( '%Y-%m-%d' )})
	result = {'data': data}
	return HttpResponse(json.dumps(result), content_type='application/json')

def get_pagedetail(request, page_id):
	page = get_object_or_404(Page, id=page_id)
	host = request.get_host()
	data = []
	data.append({'title': page.title, 'intro': page.intro, 'order': page.order, 'id': page.id, 'cover': host + page.thumb.url, 'time': page.time_display.strftime( '%Y-%m-%d' ), 'content': page.content })
	result = {'data': data}
	return HttpResponse(json.dumps(result), content_type='application/json')
