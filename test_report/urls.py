# -*- coding=utf-8 -*-
from django.urls import path
from test_report import views


urlpatterns = [
    path('add_report/', views.add_report),
    path('get_reports/', views.get_reports),
    path('delete_report/', views.delete_report),
    path('update_report/', views.update_report)
]
