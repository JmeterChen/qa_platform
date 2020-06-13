# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-06-11


"""PT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from tapd import views

urlpatterns = [
	path('tapd_data/', views.get_tapd_data),
	path('add_pro_token/', views.token_add),
	path('projects/', views.tokens),
	path('del_token/', views.del_token),
	path('search', views.search),
	path('update_projects/', views.updateToken)
]