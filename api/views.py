# -*- coding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import simplejson as json
from django.views.decorators.csrf import csrf_exempt
from weixin import WXAPPAPI
from common.utils.wxcrypt import WXBizDataCrypt
# from datetime import datetime
from vrmode.models import VRMode, VRBanner, PageType, Page, PAGE_STATUS_ACTIVE, PageComment
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
		data.append({'cover': 'https://'+host+vr.cover.url, 'title': vr.title, 'intro': vr.intro, 'vrlink': 'https://'+host+vr.vrlink})
	result = {'data': data}
	return HttpResponse(json.dumps(result), content_type='application/json')

def get_banners(request):
	host = request.get_host()
	page = int(request.GET.get('page', 1))
	if page < 1:
		page = 1
	size = int(request.GET.get('size', 2))
	if size < 1:
		size = 1
	banners = VRBanner.objects.all()[(page-1)*size:(page)*size]
	data = []
	for vr in banners.all():
		data.append({'cover': 'https://'+host+vr.cover.url, 'title': vr.title, 'intro': vr.intro, 'vrlink': 'https://'+host+vr.vrlink})
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
		data.append({'title': page.title, 'intro': page.intro, 'order': page.order, 'id': page.id, 'cover': 'https://'+host+page.thumb.url, 'time': page.time_display.strftime( '%Y-%m-%d' ), 'view_times': page.view_times, 'zan_times': page.zan_times})
	result = {'data': data}
	return HttpResponse(json.dumps(result), content_type='application/json')

def get_pagedetail(request, page_id):
	page = get_object_or_404(Page, id=page_id)
	page.view_times += 1
	page.save()
	result = {'title': page.title, 'content': page.content, 'viewtime': page.view_times, 'time': page.time_display.strftime( '%Y-%m-%d' )}
	return HttpResponse(json.dumps(result), content_type='application/json')

APP_ID = 'wxe986c48a87b379cd'
APP_SECRET = 'b842244b87187fa7f98827619d5b3d4c'
WXAPP_APPID = 'wxe986c48a87b379cd'

# @csrf_exempt
# def weixin_login(request):
#     code = request.POST['code']
#     if not code:
#     	result = {'status':-1, 'msg': u'code参数不正确'}
#     	return HttpResponse(json.dumps(result), content_type='application/json')
#     if code:
# 		api = WXAPPAPI(appid=APP_ID, app_secret=APP_SECRET)
# 		session_info = api.exchange_code_for_session_key(code=code)
# 		# 获取session_info 后
# 		session_key = session_info.get('session_key')
# 		openid = session_info.get('openid')
# 		# crypt = WXBizDataCrypt(WXAPP_APPID, session_key)
# 		# encrypted_data 包括敏感数据在内的完整用户信息的加密数据
# 		# iv 加密算法的初始向量
# 		# 这两个参数需要js获取
# 		# user_info = crypt.decrypt(encrypted_data, iv)
# 		if session_key:
# 			request.session[code+'session_key'] = session_key
# 			request.session[code+'openid'] = openid
# 			# request.session.set_expiry(30*24*60*60)
# 			result = {'status':0, '_3rd_session': code, 'msg': u'登录成功'}
# 			return HttpResponse(json.dumps(result), content_type='application/json')
# 		else:
# 			result = {'status':-1, 'msg': u'登录失败'}
# 			return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
def weixin_login(request):
	code = request.POST['code']
	if code:
		try:
			api = WXAPPAPI(appid=APP_ID, app_secret=APP_SECRET)
			session_info = api.exchange_code_for_session_key(code=code)
			session_key = session_info.get('session_key')
			openid = session_info.get('openid')
			if session_key:
				result = {'status':0, 'msg': u'登录成功', 'code': code, 'session_key': session_key, 'openid': openid}
				return HttpResponse(json.dumps(result), content_type='application/json')
			else:
				result = {'status':-1, 'msg': u'无法获取session_key,登录失败'}
				return HttpResponse(json.dumps(result), content_type='application/json')
		except Exception, e:
			result = {'status':-1, 'msg': u'code参数不正确,登录失败'}
			return HttpResponse(json.dumps(result), content_type='application/json')
	else:
		result = {'status': -1, 'msg': u'code参数不正确,登录失败'}
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

# @csrf_exempt
def set_session(request):
	# code = request.POST['code']
	# value = request.POST['codevalue']
	code = request.GET.get('code')
	value = request.GET.get('codevalue')
	request.session[code+'session_key'] = value
	# request.session.set_expiry(30*24*60*60)
	return HttpResponse(json.dumps({'request': request.GET, 'session': request.session[code+'session_key']}), content_type='application/json')

# @csrf_exempt
def get_session(request):
	# code = request.POST['code']
	code = request.GET.get('code')
	# request.session[code+'session_key'] = 'AAAA'
	key = code+'session_key'
	# codevalue = request.session[key]
	codevalue = request.session.get(key, 'BBBB')
	# codevalue = request.session[code]
	return HttpResponse(json.dumps({'keys': request.session.keys(), 'codevalue': codevalue}), content_type='application/json')

@csrf_exempt
def add_page_comment(request):
	try:
		page_id = request.POST['pageid']
		page = Page.objects.get(id=page_id)
		text = request.POST['text']
		openid = request.POST['openid']
		name = request.POST['name']
		parent_id = request.POST['parentid']
		LOG.DEBUG('%d %s %s %s %d', page_id, text, openid, name, parent_id)
		if parent_id:
			parent = PageComment.objects.get(id=parent_id)
			pageComment = PageComment.objects.create(openid=openid, name=name, page=page, text=text, parent=parent)
			return HttpResponse(json.dumps({'status':0, 'msg': u'评论成功'}), content_type='application/json')
		else:
			pageComment = PageComment.objects.create(openid=openid, name=name, page=page, text=text)
			return HttpResponse(json.dumps({'status':0, 'msg': u'评论成功'}), content_type='application/json')
	except Page.DoesNotExist:
		return HttpResponse(json.dumps({'status':-1, 'msg': u'没有对应的页面，评论失败'}), content_type='application/json')

def get_page_comments(request):
	try:
		index = int(request.GET.get('page', 1))
		if index < 1:
			index = 1
		size = int(request.GET.get('size', 10))
		if size < 1:
			size = 10
		page_id = request.GET.get('page_id')
		page = Page.objects.get(id=page_id)
		comments = PageComment.objects.filter(page=page).order_by('-create_time')[(index-1)*size:(index)*size]
		data = []
		for comment in comments.all():
			commentdata = {'name': comment.name, 'text': comment.text, 'id': comment.id, 'create_time': comment.create_time.strftime( '%Y-%m-%d' ), 'parent': ''}
			if comment.parent:
				commentdata['parent']=comment.parent.name
			data.append(commentdata)
		result = {'status': 0, 'data': data}
		return HttpResponse(json.dumps(result), content_type='application/json')
	except Page.DoesNotExist:
		return HttpResponse(json.dumps({'status':-1, 'msg': u'没有对应的页面，评论失败'}), content_type='application/json')


