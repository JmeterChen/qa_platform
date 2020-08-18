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

from django.core import serializers
from tapd.models import *
from django.core.paginator import Paginator
from django.db.models import Q

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
# 	def get(self, request, *args, **kwargs):
# 		return HttpResponse("GET")
#
# 	def post(self, request, *args, **kwargs):
# 		return HttpResponse("POST")
#
# 	def put(self, request, *args, **kwargs):
# 		return HttpResponse("PUT")
#
# 	def delete(self, request, *args, **kwargs):
# 		return HttpResponse("DELETE")

# @method_decorator(csrf_exempt, name='dispatch')
# class StudentView(View):
# 	def get(self, request, *args, **kwargs):
# 		return HttpResponse("GET")
#
# 	def post(self, request, *args, **kwargs):
# 		return HttpResponse("POST")
#
# 	def put(self, request, *args, **kwargs):
# 		return HttpResponse("PUT")
#
# 	def delete(self, request, *args, **kwargs):
# 		return HttpResponse("DELETE")


class StudentView(View):
	
	def dispatch(self, request, *args, **kwargs):
		func = getattr(self, request.method.lower())
		print(dir(self))
		return func(request, *args, **kwargs)
	
	def get(self, request, *args, **kwargs):
		# return HttpResponse("GET")
		users = ProjectToken.objects.all().values("projectName", "projectId", "robotToken", "sys_time", "userName")
		return JsonResponse(list(users), safe=False)
	
	def post(self, request, *args, **kwargs):
		return HttpResponse("POST")
	
	def put(self, request, *args, **kwargs):
		return HttpResponse("PUT")
	
	def delete(self, request, *args, **kwargs):
		return HttpResponse("DELETE")
	
	def patch(self, request, *args, **kwargs):
		return HttpResponse("PATCH")


# # 普通格式编写 views 函数
# def get_order(request):
# 	orders = Orders.objects.all().values("orderId", "orderName", "money", "status", "createUserName")
# 	return JsonResponse(list(orders), safe=False)
# 	# return HttpResponse("获取订单")
#
#
# def post_order(request):
# 	# return HttpResponse("创建订单")
# 	resquest_data = json.loads(request.body)
# 	dataId = str(round(time.time())) + str(random.randint(1, 100))
# 	# resquest_data = request.POST.get("name")
# 	# # return JsonResponse(resquest_data, safe=False)
# 	# print(type(resquest_data))
# 	# return HttpResponse(resquest_data)
# 	resquest_data["orderId"] = dataId
# 	Orders.objects.create(**resquest_data)
# 	return JsonResponse(resquest_data, safe=False)
#
#
# def put_order(request):
# 	resquest_data = json.loads(request.body)
# 	objId = resquest_data.get("orderId")
# 	Orders.objects.filter(orderId=objId).update(**resquest_data, sys_time=datetime.now())
# 	return JsonResponse(resquest_data, safe=False)
#
#
# def delete_order(request):
# 	resquest_data = json.loads(request.body)
# 	objId = resquest_data.get("orderId")
# 	Orders.objects.filter(orderId=objId).delete()
# 	return HttpResponse("删除订单")


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
	def get(self, request, *args, **kwargs):
		return HttpResponse("获取订单", status=201)
	
	def post(self, request, *args, **kwargs):
		return HttpResponse("创建订单")
	
	def put(self, request, *args, **kwargs):
		return HttpResponse("修改订单")
	
	def delete(self, request, *args, **kwargs):
		return HttpResponse("删除订单")


class DogView(APIView):
	def get(self, request, *args, **kwargs):
		res = {
			"code": 1000,
			"msg": "xxxx"
		}
		return JsonResponse(res, status=201)
	
	def post(self, request, *args, **kwargs):
		return HttpResponse({"name": [111, 22], "num":24}, safe=True)
	
	def put(self, request, *args, **kwargs):
		return HttpResponse("修改dog")
	
	def delete(self, request, *args, **kwargs):
		return HttpResponse("删除dog")

# default conf
default_pageNum = 1
default_pageSize = 10


class ProductView(View):
	def get(self, request, *args, **kwargs):
		# data = App.objects.all().values("product_name", "product_id")
		db_data = App.objects.all().filter(is_delete=0).order_by("create_time")
		data_len = db_data.__len__()
		req = request.GET
		if not len(req):
			data = db_data
			result_data = serializers.serialize("json", data, ensure_ascii=False, fields={"product_id", "product_name"})
			res = {"code": 10000, "success": True, "data": result_data, "total": data_len}
			# res = serializers.serialize("json", data, fields={"create_time", "sys_time"})
			
		else:
			pageSize, pageNum = req.get("pageSize", default_pageSize), req.get("pageNum", default_pageNum)
			max_page = (data_len // int(pageSize)) + 2
			if int(pageNum) in range(1, max_page):
				paginator = Paginator(db_data, pageSize)
				data = paginator.get_page(pageNum)
				result_data = serializers.serialize("json", data, ensure_ascii=False, fields={"product_name", "is_delete"})
				res = {"code": 10000, "success": True, "pageNum": int(pageNum), "pageSize": int(pageSize), "data": result_data}
			else:
				res = {"code": 10009, "success": False, "msg": "查询数据不再查询范围！"}
		return JsonResponse(res)
	
	def post(self, request, *args, **kwargs):
		request_data = json.loads(request.body) if request.body else {}
		request_product_name = request_data.get("product_name")
		if not request_product_name:
			res = {"code": 10012, "success": False, "msg": "缺少必填参数！"}
		elif App.objects.filter(is_delete=0).filter(product_name=request_product_name):
			res = {"code": 10011, "success": False, "msg": "添加产品线失败，存在同名产品线！"}
		else:
			product_id = str(round(time.time()))
			try:
				data = {"product_id": product_id, "product_name": request_product_name, "create_time": datetime.now()}
				App.objects.create(**data)
				res = {"code": 10000, "success": True, "msg": "添加产品线成功！", "data": data}
			except Exception as e:
				res = {"code": 10008, "success": False, "msg": "添加产品线失败", "error_msg": e}
		return JsonResponse(res)
	
	def put(self, request, *args, **kwargs):
		request_data = json.loads(request.body)
		product_id, product_name = request_data.get("product_id"), request_data.get("product_name")
		if not App.objects.filter(product_id=product_id):
			res = {"code": 10007, "success": False, "msg": "编辑产品线失败，请确认该产品线是否存在！"}
		elif App.objects.filter(is_delete=0).filter(product_name=product_name):
			res = {"code": 10011, "success": False, "msg": "编辑产品线失败，存在同名产品线！"}
		else:
			try:
				App.objects.filter(product_id=product_id).update(product_name=product_name, update_time=datetime.now())
				request_data["update_time"] = datetime.now()
				res = {"code": 10000, "success": True, "msg": "编辑产品线成功！", "data": request_data}
			except Exception as e:
				res = {"code": 10006, "success": False, "msg": "编辑产品线失败", "error_msg": e}
		return JsonResponse(res)
	
	def delete(self, request, *args, **kwargs):
		request_data = json.loads(request.body)
		product_id = request_data.get("product_id")
		if not App.objects.filter(product_id=product_id):
			res = {"code": 10005, "success": False, "msg": "删除产品线失败，请确认该产品线是否存在！"}
		else:
			App.objects.filter(product_id=product_id).update(is_delete=1, update_time=datetime.now())
			res = {"code": 10000, "success": True, "msg": "删除产品线成功！"}
		return JsonResponse(res)


class ProjectView(View):
	def get(self, request, *args, **kwargs):
		# data = App.objects.all().values("product_name", "product_id")
		db_data = Project.objects.all().filter(is_delete=0).order_by("create_time")
		req = request.GET
		pageSize, pageNum = req.get("pageSize", default_pageSize), req.get("pageNum", default_pageNum)
		if req.get("product_id"):
			db_data = db_data.filter(product_id=req.get("product_id"))
		data_len = db_data.__len__()
		data = Paginator(db_data, pageSize).get_page(pageNum)
		result_data = serializers.serialize("json", data, fields={"project_name", "project_id", 'test_user_id', 'product_id'})
		dict_data = json.loads(result_data)
		for i in dict_data:
			i["fields"]["product_name"] = App.objects.filter(product_id=i["fields"]["product_id"]).first().product_name
			i["fields"]["test_user_name"] = User.objects.filter(user_id=i["fields"]["test_user_id"]).first().user_name
		result_data = json.dumps(dict_data, ensure_ascii=False)
		res = {"code": 10000, "success": True, "data": result_data, "total": data_len}
		return JsonResponse(res)
	
	def post(self, request, *args, **kwargs):
		request_data = json.loads(request.body) if request.body else {}
		project_name = request_data.get("project_name")
		if not project_name:
			res = {"code": 10012, "success": False, "msg": "缺少必填参数！"}
		elif Project.objects.filter(is_delete=0).filter(project_name=project_name):
			res = {"code": 10011, "success": False, "msg": "添加项目组失败，存在同名项目组！"}
		else:
			project_id = str(round(time.time()))[::-1][:-3]
			try:
				request_data["project_id"] = project_id
				Project.objects.create(**request_data)
				res = {"code": 10000, "success": True, "msg": "添加产品线成功！", "data": request_data}
			except Exception as e:
				res = {"code": 10008, "success": False, "msg": "添加项目组失败", "error_msg": e}
		return JsonResponse(res)
		
	def put(self, request, *args, **kwargs):
		request_data = json.loads(request.body) if request.body else {}
		req_project_id = request_data.get("project_id")
		if not req_project_id:
			res = {"code": 10012, "success": False, "msg": "缺少必填参数！"}
		else:
			product_id, test_user_id, project_name = request_data.get("product_id"), request_data.get("test_user_id"), request_data.get("project_name")
			db_data1 = Project.objects.filter(is_delete=0).filter(project_id=req_project_id)
			db_data2 = Project.objects.filter(is_delete=0).filter(~Q(project_id=req_project_id)).filter(project_name=project_name)
			if db_data2:
				res = {"code": 10013, "success": False, "msg": "编辑项目组失败，存在同名项目组！"}
			elif not db_data1:
				res = {"code": 10005, "success": False, "msg": "编辑项目组失败，请确认该项目组是否存在！"}
			else:
				try:
					db_data1.update(product_id=product_id, project_name=project_name, test_user_id=test_user_id, update_time=datetime.now())
					res = {"code": 10000, "success": True, "msg": "编辑项目组成功！", "data": request_data}
				except Exception as e:
					res = {"code": 10014, "success": False, "msg": "编辑项目组失败", "error_msg": e}
		return JsonResponse(res)
	
	def delete(self, request, *args, **kwargs):
		request_data = json.loads(request.body)
		project_id = request_data.get("project_id")
		if not project_id:
			res = {"code": 10012, "success": False, "msg": "缺少必填参数！"}
		elif not Project.objects.filter(project_id=project_id):
			res = {"code": 10005, "success": False, "msg": "删除项目组失败，请确认该项目组是否存在！"}
		else:
			try:
				Project.objects.filter(project_id=project_id).update(is_delete=1, update_time=datetime.now())
				res = {"code": 10000, "success": True, "msg": "删除项目组成功！"}
			except Exception as e:
				res = {"code": 10014, "success": False, "msg": "删除项目组失败", "error_msg": e}
		return JsonResponse(res)
	
	
class SonarView(View):
	def post(self, request, *args, **kwargs):
		pass
	
	def get(self, request, *args, **kwargs):
		db_data = SonarReport.objects.all().filter(is_delete=0).order_by("create_time")
		data_len = db_data.__len__()
		if not len(request.GET):
			data = Paginator(db_data, default_pageSize).get_page(default_pageNum)
			res = serializers.serialize("json", data)
			res = {"code": 10000, "success": True, "pageNum": default_pageNum, "pageSize": default_pageSize, data: res, "total": data_len}
		else:
			product_id, project_id, _time = request.GET.get("product_id", None), request.GET.get("project_id", None), request.GET.get("_time", None)
			req_list = list(filter(None, [product_id, project_id, _time]))
		pass


class ServicesView(View):
	def post(self, request, *args, **kwargs):
		req_data = json.loads(request.body)
		service_name, service_type, product_id, project_id, coder = req_data.get("service_name"), req_data.get(
			"service_type"), req_data.get("product_id"), req_data.get("project_id"), req_data.get("coder")
		if not (service_name and service_type and product_id and project_id and coder):
			res = {"code": 10012, "success": False, "msg": "缺少必填参数！"}
		elif Services.objects.filter(is_delete=0).filter(service_name=service_name):
			res = {"code": 10011, "success": False, "msg": "添加服务失败，存在同名服务！"}
		else:
			try:
				Services.objects.create(**req_data)
				res = {"code": 10000, "success": True, "msg": "添加服务成功！", "data": req_data}
			except Exception as e:
				res = {"code": 10014, "success": False, "msg": "添加服务失败", "error_msg": e}
		return JsonResponse(res)
	
	def get(self, request, *args, **kwargs):
		db_data = Services.objects.all().filter(is_delete=0).order_by("create_time")
		req = request.GET
		pageSize, pageNum = req.get("pageSize", default_pageSize), req.get("pageNum", default_pageNum)
		if req.get("product_id"):
			db_data = db_data.filter(product_id=req.get("product_id"))
		if req.get("project_id"):
			db_data = db_data.filter(project_id=req.get("project_id"))
			# TODO how to add attr to serializers obj ？
			# for i in data:
			# 	i.product_name = App.objects.filter(product_id=i.product_id).first().product_name
			# 	i.project_name = Project.objects.filter(project_id=i.project_id).first().project_name
			# 	i.test_user_name = User.objects.filter(user_id=i.test_user_id).first().user_name
		data_len = db_data.__len__()
		data = Paginator(db_data, pageSize).get_page(pageNum)
		result_data = serializers.serialize("json", data, ensure_ascii=False,
		                                    fields={"service_name", "service_type", "product_id", "project_id", "coder", "test_user_id"})

		dict_data = json.loads(result_data)
		for i in dict_data:
			i["fields"]["product_name"] = App.objects.filter(product_id=i["fields"]["product_id"]).first().product_name
			i["fields"]["project_name"] = Project.objects.filter(project_id=i["fields"]["project_id"]).first().project_name
			i["fields"]["test_user_name"] = User.objects.filter(user_id=i["fields"]["test_user_id"]).first().user_name
		result_data = json.dumps(dict_data, ensure_ascii=False)
		res = {"code": 10000, "success": True, "pageNum": default_pageNum, "pageSize": default_pageSize, "data": result_data, "total": data_len}
		return JsonResponse(res)
	
	def put(self, request, *args, **kwargs):
		req_data = json.loads(request.body)
		db_data = Services.objects.filter(is_delete=0)
		service_id, service_name, product_id, project_id = req_data.get("service_id"), req_data.get("service_name"), req_data.get("product_id"), req_data.get("project_id")
		
		if not service_id:
			res = {"code": 10012, "success": False, "msg": "缺少必填参数！"}
		else:
			db_data1 = db_data.filter(id=service_id)
			db_data2 = db_data.filter(~Q(id=service_id)).filter(Q(product_id=product_id), Q(project_id=project_id), Q(service_name=service_name))
			if not db_data1:
				res = {"code": 10005, "success": False, "msg": "编辑服务失败，请确认该服务是否存在！"}
			elif db_data2:
				res = {"code": 10013, "success": False, "msg": "编辑服务失败，同产品线同项目组存在同名服务！"}
			else:
				try:
					req_data.pop("service_id")
					req_data["update_time"] = datetime.now()
					db_data1.update(**req_data)
					res = {"code": 10000, "success": True, "msg": "编辑服务成功！", "data": req_data}
				except Exception as e:
					res = {"code": 10014, "success": False, "msg": "编辑服务失败", "error_msg": e}
		return JsonResponse(res)
			
	def delete(self, request, *args, **kwargs):
		request_data = json.loads(request.body)
		service_id = request_data.get("service_id")
		db_data = Services.objects.filter(is_delete=0)
		if not service_id:
			res = {"code": 10012, "success": False, "msg": "缺少必填参数！"}
		elif not db_data.filter(id=service_id):
			res = {"code": 10005, "success": False, "msg": "删除服务失败，请确认该项目组是否存在！"}
		else:
			try:
				db_data.filter(id=service_id).update(is_delete=1, update_time=datetime.now())
				res = {"code": 10000, "success": True, "msg": "删除项目组成功！"}
			except Exception as e:
				res = {"code": 10014, "success": False, "msg": "删除项目组失败", "error_msg": e}
		return JsonResponse(res)