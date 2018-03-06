# -*- coding: utf-8 -*-
from django.db import models
from vrauth.models import string_with_title
from common.utils.images import get_image, uuid_image_path
from vrauth.models import VRAuth

def publish_img_path(instance, filename):
    return uuid_image_path(filename, 'publish/')

PUBLISH_STATUS_ACTIVE = '2'
PUBLISH_STATUS = (
    ('1', u'草稿'),
    (PUBLISH_STATUS_ACTIVE, u'生效'),
)

class PublishType(models.Model):
    name = models.CharField(verbose_name=u'标题名称', max_length=128)
    status = models.CharField(u'状态', choices=PUBLISH_STATUS, default='1', max_length=1)
    order = models.PositiveIntegerField(u'排序', default=100, help_text=u'从小到大显示,相同顺序按照[显示发布时间]排序')

    class Meta:
        verbose_name_plural = verbose_name = u'话题类型'

    def __unicode__(self):
        return self.name

    __str__ = __unicode__

class Publish(models.Model):
    title = models.CharField(max_length=128, verbose_name=u'标题')
    content = models.TextField(verbose_name=u'话题内容')
    type = models.ForeignKey(PublishType, verbose_name=u'话题类型', null=True, blank=True)
    user = models.ForeignKey(VRAuth, verbose_name=u'用户')
    pic1 = models.ImageField(verbose_name=u'话题配图1', upload_to=publish_img_path, help_text=u'话题配图 300*300', null=True, blank=True)
    pic2 = models.ImageField(verbose_name=u'话题配图2', upload_to=publish_img_path, help_text=u'话题配图 300*300', null=True, blank=True)
    pic3 = models.ImageField(verbose_name=u'话题配图3', upload_to=publish_img_path, help_text=u'话题配图 300*300', null=True, blank=True)
    pic4 = models.ImageField(verbose_name=u'话题配图4', upload_to=publish_img_path, help_text=u'话题配图 300*300', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)

    class Meta:
        verbose_name_plural = verbose_name = u'话题'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.title

    __str__ = __unicode__

class PublishComment(models.Model):
    user = models.ForeignKey(VRAuth, verbose_name=u'用户', null=True)
    publish = models.ForeignKey(Publish, verbose_name=u'话题')
    text = models.TextField(verbose_name=u'评论内容')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    parent = models.ForeignKey('self', default=None, blank=True, null=True,
                               verbose_name=u'引用')

    class Meta:
        verbose_name_plural = verbose_name = u'话题评论'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.text

    __str__ = __unicode__