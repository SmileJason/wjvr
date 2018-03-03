#coding: utf-8
from django.db import models

from vrauth.models import VRAuth
from vrmode.models import Page, VRMode

class string_with_title(str):
    def __new__(cls, value, title):
        instance = str.__new__(cls, value)
        instance._title = title
        return instance

    def title(self):
        return self._title

    __copy__ = lambda self: self
    __deepcopy__ = lambda self, memodict: self



class FavoritePage(models.Model):
    user = models.ForeignKey(VRAuth, verbose_name=u'用户')
    page = models.ForeignKey(Page, verbose_name=u'页面')
    
    class Meta:
    	string_with_title('favourite', u"收藏管理")
        db_table = 'favorite_page'
        verbose_name_plural = verbose_name = u'页面收藏'

    def __unicode__(self):
        return 'Fav #%d' % self.id


class FavoriteVRMode(models.Model):
    user = models.ForeignKey(VRAuth, verbose_name=u'用户')
    vrmode = models.ForeignKey(VRMode, verbose_name=u'VR场景')
    
    class Meta:
    	string_with_title('favourite', u"收藏管理")
        db_table = 'favorite_vrmode'
        verbose_name_plural = verbose_name = u'VR收藏'

    def __unicode__(self):
        return 'Fav #%d' % self.id