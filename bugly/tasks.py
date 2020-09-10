# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-09-10

from celery import shared_task
from bugly.models import BuglyData


@shared_task
def saveBuglyData(data=None):
	if data and isinstance(data, list):
		for i in data:
			BuglyData.objects.create(**i)
		return True
	else:
		return False