from django.http import Http404, HttpResponse, JsonResponse
import datetime
import json
import time
from datetime import datetime
from urllib.parse import unquote
from django.core import serializers
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponse, JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from mypro.common.func import mondayOfWeek, sundayOfWeek, monthOfTime
from mypro import tasks
from mypro.myModelSerializers import GeneralPaginator, AppSerializers, ProjectSerializers, SonarSerializers, ServiceSerializers
from rest_framework import response
from mypro.models import *
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
		return func(request, *args, **kwargs)
	
	def get(self, request, *args, **kwargs):
		# return HttpResponse("GET")
		# users = ProjectToken.objects.all().values("projectName", "projectId", "robotToken", "sys_time", "userName")
		# return JsonResponse(list(users), safe=False)
		res = tasks.saveJenkinsData.delay()
		return JsonResponse({'status': 'successful', 'task_id': res.task_id})
	
	def post(self, request, *args, **kwargs):
		return HttpResponse("POST")
	
	def put(self, request, *args, **kwargs):
		return HttpResponse("PUT")
	
	def delete(self, request, *args, **kwargs):
		return HttpResponse("DELETE")
	
	def patch(self, request, *args, **kwargs):
		return HttpResponse("PATCH")


class ProductView(APIView):
	def get(self, request, *args, **kwargs):
		db_data = App.objects.filter(is_delete=0).order_by("-create_time")
		total = db_data.count()
		paginator = GeneralPaginator()
		page_app_list = paginator.paginate_queryset(db_data, self.request, view=self)
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
		HTTP_OPERATOR = request.META.get('HTTP_OPERATOR')
		req_data["operator"] = "Anonymous" if not HTTP_OPERATOR else unquote(HTTP_OPERATOR)
		req_data["product_id"] = str(round(time.time()))
		check_data = AppSerializers(data=req_data)
		if check_data.is_valid():
			check_data.save()
			return JsonResponse({
				"code": 10000,
				"success": True,
				"msg": "创建成功！",
				"data": req_data
			})
		else:
			msg = ''
			for i in check_data.errors.items():
				msg += i[0] + i[1][0]
				break
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": msg,
				"errorDetail": check_data.errors
			})
	
	def put(self, request, *args, **kwargs):
		req_data = json.loads(request.body)
		HTTP_OPERATOR = request.META.get('HTTP_OPERATOR')
		req_data["operator"] = "Anonymous" if not HTTP_OPERATOR else unquote(HTTP_OPERATOR)
		db_data = App.objects.filter(pk=req_data.get("product_id"), is_delete=0).first()
		if not db_data:
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": "请确认该产品线是否存在！"
			})
		check_data = AppSerializers(instance=db_data, data=req_data)
		if check_data.is_valid():
			check_data.save()
			return JsonResponse({
				"code": 10000,
				"success": True,
				"msg": "更新成功！",
				"data": req_data
			})
		else:
			msg = ''
			for i in check_data.errors.items():
				msg += i[0] + i[1][0]
				break
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": msg,
				"errorDetail": check_data.errors
			})
	
	def delete(self, request, *args, **kwargs):
		# req_data = json.loads(request.body)
		req_data = request.GET
		HTTP_OPERATOR = request.META.get('HTTP_OPERATOR')
		operator = "Anonymous" if not HTTP_OPERATOR else unquote(HTTP_OPERATOR)
		db_data_one = App.objects.filter(pk=req_data.get("product_id"), is_delete=0).first()
		if not db_data_one:
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": "请确认该产品线是否存在！"
			})
		else:
			db_data_one.is_delete = 1
			db_data_one.operator = operator
			db_data_one.save()
			return response.Response({
				"code": 10000,
				"success": True,
				"msg": "删除成功！"
			})


class ProjectView(APIView):
	def get(self, request, *args, **kwargs):
		db_data = Project.objects.filter(is_delete=0).order_by("-create_time")
		req = request.GET
		if req.get("product_id"):
			db_data = db_data.filter(product_id=req.get("product_id"))
		total = db_data.count()
		paginator = GeneralPaginator()
		page_app_list = paginator.paginate_queryset(db_data, self.request, view=self)
		page_number = request.GET.get("page_number", 1)
		page_size = request.GET.get("page_size", paginator.page_size)
		result = ProjectSerializers(instance=page_app_list, many=True)
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
		HTTP_OPERATOR = request.META.get('HTTP_OPERATOR')
		req_data["operator"] = "Anonymous" if not HTTP_OPERATOR else unquote(HTTP_OPERATOR)
		req_data["project_id"] = str(round(time.time()))[::-1][:-3]
		check_data = ProjectSerializers(data=req_data)
		if check_data.is_valid():
			check_data.save()
			return JsonResponse({
				"code": 10000,
				"success": True,
				"msg": "创建成功！",
				"data": req_data
			})
		else:
			msg = ''
			for i in check_data.errors.items():
				msg += i[0] + i[1][0]
				break
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": msg,
				"errorDetail": check_data.errors
			})
	
	def put(self, request, *args, **kwargs):
		req_data = json.loads(request.body)
		HTTP_OPERATOR = request.META.get('HTTP_OPERATOR')
		req_data["operator"] = "Anonymous" if not HTTP_OPERATOR else unquote(HTTP_OPERATOR)
		db_data = Project.objects.filter(pk=req_data.get("project_id"), is_delete=0).first()
		if not db_data:
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": "请确认该项目组是否存在！"
			})
		check_data = ProjectSerializers(instance=db_data, data=req_data)
		if check_data.is_valid():
			check_data.save()
			return JsonResponse({
				"code": 10000,
				"success": True,
				"msg": "更新成功！",
				"data": req_data
			})
		else:
			msg = ''
			for i in check_data.errors.items():
				msg += i[0] + i[1][0]
				break
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": msg,
				"errorDetail": check_data.errors
			})
	
	def delete(self, request, *args, **kwargs):
		# req_data = json.loads(request.body)
		req_data = request.GET
		HTTP_OPERATOR = request.META.get('HTTP_OPERATOR')
		operator = "Anonymous" if not HTTP_OPERATOR else unquote(HTTP_OPERATOR)
		db_data = Project.objects.filter(pk=req_data.get("project_id"), is_delete=0).first()
		if not db_data:
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": "请确认该项目组是否存在!"
			})
		else:
			db_data.is_delete = 1
			db_data.operator = operator
			db_data.save()
			return response.Response({
				"code": 10000,
				"success": True,
				"msg": "删除成功！"
			})


default_pageSize = 10
default_pageNum = 1


class ServicesView(View):
	def post(self, request, *args, **kwargs):
		req_data = json.loads(request.body)
		HTTP_OPERATOR = request.META.get('HTTP_OPERATOR')
		req_data["operator"] = "Anonymous" if not HTTP_OPERATOR else unquote(HTTP_OPERATOR)
		service_name, service_type, product_id, project_id, coder = req_data.get("service_name"), req_data.get(
			"service_type"), req_data.get("product_id"), req_data.get("project_id"), req_data.get("coder")
		if not (service_name and service_type and product_id and project_id and coder):
			res = {"code": 10012, "success": False, "msg": "缺少必填参数！"}
		# elif Services.objects.filter(is_delete=0).filter(service_name=service_name):
		# 	res = {"code": 10011, "success": False, "msg": "添加服务失败，存在同名服务！"}
		elif Services.objects.filter(is_delete=0, product_id=product_id, project_id=project_id, service_name=service_name):
			res = {"code": 10011, "success": False, "msg": "添加服务失败，同产品线同项目组存在同名服务！！"}
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
			if i["fields"]["test_user_id"]:
				i["fields"]["test_user_name"] = User.objects.filter(user_id=i["fields"]["test_user_id"]).first().user_name
		# result_data = json.dumps(dict_data, ensure_ascii=False)
		# print(type(result_data))
		res = {"code": 10000, "success": True, "pageNum": default_pageNum, "pageSize": default_pageSize, "data": dict_data, "total": data_len}
		return JsonResponse(res)
	
	def put(self, request, *args, **kwargs):
		req_data = json.loads(request.body)
		HTTP_OPERATOR = request.META.get('HTTP_OPERATOR')
		req_data["operator"] = "Anonymous" if not HTTP_OPERATOR else unquote(HTTP_OPERATOR)
		db_data = Services.objects.filter(is_delete=0)
		service_id, service_name, product_id, project_id = req_data.get("id"), req_data.get("service_name"), req_data.get("product_id"), req_data.get("project_id")
		
		if not service_id:
			res = {"code": 10012, "success": False, "msg": "缺少必填参数！"}
		else:
			db_data1 = db_data.filter(id=service_id)
			db_data2 = db_data.filter(~Q(id=service_id)).filter(product_id=product_id, project_id=project_id, service_name=service_name)
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
		# req_data = json.loads(request.body)
		req_data = request.GET
		service_id = req_data.get("id")
		HTTP_OPERATOR = request.META.get('HTTP_OPERATOR')
		operator = "Anonymous" if not HTTP_OPERATOR else unquote(HTTP_OPERATOR)
		db_data = Services.objects.filter(is_delete=0)
		if not service_id:
			res = {"code": 10012, "success": False, "msg": "缺少必填参数！"}
		elif not db_data.filter(id=service_id):
			res = {"code": 10005, "success": False, "msg": "删除服务失败，请确认该项目组是否存在！"}
		else:
			try:
				db_data.filter(id=service_id).update(is_delete=1, operator=operator, update_time=datetime.now())
				res = {"code": 10000, "success": True, "msg": "删除项目组成功！"}
			except Exception as e:
				res = {"code": 10014, "success": False, "msg": "删除项目组失败", "error_msg": e}
		return JsonResponse(res)
	
	
class ServicesViewApiView(APIView):
	def get(self, request, *args, **kwargs):
		db_data = Services.objects.filter(is_delete=0).order_by("-create_time")
		req = request.GET
		if req.get("product_id"):
			db_data = db_data.filter(product_id=req.get("product_id"))
		if req.get("project_id"):
			db_data = db_data.filter(project_id=req.get("project_id"))
		if req.get("service_type"):
			db_data = db_data.filter(service_type=req.get("service_type"))
		if req.get("test_user_id"):
			db_data = db_data.filter(test_user_id=req.get("test_user_id"))
		total = db_data.count()
		# 创建分页对象实例
		paginator = GeneralPaginator()
		page_app_list = paginator.paginate_queryset(db_data, self.request, view=self)
		page_number = request.GET.get("page_number", 1)
		page_size = request.GET.get("page_size", paginator.page_size)
		result = ServiceSerializers(instance=page_app_list, many=True)
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
		HTTP_OPERATOR = request.META.get('HTTP_OPERATOR')
		req_data["operator"] = "Anonymous" if not HTTP_OPERATOR else unquote(HTTP_OPERATOR)
		check_data = ServiceSerializers(data=req_data)
		if check_data.is_valid():
			data = check_data.save(**req_data)
			req_data["id"] = data.id
			return JsonResponse({
				"code": 10000,
				"success": True,
				"msg": "创建成功！",
				"data": req_data
			})
		else:
			msg = ''
			for i in check_data.errors.items():
				msg += i[0] + i[1][0]
				break
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": msg,
				"errorDetail": check_data.errors
			})
	
	def put(self, request, *args, **kwargs):
		req_data = json.loads(request.body)
		HTTP_OPERATOR = request.META.get('HTTP_OPERATOR')
		req_data["operator"] = "Anonymous" if not HTTP_OPERATOR else unquote(HTTP_OPERATOR)
		app = Services.objects.filter(pk=req_data.get("id"), is_delete=0).first()
		if not app:
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": "请确认该服务是否存在！"
			})
		check_data = ServiceSerializers(instance=app, data=req_data)
		if check_data.is_valid():
			check_data.save()
			return JsonResponse({
				"code": 10000,
				"success": True,
				"msg": "更新成功！",
				"data": req_data
			})
		else:
			msg = ''
			for i in check_data.errors.items():
				msg += i[0] + i[1][0]
				break
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": msg,
				"errorDetail": check_data.errors
			})
	
	def delete(self, request, *args, **kwargs):
		# req_data = json.loads(request.body)
		req_data = request.GET
		HTTP_OPERATOR = request.META.get('HTTP_OPERATOR')
		operator = "Anonymous" if not HTTP_OPERATOR else unquote(HTTP_OPERATOR)
		app = Services.objects.filter(pk=req_data.get("id"), is_delete=0).first()
		if not app:
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": "请确认该服务是否存在!"
			})
		else:
			app.is_delete = 1
			app.operator = operator
			# app.operator = operator
			app.save()
			return response.Response({
				"code": 10000,
				"success": True,
				"msg": "删除成功!"
			})


class SonarData(APIView):
	def get(self, request, *args, **kwargs):
		db_data = SonarReport.objects.order_by("-create_time")
		req = request.GET
		time_type = req.get("time_type")
		if req.get("product_id"):
			db_data = db_data.filter(product_id=req.get("product_id"))
		if req.get("project_id"):
			db_data = db_data.filter(project_id=req.get("project_id"))
		if time_type == "week":
			week_start, week_end = req.get("week_start", mondayOfWeek()) + ' 00:00:00.000000', req.get("week_end", sundayOfWeek()) + ' 23:59:59.999999'
			db_data = db_data.filter(is_month=0).filter(create_time__range=[week_start, week_end])
		elif time_type == "month":
			month_start, month_end = req.get("month_start", monthOfTime()[0]) + ' 00:00:00.000000', req.get("month_end", monthOfTime()[1]) + ' 23:59:59.999999'
			db_data = db_data.filter(is_month=1).filter(create_time__range=[month_start, month_end])
		total = db_data.count()
		# 创建分页对象实例
		paginator = GeneralPaginator()
		page_result_list = paginator.paginate_queryset(db_data, self.request, view=self)
		page_number = req.get("page_number", 1)
		page_size = req.get("page_size", paginator.page_size)
		result = SonarSerializers(instance=page_result_list, many=True)
		# data = Paginator(db_data, pageSize).get_page(pageNum)
		# result_data = serializers.serialize("json", data, ensure_ascii=False)
		# dict_data = json.loads(result_data)
		# for i in dict_data:
		# 	i["fields"]["product_name"] = App.objects.filter(product_id=i["fields"]["product_id"]).first().product_name
		# 	i["fields"]["project_name"] = Project.objects.filter(project_id=i["fields"]["project_id"]).first().project_name
		# 	i["fields"]["count_time"] = f'{i["fields"]["create_time"].split("T")[0]}'
		# # result_data = json.dumps(dict_data, ensure_ascii=False)
		# res = {"code": 10000, "success": True, "pageNum": default_pageNum, "pageSize": default_pageSize, "data": dict_data, "total": data_len}
		return response.Response({
			"code": 1000,
			"success": True,
			"page_number": page_number,
			"page_size": page_size,
			"total": total,
			"data": result.data
		})


