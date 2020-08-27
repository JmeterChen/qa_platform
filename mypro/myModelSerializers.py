# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-08-27


from rest_framework import response, serializers
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from mypro.models import *


class GeneralPaginator(PageNumberPagination):
	# 默认每页显示的数据条数
	page_size = 10
	
	# 获取URL参数中的设置页数
	page_query_param = 'page_number'
	# 获取URL参数中的设置的每页显示数据条数
	page_size_query_param = 'page_size'
	# 最大支持的每页显示的条数
	max_page_size = 20


class AppSerializers(serializers.ModelSerializer):
	class Meta:
		model = App
		# fields = "__all__"
		fields = ["product_id", "product_name"]
		

class ProjectSerializers(serializers.ModelSerializer):
	product_name = serializers.SerializerMethodField("get_product_name")
	test_user_name = serializers.SerializerMethodField("get_test_user_name")
	
	class Meta:
		model = Project
		# fields = "__all__"
		fields = ["product_name", "product_id", "project_name", "project_id", "test_user_id", "test_user_name", "operator"]
	
	def get_product_name(self, obj):
		product_id = obj.product_id
		product_name = App.objects.filter(product_id=product_id).first().product_name
		return product_name
	
	def get_test_user_name(self, obj):
		user_id = obj.test_user_id
		user_name = User.objects.filter(user_id=user_id).first().user_name
		return user_name
		
		
class SonarSerializers(serializers.ModelSerializer):
	product_name = serializers.SerializerMethodField("get_product_name")
	project_name = serializers.SerializerMethodField("get_project_name")
	
	class Meta:
		model = SonarReport
		# fields = "__all__"
		# exclude = ["create_time", "update_time"]
		fields = ["product_name", "project_name", "sonar_bugs", "sonar_holes", "year", "month", "day", "is_month"]

	def get_product_name(self, obj):
		product_id = obj.product_id
		product_name = App.objects.filter(product_id=product_id).first().product_name
		return product_name
	
	def get_project_name(self, obj):
		project_id = obj.project_id
		project_name = Project.objects.filter(project_id=project_id).first().project_name
		return project_name