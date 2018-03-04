# -*- coding: utf-8 -*-
from django.db import models
from vrauth.models import string_with_title
from DjangoUeditor.models import UEditorField
from common.utils.images import get_image, uuid_image_path, uuid_vrzip_path
from vrauth.models import VRAuth

def vrmode_img_path(instance, filename):
    return uuid_image_path(filename, 'vrmode/')

def vrbanner_img_path(instance, filename):
    return uuid_image_path(filename, 'vrbanner/')

def page_img_path(instance, filename):
    return uuid_image_path(filename, 'page/')

def vr_zip_path(instance, filename):
    return uuid_vrzip_path(filename, 'vrmode/')

PAGE_STATUS_ACTIVE = '2'
PAGE_STATUS = (
    ('1', u'草稿'),
    (PAGE_STATUS_ACTIVE, u'生效'),
)

class VRMode(models.Model):
    title = models.CharField(max_length=128, verbose_name=u'标题')
    intro = models.CharField(max_length=200, verbose_name=u'简介')
    tag1 = models.CharField(max_length=100, verbose_name=u'标记一', default='14')
    tag2 = models.CharField(max_length=100, verbose_name=u'标记二', default='MAR')
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

class PageType(models.Model):
    name = models.CharField(verbose_name=u'标题名称', max_length=128)
    status = models.CharField(u'状态', choices=PAGE_STATUS, default='1', max_length=1)
    order = models.PositiveIntegerField(u'排序', default=100, help_text=u'从小到大显示,相同顺序按照[显示发布时间]排序')

    class Meta:
        app_label = string_with_title('vrmode', u"页面管理")
        db_table = 'page_type'
        verbose_name_plural = verbose_name = u'页面类型'

    def __unicode__(self):
        return self.name

    __str__ = __unicode__

class Page(models.Model):
    title = models.CharField(verbose_name=u'标题', max_length=128)
    intro = models.CharField(max_length=200, verbose_name=u'摘要')
    thumb = models.ImageField(verbose_name=u'封面', upload_to=page_img_path, help_text=u'建议大小为815*400')
    slug = models.SlugField(verbose_name=u'唯一路径', max_length=254, unique=True)
    type = models.ForeignKey(PageType, related_name='page', verbose_name=u'页面类型')
    status = models.CharField(verbose_name=u'状态', choices=PAGE_STATUS, default='1', max_length=1)
    order = models.PositiveIntegerField(verbose_name=u'排序', default=100, help_text=u'从小到大显示,相同顺序按照[显示发布时间]排序')
    time_display = models.DateTimeField(verbose_name=u'显示发布时间')
    content = UEditorField(verbose_name=u'内容', width=600, height=300, toolbars="full", imagePath="course/ueditor/", filePath="course/ueditor/", upload_settings={"imageMaxSize":1204000},default='')
    view_times = models.IntegerField(default=0)
    zan_times = models.IntegerField(default=0)
    created_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)
    last_modified = models.DateTimeField(verbose_name=u'最近更新时间', auto_now=True)
    
    class Meta:
        app_label = string_with_title('vrmode', u"页面管理")
        db_table = 'page_static'
        verbose_name_plural = verbose_name = u'页面发布'

    def __unicode__(self):
        return self.title

    __str__ = __unicode__

class PageComment(models.Model):
    user = models.ForeignKey(VRAuth, verbose_name=u'用户', null=True)
    page = models.ForeignKey(Page, verbose_name=u'页面')
    text = models.TextField(verbose_name=u'评论内容')
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    parent = models.ForeignKey('self', default=None, blank=True, null=True,
                               verbose_name=u'引用')

    class Meta:
        app_label = string_with_title('vrmode', u"页面管理")
        verbose_name_plural = verbose_name = u'页面评论'
        db_table = 'page_comment'
        # app_label = string_with_title('vmaig_comments', u"评论管理")

    def __unicode__(self):
        return self.text

    __str__ = __unicode__

class VRBanner(models.Model):
    title = models.CharField(max_length=128, verbose_name=u'标题')
    intro = models.CharField(max_length=200, verbose_name=u'简介')
    cover = models.ImageField(verbose_name=u'封面', upload_to=vrbanner_img_path, help_text=u'轮播图片 640*320', null=False)
    vrlink = models.CharField(max_length=128, verbose_name=u'文章链接', null=True, blank=True)
    page = models.ForeignKey(Page, verbose_name=u'页面', null=True, blank=True)
    create_time = models.DateTimeField(verbose_name=u'创建时间', auto_now_add=True)

    class Meta:
        app_label = string_with_title('vrmode', u"页面管理")
        verbose_name_plural = verbose_name = u'首页轮播'
        ordering = ['-create_time']

    def __unicode__(self):
        return self.title

    __str__ = __unicode__

