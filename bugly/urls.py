# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-09-09

from django.urls import path, re_path, include
from bugly import views


urlpatterns = [
	path('bugly/crash/webhook/', views.bugly_data),
]
