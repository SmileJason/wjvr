# -*- coding: utf-8 -*-
import os
import shutil
from django.shortcuts import render, get_object_or_404, redirect
from community.models import Publish
from common import LOG
from django.db import transaction

@transaction.atomic
def publish_delete(request, publish_id):
	publish = get_object_or_404(Publish, id=publish_id)
	if publish.pic1:
		file = publish.pic1.path
		if os.path.exists(file):
			os.remove(file)
	if publish.pic2:
		file = publish.pic2.path
		if os.path.exists(file):
			os.remove(file)
	if publish.pic3:
		file = publish.pic3.path
		if os.path.exists(file):
			os.remove(file)
	if publish.pic4:
		file = publish.pic4.path
		if os.path.exists(file):
			os.remove(file)
	publish.delete()
	return redirect('/xadmin/community/publish/')