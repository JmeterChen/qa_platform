# -*- coding=utf-8 -*-
# Author: Luo yuan
# @Date : 2020-08-14

from django.urls import path
from qualitydata import views

urlpatterns = [
    path('version_qualitydata/list/', views.IterableView.as_view()),
    path('version_qualitydata/add/', views.IterableView.as_view()),
    path('version_qualitydata/edit/', views.IterableView.as_view()),
]
