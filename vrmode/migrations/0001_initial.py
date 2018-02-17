# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import vrmode.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='VRMode',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=128, verbose_name='\u6807\u9898')),
                ('intro', models.CharField(max_length=200, verbose_name='\u7b80\u4ecb')),
                ('cover', models.ImageField(help_text='3D\u65b9\u6848\u5c01\u9762\u56fe\u7247', upload_to=vrmode.models.vrmode_img_path, verbose_name='\u5c01\u9762')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
            ],
            options={
                'ordering': ['-create_time'],
                'verbose_name': '3D\u65b9\u6848',
                'verbose_name_plural': '3D\u65b9\u6848',
            },
        ),
    ]
