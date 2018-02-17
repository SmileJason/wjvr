# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse
import simplejson as json
from vrmode.models import VRMode

def get_vrmodes(request):
	page = int(request.GET.get('page', 1))
	if page < 1:
		page = 1
	size = int(request.GET.get('size', 2))
	if size < 2:
		size = 2
	vrmodes = VRMode.objects.all()[(page-1)*size:(page)*size]
	data = []
	for vr in vrmodes.all():
		data.append({'cover': 'https://wjvr.json666.cn'+vr.cover.url, 'title': vr.title, 'intro': vr.intro, 'vrlink': 'https://wjvr.json666.cn'+vr.vrlink})
	result = {'data': data}
	return HttpResponse(json.dumps(result), content_type='application/json')
