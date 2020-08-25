import json

from django.http import JsonResponse
from django.shortcuts import render

from rest_framework import response, serializers
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from mypro.models import *
import time


class AppSerializers(serializers.ModelSerializer):
	class Meta:
		model = App
		# fields = "__all__"
		fields = ["product_id", "product_name"]


class Paginator(PageNumberPagination):
	
	# 默认每页显示的数据条数
	page_size = 10
	
	# 获取URL参数中的设置页数
	page_query_param = 'page_number'
	# 获取URL参数中的设置的每页显示数据条数
	page_size_query_param = 'page_size'
	# 最大支持的每页显示的条数
	max_page_size = 20


class Apps(APIView):
	
	def get(self, request, *args, **kwargs):
		# 获取有效的产品线
		app_list = App.objects.filter(is_delete=0).order_by("create_time")
		# 计算产品线个数
		total = app_list.count()
		# 创建分页对象实例
		paginator = Paginator()
		page_app_list = paginator.paginate_queryset(app_list, self.request, view=self)
		page_number = request.GET.get("page_number", 1)
		page_size = request.GET.get("page_size", paginator.page_size)
		# 对数据序列化
		# result = AppSerializers(instance=page_app_list, many=True)
		result = AppSerializers(instance=page_app_list, many=True)

		return response.Response({
			"code": 1000,
			"success": True,
			"page_number": page_number,
			"page_size": page_size,
			"total": total,
			"data": result.data
		})
		
	def post(self, request, *args, **kwargs):
		req_data = json.loads(request.body)
		req_data["product_id"] = str(round(time.time()))[::-1][:-3]
		app = AppSerializers(data=req_data)
		if app.is_valid():
			app.save()
			return JsonResponse({
				"code": 10000,
				"success": True,
				"data": req_data
			})
		else:
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": app.errors
			})

	def put(self, request, *args, **kwargs):
		req_data = json.loads(request.body)
		app = App.objects.filter(pk=req_data.get("product_id"), is_delete=0).first()
		if not app:
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": "请确认该产品线是否存在！"
			})
		check_app = AppSerializers(instance=app, data=req_data)
		if check_app.is_valid():
			check_app.save()
			return JsonResponse({
				"code": 10000,
				"success": True,
				"data": req_data
			})
		else:
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": check_app.errors
			})
	
	def delete(self, request, *args, **kwargs):
		req_data = json.loads(request.body)
		app = App.objects.filter(pk=req_data.get("product_id"), is_delete=0).first()
		if not app:
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": "请确认该产品线是否存在!"
			})
		else:
			app.is_delete = 1
			app.save()
			return response.Response({
				"code": 10000,
				"success": True,
				"msg": "产品线删除成功!"
			})