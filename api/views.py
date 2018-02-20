# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from weixin import WXAPPAPI
from common.utils.wxcrypt import WXBizDataCrypt
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

APP_ID = 'wxe986c48a87b379cd'
APP_SECRET = 'b842244b87187fa7f98827619d5b3d4c'
WXAPP_APPID = 'wxe986c48a87b379cd'

@csrf_exempt
def weixin_login(request):
    code = request.POST['code']
    if not code:
    	result = {'status':-1, 'msg': u'code参数不正确'}
    	return HttpResponse(json.dumps(result), content_type='application/json')
    if code:
		api = WXAPPAPI(appid=APP_ID, app_secret=APP_SECRET)
		session_info = api.exchange_code_for_session_key(code=code)
		# 获取session_info 后
		session_key = session_info.get('session_key')
		openid = session_info.get('openid')
		# crypt = WXBizDataCrypt(WXAPP_APPID, session_key)
		# encrypted_data 包括敏感数据在内的完整用户信息的加密数据
		# iv 加密算法的初始向量
		# 这两个参数需要js获取
		# user_info = crypt.decrypt(encrypted_data, iv)
		if session_key:
			request.session[code+'session_key'] = session_key
			request.session[code+'openid'] = openid
			request.session.set_expiry(30*24*60*60)
			result = {'status':0, '_3rd_session': code, 'msg': u'登录成功'}
			return HttpResponse(json.dumps(result), content_type='application/json')
		else:
			result = {'status':-1, 'msg': u'登录失败'}
			return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def check_session(request):
	code = request.POST['code']
	if code:
		session_key = request.session[code+'session_key']
		openid = request.session[code+'openid']
		# LOG.error(session_key)
		# LOG.error(openid)
		if session_key:
			result = {'status':0, 'msg': u'session有效'}
			return HttpResponse(json.dumps(result), content_type='application/json')
		else:
			result = {'status':-1, 'msg': u'session失效'}
			return HttpResponse(json.dumps(result), content_type='application/json')
	else:
		result = {'status':-1, 'msg': u'code参数不正确'}
		return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def check_post(request):
	return HttpResponse(json.dumps({'request': request.POST, 'code': request.POST['code']}), content_type='application/json')