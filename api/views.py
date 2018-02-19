# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import simplejson as json
from vrmode.models import VRMode, VRBanner
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
