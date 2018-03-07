# -*- coding: utf-8 -*-

import os
from django.core.files import File
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import simplejson as json
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from weixin import WXAPPAPI
from common.utils.wxcrypt import WXBizDataCrypt
# from datetime import datetime
from vrmode.models import VRMode, VRBanner, PageType, Page, PAGE_STATUS_ACTIVE, PageComment
from vrauth.models import VRAuth
from favourite.models import FavoritePage
from community.models import PublishType, Publish, PublishComment, PUBLISH_STATUS_ACTIVE, PublishImage
from django.contrib.auth.hashers import make_password
from common.utils.images import get_image, uuid_image_path
from common import LOG

def get_vrmodes(request):
	# LOG.error(request.get_host())
	host = request.get_host()
	page = int(request.GET.get('page', 1))
	if page < 1:
		page = 1
	size = int(request.GET.get('size', 5))
	if size < 1:
		size = 5
	vrmodes = VRMode.objects.all()[(page-1)*size:(page)*size]
	data = []
	for vr in vrmodes.all():
		data.append({'cover': 'https://'+host+vr.cover.url, 'title': vr.title, 'intro': vr.intro, 'vrlink': 'https://'+host+vr.vrlink, 'tag1': vr.tag1, 'tag2': vr.tag2})
	result = {'data': data}
	return HttpResponse(json.dumps(result), content_type='application/json')

def get_banners(request):
	host = request.get_host()
	banners = VRBanner.objects.all()[:4]
	data = []
	for vr in banners.all():
		obj = {'cover': 'https://'+host+vr.cover.url, 'title': vr.title, 'intro': vr.intro}
		if vr.vrlink:
			obj['vrlink'] = 'https://'+host+vr.vrlink
		if vr.page:
			obj['pageid'] = vr.page.id
			# data.append({'cover': 'https://'+host+vr.cover.url, 'title': vr.title, 'intro': vr.intro, 'vrlink': 'https://'+host+vr.vrlink})
		data.append(obj)
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
	openid = request.GET.get('openid', 'x')
	page = int(request.GET.get('page', 1))
	if page < 1:
		page = 1
	size = int(request.GET.get('size', 5))
	if size < 1:
		size = 1
	pages = Page.objects.filter(status=PAGE_STATUS_ACTIVE, type__id=type).order_by('order')[(page-1)*size:(page)*size]
	data = []
	for page in pages.all():
		fav = FavoritePage.objects.filter(page=page, user__openid=openid)[:1]
		if fav:
			data.append({'title': page.title, 'intro': page.intro, 'order': page.order, 'id': page.id, 'cover': 'https://'+host+page.thumb.url, 'time': page.time_display.strftime( '%Y-%m-%d' ), 'view_times': page.view_times, 'favourite': True})
		else:
			data.append({'title': page.title, 'intro': page.intro, 'order': page.order, 'id': page.id, 'cover': 'https://'+host+page.thumb.url, 'time': page.time_display.strftime( '%Y-%m-%d' ), 'view_times': page.view_times, 'favourite': False})
	result = {'data': data}
	return HttpResponse(json.dumps(result), content_type='application/json')

def get_pagedetail(request, page_id):
	page = get_object_or_404(Page, id=page_id)
	page.view_times += 1
	page.save()
	openid = request.GET.get('openid', 'x')
	fav = FavoritePage.objects.filter(page__id=page_id, user__openid=openid)[:1]
	if fav:
		result = {'title': page.title, 'content': page.content, 'viewtime': page.view_times, 'time': page.time_display.strftime( '%Y-%m-%d' ), 'favourite': True}
		return HttpResponse(json.dumps(result), content_type='application/json')
	else:
		result = {'title': page.title, 'content': page.content, 'viewtime': page.view_times, 'time': page.time_display.strftime( '%Y-%m-%d' ), 'favourite': False}
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
	nickname = request.POST['nickname']
	avatarurl = request.POST['avatarurl']
	if code:
		try:
			api = WXAPPAPI(appid=APP_ID, app_secret=APP_SECRET)
			session_info = api.exchange_code_for_session_key(code=code)
			session_key = session_info.get('session_key')
			openid = session_info.get('openid')
			if session_key:
				try:
					auth = VRAuth.objects.get(openid=openid)
					if auth:
						auth.wxcover = avatarurl
						auth.wxname = nickname
						auth.save()
					else:
						auth = VRAuth.objects.create(username=nickname, password=make_password('123456'), wxname=nickname, wxcover=avatarurl, openid=openid)
				except VRAuth.DoesNotExist:
					auth = VRAuth.objects.create(username=nickname, password=make_password('123456'), wxname=nickname, wxcover=avatarurl, openid=openid)
				result = {'status':0, 'msg': u'登录成功', 'code': code, 'session_key': session_key, 'openid': openid}
				return HttpResponse(json.dumps(result), content_type='application/json')
			else:
				result = {'status':-1, 'msg': u'无法获取session_key,登录失败'}
				return HttpResponse(json.dumps(result), content_type='application/json')
		except Exception, e:
			result = {'status':-1, 'msg': u'code参数不正确,登录失败.'+e.message}
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
		page_id = request.POST['index']
		page = Page.objects.get(id=page_id)
		text = request.POST['text']
		openid = request.POST['openid']
		name = request.POST['name']
		parent_id = request.POST['parentid']
		try:
			auth = VRAuth.objects.get(openid=openid)
			if auth:
				if parent_id:
					parent = PageComment.objects.get(id=parent_id)
					pageComment = PageComment.objects.create(user=auth, page=page, text=text, parent=parent)
					return HttpResponse(json.dumps({'status':0, 'msg': u'评论成功'}), content_type='application/json')
				else:
					pageComment = PageComment.objects.create(user=auth, page=page, text=text)
					return HttpResponse(json.dumps({'status':0, 'msg': u'评论成功'}), content_type='application/json')
			else:
				return HttpResponse(json.dumps({'status':-1, 'msg': u'没有对应的用户，评论失败'}), content_type='application/json')
		except VRAuth.DoesNotExist:
			return HttpResponse(json.dumps({'status':-1, 'msg': u'没有对应的用户，评论失败'}), content_type='application/json')
		# LOG.DEBUG('%d %s %s %s %d', page_id, text, openid, name, parent_id)
	except Page.DoesNotExist:
		return HttpResponse(json.dumps({'status':-1, 'msg': u'没有对应的页面，评论失败'}), content_type='application/json')

def get_page_comments(request):
	try:
		index = int(request.GET.get('page', 1))
		if index < 1:
			index = 1
		size = int(request.GET.get('size', 100))
		if size < 1:
			size = 100
		page_id = request.GET.get('page_id')
		page = Page.objects.get(id=page_id)
		comments = PageComment.objects.filter(page=page).order_by('-create_time')[(index-1)*size:(index)*size]
		data = []
		for comment in comments.all():
			commentdata = {'name': comment.user.wxname, 'cover': comment.user.wxcover, 'openid': comment.user.openid, 'text': comment.text, 'id': comment.id, 'create_time': comment.create_time.strftime( '%Y-%m-%d' ), 'parent': ''}
			if comment.parent:
				commentdata['parent']=comment.parent.user.wxname
			data.append(commentdata)
		result = {'status': 0, 'data': data}
		return HttpResponse(json.dumps(result), content_type='application/json')
	except Page.DoesNotExist:
		return HttpResponse(json.dumps({'status':-1, 'msg': u'没有对应的页面，评论失败'}), content_type='application/json')

def favourite_page(request):
	openid = request.GET.get('openid', 'x')
	page_id = request.GET.get('pageid', 0)
	try:
		page = Page.objects.get(id=page_id)
		try:
			fav = FavoritePage.objects.get(page=page, user__openid=openid)
			fav.delete()
			result = {'status': 0, 'msg': u'取消收藏', 'fav': False}
			return HttpResponse(json.dumps(result), content_type='application/json')
		except FavoritePage.DoesNotExist:
			user = VRAuth.objects.get(openid=openid)
			fav = FavoritePage.objects.create(page=page, user=user)
			result = {'status': 0, 'msg': u'收藏成功', 'fav': True}
			return HttpResponse(json.dumps(result), content_type='application/json')
	except Page.DoesNotExist:
		result = {'status': -1, 'msg': u'没有对应的页面，收藏失败'}
		return HttpResponse(json.dumps(result), content_type='application/json')

def get_favourite_pages(request):
	host = request.get_host()
	openid = request.GET.get('openid', 'x')
	favs = FavoritePage.objects.filter(user__openid=openid)
	data = []
	for fav in favs:
		data.append({'title': fav.page.title, 'intro': fav.page.intro, 'order': fav.page.order, 'id': fav.page.id, 'cover': 'https://'+host+fav.page.thumb.url, 'time': fav.page.time_display.strftime( '%Y-%m-%d' ), 'view_times': fav.page.view_times, 'favourite': True})
	result = {'status': 0, 'data': data}
	return HttpResponse(json.dumps(result), content_type='application/json')

def init_mine(request):
	openid = request.GET.get('openid', 'x')
	favs = FavoritePage.objects.filter(user__openid=openid)
	if favs:
		result = {'status': 0, 'length': len(favs)}
		return HttpResponse(json.dumps(result), content_type='application/json')
	else:
		result = {'status': 0, 'length': 0}
		return HttpResponse(json.dumps(result), content_type='application/json')

def init_publish(request):
	types = PublishType.objects.filter(status=PUBLISH_STATUS_ACTIVE).order_by('order')[:5]
	data = []
	for type in types:
		data.append({'id': type.id, 'name': type.name, 'order': type.order})
	publishs = Publish.objects.filter(type__status=PUBLISH_STATUS_ACTIVE)
	comments = PublishComment.objects.all()
	result = {'types': data, 'article_count': len(publishs), 'comment_count': len(comments)}
	return HttpResponse(json.dumps(result), content_type='application/json')

def get_publishs(request):
	host = request.get_host()
	type = request.GET.get('type')
	openid = request.GET.get('openid', '')
	page = int(request.GET.get('page', 1))
	if page < 1:
		page = 1
	size = int(request.GET.get('size', 5))
	if size < 1:
		size = 1
	publishs = []
	if openid != '':
		publishs = Publish.objects.filter(user__openid=openid, type__id=type).order_by('-create_time')[(page-1)*size:(page)*size]
	else :
		publishs = Publish.objects.filter(type__id=type).order_by('-create_time')[(page-1)*size:(page)*size]
	data = []
	for publish in publishs.all():
		comments = PublishComment.objects.filter(publish=publish)
		pdata = {'id': publish.id, 'title': publish.title, 'content': publish.content, 'username': publish.user.wxname, 'cover': publish.user.wxcover, 'pic1': '', 'pic2': '', 'pic3': '', 'pic4': '', 'time': publish.create_time.strftime( '%Y-%m-%d' )}
		if publish.pic1:
			pdata['pic1'] = 'https://'+host+publish.pic1.url
		if publish.pic2:
			pdata['pic2'] = 'https://'+host+publish.pic2.url
		if publish.pic3:
			pdata['pic3'] = 'https://'+host+publish.pic3.url
		if publish.pic4:
			pdata['pic4'] = 'https://'+host+publish.pic4.url
		data.append(pdata)
	result = {'data': data}
	return HttpResponse(json.dumps(result), content_type='application/json')

@csrf_exempt
@transaction.atomic
def image_upload(request):
    file = request.FILES['img_data']
    fname, ext = os.path.splitext(file.name)
    if ext.lower() not in ('.jpg', '.jpeg', '.png', '.bmp'):
        return HttpResponseBadRequest(f.name)
    new_image = PublishImage.objects.create(
                    file = File(file),
                )
    tmp = Image.open(new_image.file.path)
    ImageFile.MAXBLOCK = tmp.size[0] * tmp.size[1]
    tmp.save(new_image.file.path, quality=95, optimize=True)
    return HttpResponse(json.dumps({'status':0, 'src': new_image.file.url, 'msg': '', 'id': new_image.id}), content_type='application/json')

@transaction.atomic
def image_delete(request, image_id):
    image = get_object_or_404(PublishImage, id=image_id)
    file = image.file.path
    if os.path.exists(file):
        os.remove(file)
        image.delete()
        return HttpResponse(json.dumps({'status':0, 'message':'success', 'id': image_id}), content_type='application/json')
    else:
        return HttpResponse(json.dumps({'status':-1, 'message':'fail', 'id': image_id}), content_type='application/json')
