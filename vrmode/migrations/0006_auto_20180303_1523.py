# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-03 07:23
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vrmode', '0005_vrbanner_page'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pagecomment',
            name='name',
        ),
        migrations.RemoveField(
            model_name='pagecomment',
            name='openid',
        ),
        migrations.AddField(
            model_name='pagecomment',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237'),
        ),
    ]
