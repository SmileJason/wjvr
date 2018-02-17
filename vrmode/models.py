# -*- coding: utf-8 -*-
from django.db import models
from vrauth.models import string_with_title
from common.utils.images import get_image, uuid_image_path, uuid_vrzip_path

def vrmode_img_path(instance, filename):
    return uuid_image_path(filename, 'vrmode/')

def vr_zip_path(instance, filename):
    return uuid_vrzip_path(filename, 'vrmode/')

class VRMode(models.Model):
    title = models.CharField(max_length=128, verbose_name=u'标题')
    intro = models.CharField(max_length=200, verbose_name=u'简介')
    cover = models.ImageField(verbose_name=u'封面', upload_to=vrmode_img_path, help_text=u'3D方案封面图片 815*400', null=False)
    vrzip = models.FileField(verbose_name=u'vr文件压缩包', upload_to=vr_zip_path, null=True, blank=True, help_text=u'如果保持为空，表示只有封面，否则上面请上传vr压缩包')
    vrlink = models.CharField(max_length=128, verbose_name=u'vr链接', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)

    class Meta:
        app_label = string_with_title('vrmode', u"页面管理")
        verbose_name_plural = verbose_name = u'3D方案'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.title

    __str__ = __unicode__
