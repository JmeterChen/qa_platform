# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-06-06

from django.urls import path, include, re_path
from index import views

urlpatterns = [
	path('app/', views.Apps.as_view())
]
