# -*- coding: utf-8 -*-
import os
import shutil
from django.shortcuts import render, get_object_or_404, redirect
from vrmode.models import VRMode, VRBanner
from common import LOG
from django.db import transaction

@transaction.atomic
def vrmode_delete(request, vrmode_id):
	vrmode = get_object_or_404(VRMode, id=vrmode_id)
	file = vrmode.cover.path
	vrzip = vrmode.vrzip
	# LOG.error(request.get_host())
	vrmode.delete()
	if os.path.exists(file):
		os.remove(file)
	if vrzip:
		file = vrzip.path
		if os.path.exists(file):
			os.remove(file)
		file = vrzip.path[:-4]
		if os.path.exists(file):
			shutil.rmtree(file)
	return redirect('/xadmin/vrmode/vrmode/')

@transaction.atomic
def vrbanner_delete(request, vrbanner_id):
	vrbanner = get_object_or_404(VRBanner, id=vrbanner_id)
	file = vrbanner.cover.path
	vrbanner.delete()
	if os.path.exists(file):
		os.remove(file)
	return redirect('/xadmin/vrmode/vrbanner/')

        		


