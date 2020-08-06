# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-07-30


from django.urls import path, re_path, include
from mysite import views


url_extra = [
	path('test/', views.test_extra)
]

urlpatterns = [
	path('articles/<int:year>/', views.get_year),
	re_path(r'time/plus/(\d{1,2})/$', views.hours_ahead),
	path('extra/<int:year>/', include(url_extra)),
	path('users/', views.user_list),
	path('students/', views.StudentView.as_view())
]

