# -*- coding: utf-8 -*-

from django.conf.urls import url
from api.views import get_vrmodes, get_banners, get_pagetypes, get_pages, get_pagedetail, weixin_login, check_session, check_post, set_session, get_session, get_page_comments, add_page_comment, favourite_page, get_favourite_pages, init_mine, init_publish, get_publishs, image_upload, image_delete, add_publish


urlpatterns = [

    url(r'^getModes/$', get_vrmodes),

    url(r'^getBanners/$', get_banners),

    url(r'^getPageTypes/$', get_pagetypes),

    url(r'^getPages/$', get_pages),

    url(r'^getPageDetail/$', get_pagedetail),

    url(r'^pagedetail/(?P<page_id>\d+)/$', get_pagedetail),

    url(r'^weixinLogin/$', weixin_login),

    url(r'^checkSession/$', check_session),

    url(r'^checkPost/$', check_post),

    url(r'^setSession/$', set_session),

    url(r'^getSession/$', get_session),

    url(r'^getPageComments/$', get_page_comments),

    url(r'^addPageComment/$', add_page_comment),

    url(r'^favouritePage/$', favourite_page),

    url(r'^getFavouritePages/$', get_favourite_pages),

    url(r'^initMine/$', init_mine),

    url(r'^initPublish/$', init_publish),

    url(r'^getPublishs/$', get_publishs),

    url(r'^addPublish/$', add_publish),

    url(r'^imageupload/$', image_upload),

    url(r'^image/(?P<image_id>\d+)/delete/$', image_delete),

    # url(r'^addPublishComment/$', add_publish_comment),

    # url(r'^getPublishComments/$', get_publish_comments),

]