#coding: utf-8
from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
import xadmin

urlpatterns = [
    # Examples:
    # url(r'^$', 'wjvr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),

    url(r'^xadmin/vrmode/vrmode/(?P<vrmode_id>\d+)/delete/$', 'vrmode.views.vrmode_delete', name='vrmoade-admin-delete'),

    url(r'^xadmin/vrmode/vrbanner/(?P<vrbanner_id>\d+)/delete/$', 'vrmode.views.vrbanner_delete', name='vrbanner-admin-delete'),

    url(r'^xadmin/community/publish/(?P<publish_id>\d+)/delete/$', 'community.views.publish_delete', name='publish-admin-delete'),

    url(r'^xadmin/', xadmin.site.urls),

    url(r'^api/', include('api.urls')),

    # url(r'^ueditor/', include('DjangoUeditor.utils')),
    url(r'^ueditor/', include('DjangoUeditor.urls' )),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
   
