# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-03-03 03:10
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('favourite', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoritepage',
            name='created_time',
        ),
        migrations.RemoveField(
            model_name='favoritepage',
            name='last_modified',
        ),
        migrations.RemoveField(
            model_name='favoritevrmode',
            name='created_time',
        ),
        migrations.RemoveField(
            model_name='favoritevrmode',
            name='last_modified',
        ),
    ]
