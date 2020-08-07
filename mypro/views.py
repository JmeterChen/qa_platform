
from django.shortcuts import render
from django.http import Http404, HttpResponse, JsonResponse, QueryDict
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.utils.decorators import method_decorator
import json
import datetime
from django.views import View
from rest_framework.views import APIView
from mypro.models import *
import time, random
from datetime import datetime

# Create your views here.


@csrf_exempt
def hours_ahead(request, offset):
	try:
		offset = int(offset)
	except ValueError:
		raise Http404()
	dt = datetime.datetime.now() + datetime.timedelta(hours=offset)
	html = f"In {offset} hour(s), it will be {str(dt).split('.')[0]}"
	return HttpResponse(html)


@csrf_exempt
# @csrf_protect
def get_year(request, year):
	return HttpResponse(f"Hello this Year is {year}！")


def test_extra(request, year):
	return HttpResponse(f"Hello this Year is {year}！")


def user_list(request):
	userList = ["kobe", "chenBoLin"]
	return HttpResponse(json.dumps(userList))


# class StudentView(View):
#
# 	@method_decorator(csrf_exempt)
# 	def dispatch(self, request, *args, **kwargs):
# 		return super(StudentView, self).dispatch(request, *args, **kwargs)
#
# 	def get(self, requests, *args, **kwargs):
# 		return HttpResponse("GET")
#
# 	def post(self, requests, *args, **kwargs):
# 		return HttpResponse("POST")
#
# 	def put(self, requests, *args, **kwargs):
# 		return HttpResponse("PUT")
#
# 	def delete(self, requests, *args, **kwargs):
# 		return HttpResponse("DELETE")

@method_decorator(csrf_exempt, name='dispatch')
class StudentView(View):
	def get(self, requests, *args, **kwargs):
		return HttpResponse("GET")
	
	def post(self, requests, *args, **kwargs):
		return HttpResponse("POST")
	
	def put(self, requests, *args, **kwargs):
		return HttpResponse("PUT")
	
	def delete(self, requests, *args, **kwargs):
		return HttpResponse("DELETE")


# 普通格式编写 views 函数
def get_order(request):
	orders = Orders.objects.all().values("orderId", "orderName", "money", "status", "createUserName")
	return JsonResponse(list(orders), safe=False)
	# return HttpResponse("获取订单")


def post_order(request):
	# return HttpResponse("创建订单")
	resquest_data = json.loads(request.body)
	dataId = str(round(time.time())) + str(random.randint(1, 100))
	# resquest_data = request.POST.get("name")
	# # return JsonResponse(resquest_data, safe=False)
	# print(type(resquest_data))
	# return HttpResponse(resquest_data)
	resquest_data["orderId"] = dataId
	Orders.objects.create(**resquest_data)
	return JsonResponse(resquest_data, safe=False)


def put_order(request):
	resquest_data = json.loads(request.body)
	objId = resquest_data.get("orderId")
	Orders.objects.filter(orderId=objId).update(**resquest_data, sys_time=datetime.now())
	return JsonResponse(resquest_data, safe=False)


def delete_order(request):
	resquest_data = json.loads(request.body)
	objId = resquest_data.get("orderId")
	Orders.objects.filter(orderId=objId).delete()
	return HttpResponse("删除订单")


# 基于 FBV 编写 views 函数
def orders(request):
	if request.method == 'GET':
		return HttpResponse("获取订单")
	elif request.method == 'POST':
		return HttpResponse("创建订单")
	elif request.method == 'PUT':
		return HttpResponse("修改订单")
	elif request.method == 'DELETE':
		return HttpResponse("删除订单")


# 基于 CBV 编写 views 函数
class OrderView(View):
	def get(self, requests, *args, **kwargs):
		return HttpResponse("获取订单", status=201)
	
	def post(self, requests, *args, **kwargs):
		return HttpResponse("创建订单")
	
	def put(self, requests, *args, **kwargs):
		return HttpResponse("修改订单")
	
	def delete(self, requests, *args, **kwargs):
		return HttpResponse("删除订单")


class DogView(APIView):
	def get(self, requests, *args, **kwargs):
		res = {
			"code": 1000,
			"msg": "xxxx"
		}
		return HttpResponse(json.dumps(res), status=201)
	
	def post(self, requests, *args, **kwargs):
		return HttpResponse("创建dog")
	
	def put(self, requests, *args, **kwargs):
		return HttpResponse("修改dog")
	
	def delete(self, requests, *args, **kwargs):
		return HttpResponse("删除dog")