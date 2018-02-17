from django.conf.urls import include, url
from django.conf import settings
from django.contrib import admin
import xadmin

urlpatterns = [
    # Examples:
    # url(r'^$', 'wjvr.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),

    url(r'^xadmin/vrmode/vrmode/(?P<vrmode_id>\d+)/delete/$', 'vrmode.views.admindelete', name='vrmoade-admin-delete'),

    url(r'^xadmin/', xadmin.site.urls),
]

if settings.DEBUG:
    urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]
   
