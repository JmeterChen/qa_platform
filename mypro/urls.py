# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-07-30


from django.urls import path, re_path, include
from mypro import views


url_extra = [
	path('test/', views.test_extra)
]

urlpatterns = [
	path('articles/<int:year>/', views.get_year),
	re_path(r'time/plus/(\d{1,2})/$', views.hours_ahead),
	path('extra/<int:year>/', include(url_extra)),
	path('users/', views.user_list),
	path('students/', views.StudentView.as_view()),
	path('get_order/', views.get_order),
	path('post_order/', views.post_order),
	path('put_order/', views.put_order),
	path('delete_order/', views.delete_order),
	path('orders/', views.orders),
	path('order/', views.OrderView.as_view()),
	path('dog/', views.DogView.as_view())
]
