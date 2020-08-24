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

from problem_guide import views

urlpatterns = [
    path('add/', views.add_problem_guide),
    path('add-bat/', views.add_bat_problem_guide),
    path('edit/', views.edit_problem_guide),
    path('delete/', views.delete_problem_guide),
    path('search/', views.search_problem_guide),
]
