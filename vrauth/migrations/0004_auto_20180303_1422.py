# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-03 06:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vrauth', '0003_auto_20180303_1421'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vrauth',
            name='wxcover',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u5fae\u4fe1\u5934\u50cf'),
        ),
        migrations.AlterField(
            model_name='vrauth',
            name='wxname',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='\u5fae\u4fe1\u540d\u79f0'),
        ),
    ]
