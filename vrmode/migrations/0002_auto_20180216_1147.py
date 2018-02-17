# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import vrmode.models


class Migration(migrations.Migration):

    dependencies = [
        ('vrmode', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vrmode',
            name='vrlink',
            field=models.CharField(max_length=128, null=True, verbose_name='vr\u94fe\u63a5', blank=True),
        ),
        migrations.AddField(
            model_name='vrmode',
            name='vrzip',
            field=models.FileField(help_text='\u5982\u679c\u4fdd\u6301\u4e3a\u7a7a\uff0c\u8868\u793a\u53ea\u6709\u5c01\u9762\uff0c\u5426\u5219\u4e0a\u9762\u8bf7\u4e0a\u4f20vr\u538b\u7f29\u5305', upload_to=vrmode.models.vr_zip_path, null=True, verbose_name='vr\u6587\u4ef6\u538b\u7f29\u5305', blank=True),
        ),
        migrations.AlterField(
            model_name='vrmode',
            name='cover',
            field=models.ImageField(help_text='3D\u65b9\u6848\u5c01\u9762\u56fe\u7247 815*400', upload_to=vrmode.models.vrmode_img_path, verbose_name='\u5c01\u9762'),
        ),
    ]
