# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-08-24

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qa_platform.settings')

# 创建celery实例
app = Celery('celery_sonar')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
# 在django中创建celery的命名空间
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
# 自动加载任务
app.autodiscover_tasks()
app.conf.timezone = 'Asia/Shanghai'

app.conf.update(
    CELERYBEAT_SCHEDULE={
        'sonar-report_week': {
            'task': 'mypro.tasks.saveJenkinsData',
            'schedule': crontab(hour=23, minute=45, day_of_week="sunday"),
            "args": ()
        },
	    'sonar-report_31': {
		    'task': 'mypro.tasks.saveJenkinsData',
		    'schedule': crontab(month_of_year="1,3,5,7,8,10,12", day_of_month=26, hour=23, minute=30),
		    "args": (1,)
	    },
	    'sonar-report_30': {
		    'task': 'mypro.tasks.saveJenkinsData',
		    'schedule': crontab(month_of_year="4,6,9,11", day_of_month=30, hour=23, minute=30),
		    "args": (1,)
	    },
	    'sonar-report_28': {
		    'task': 'mypro.tasks.saveJenkinsData',
		    'schedule': crontab(month_of_year="2", day_of_month=28, hour=23, minute=30),
		    "args": (1,)
	    },
	    # TODO  why add day_of_month don't work？
        'sonar-report_month': {
            'task': 'mypro.tasks.saveJenkinsData',
            'schedule': crontab(minute=45, hour=23, day_of_month='26'),
            "args": (1,)
        },
    },
    result_expires=604800
)