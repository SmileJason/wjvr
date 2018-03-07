# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-06 02:57
from __future__ import unicode_literals

import community.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publish',
            name='pic1',
            field=models.ImageField(help_text='\u8bdd\u9898\u914d\u56fe 300*300', null=True, upload_to=community.models.publish_img_path, verbose_name='\u8bdd\u9898\u914d\u56fe1'),
        ),
        migrations.AddField(
            model_name='publish',
            name='pic2',
            field=models.ImageField(help_text='\u8bdd\u9898\u914d\u56fe 300*300', null=True, upload_to=community.models.publish_img_path, verbose_name='\u8bdd\u9898\u914d\u56fe2'),
        ),
        migrations.AddField(
            model_name='publish',
            name='pic3',
            field=models.ImageField(help_text='\u8bdd\u9898\u914d\u56fe 300*300', null=True, upload_to=community.models.publish_img_path, verbose_name='\u8bdd\u9898\u914d\u56fe3'),
        ),
        migrations.AddField(
            model_name='publish',
            name='pic4',
            field=models.ImageField(help_text='\u8bdd\u9898\u914d\u56fe 300*300', null=True, upload_to=community.models.publish_img_path, verbose_name='\u8bdd\u9898\u914d\u56fe4'),
        ),
        migrations.AlterField(
            model_name='publish',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237'),
        ),
    ]