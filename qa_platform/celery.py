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

app.conf.update(
    CELERYBEAT_SCHEDULE={
        'sonar-report': {
            'task': 'mypro.tasks.saveJenkinsData',
            'schedule': crontab(hour=23, minute=30, day_of_week="sunday"),
        }
    },
    result_expires=604800
)