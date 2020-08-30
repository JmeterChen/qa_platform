import json
from django.http import JsonResponse
from django.shortcuts import render
from tapd.common.api import *
from tapd.models import *
from django.db.models import Q

from tapd.common.dingDing import *
from datetime import datetime
from tapd import logger
from rest_framework import response, serializers
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from mypro.models import *
import time
# Create your views here.

url_NF = 'http://ddcorp.dc.fdd/robot/send?'  # 智敏的服务
default_pageNum = '1'
default_pageSize = '10'


def get_tapd_data(request):
	data_dict = json.loads(request.body)
	logger.debug(f"请求操作            :腾讯发起操作")
	logger.debug(f"请求参数            :{data_dict}")
	# 从请求中获取请求参数
	event = data_dict.get("event")
	if event == 'bug::create':
		projectId = data_dict.get("workspace_id")
		workId = data_dict.get("id")
		
		# 获取新建的工作对象详情
		data = get_work_detail_by_id(projectId, workId).get("data", {}).get("Bug", {})
		currentOwner = data.get("current_owner")  # 当前处理人 可能是多个；
		
		OwnerList = get_usersList(currentOwner)
		emailList = get_user_email_by_name(projectId, OwnerList)  # 拿到邮箱
		
		logger.debug(f"发送对象            :{emailList}")
		# 调用
		code = push_ding(emailList, content=data, projectId=projectId, workId=workId)
		if code == 200:
			res = {"code": code, "success": True, "msg": "钉钉消息发送成功！", "data": data_dict}
			logger.debug(f"发送状态            :✅")
		else:
			res = {"code": code, "success": False, "msg": "钉钉消息发送失败！", "data": data_dict}
			logger.debug(f"发送状态            :❌")
	else:
		res = {"code": 201, "success": "suspend", "msg": "创建BUG以外的事件不做处理！"}
		logger.debug(f"发送状态            :push终止！")
	return JsonResponse(res)


def token_add(request):
	data_dict = json.loads(request.body)
	logger.debug(f"请求操作            :添加")
	logger.debug(f"请求参数            :{data_dict}")
	projectName = data_dict.get("projectName")
	# print(projectName)
	projectId = data_dict.get("projectId")
	# 将钉钉的token转换成智敏服务链接
	robotToken = url_NF + data_dict.get("robotToken").split('robot/send?')[-1]
	userName = data_dict.get("userName")
	
	if projectName and projectId and robotToken and userName:
		# p = ProjectToken.objects.filter(projectName=projectName)
		p_id = ProjectToken.objects.filter(projectId=projectId)
		if not p_id.exists():
			try:
				ProjectToken.objects.create(**{"projectName": projectName, "projectId": projectId, "robotToken": robotToken,
				                            "userName": userName})
				logger.debug(f"数据写入状态         :✅")
				res = {'code': 200, 'msg': '新增项目配置成功！', 'data': data_dict}
			except Exception as e:
				res = {"code": 99999, 'msg': f"添加数据出现异常：{e}"}
				logger.debug(f"数据写入状态         :❌")
		else:
			res = {'code': 10001, 'msg': '项目ID已经存在，请前往TAPD确认正确的项目参数！'}
	else:
		res = {'code': 10003, 'msg': '缺少必填参数！'}
	return JsonResponse(res)


def tokens(request):
	users = ProjectToken.objects.all().values("projectName", "projectId", "robotToken", "userName")
	return render(request, 'tapd/token.html', {"userList": list(users)})


def tokens_api(request):
	users = ProjectToken.objects.all().values("projectName", "projectId", "robotToken", "sys_time", "userName")
	return JsonResponse(list(users), safe=False)


def del_token(request):
	del_data = json.loads(request.body)
	logger.debug(f"请求操作            :删除")
	logger.debug(f"请求参数            :{del_data}")
	projectId = del_data.get("projectId")
	try:
		ProjectToken.objects.filter(projectId=projectId).delete()
		res = {"code": 200, "success": True, 'msg': "删除数据成功"}
		logger.debug(f"数据删除状态         :✅")
	except Exception as e:
		res = {"code": 99999, "success": False,  'msg': f"删除数据出现异常：{e}"}
		logger.debug(f"数据删除状态         :❌")
	return JsonResponse(res)
	

def search(request):
	logger.debug(f"请求操作            :搜索")
	keyword = request.GET.get("keyword")
	logger.debug(f"请求参数            :{keyword}")
	if keyword:
		p = ProjectToken.objects.filter(Q(projectName__icontains=keyword) | Q(userName__icontains=keyword) |
		                                Q(projectId__icontains=keyword)).values(
			"projectName", "projectId", "robotToken", "userName"
		)
	else:
		p = ProjectToken.objects.all().values("projectName", "projectId", "robotToken", "userName")
	return JsonResponse({"projects": list(p)})


def updateToken(request):
	data_dict = json.loads(request.body)
	logger.debug(f"请求操作            :更新")
	logger.debug(f"请求参数            :{data_dict}")
	projectName = data_dict.get('projectName')
	projectId = data_dict.get("projectId")
	# robotToken = data_dict.get("robotToken")
	# 将钉钉的token转换成智敏服务链接
	robotToken = url_NF + data_dict.get("robotToken").split('robot/send?')[-1]
	try:
		ProjectToken.objects.filter(projectId=projectId).update(projectName=projectName, robotToken=robotToken, sys_time=datetime.now())
		res = {"code": 200, 'msg': "数据更新成功", "data": data_dict}
		logger.debug(f"数据写入状态         :✅")
	except Exception as e:
		res = {"code": 99999, "msg": f"数据更新出现异常：{e}"}
		logger.debug(f"数据写入状态         :❌")
	return JsonResponse(res)


class TokenSerializers(serializers.ModelSerializer):
	class Meta:
		model = ProjectToken
		# fields = "__all__"
		exclude = ['create_time', 'sys_time']


class Paginator(PageNumberPagination):
	# 默认每页显示的数据条数
	page_size = 10
	
	# 获取URL参数中的设置页数
	page_query_param = 'page_number'
	# 获取URL参数中的设置的每页显示数据条数
	page_size_query_param = 'page_size'
	# 最大支持的每页显示的条数
	max_page_size = 20
	
	
class Tokens(APIView):
	def get(self, request, *args, **kwargs):
		keyword = request.GET.get("keyword")
		if keyword:
			token_list = ProjectToken.objects.filter(Q(projectName__icontains=keyword) | Q(userName__icontains=keyword) |
			                                Q(projectId__icontains=keyword)).order_by("create_time")
		else:
			token_list = ProjectToken.objects.all().order_by("create_time")
		# 计算产品线个数
		total = token_list.count()
		# 创建分页对象实例
		paginator = Paginator()
		page_app_list = paginator.paginate_queryset(token_list, self.request, view=self)
		page_number = request.GET.get("page_number", 1)
		page_size = request.GET.get("page_size", paginator.page_size)
		# 对数据序列化
		result = TokenSerializers(instance=page_app_list, many=True)
		return response.Response({
			"code": 1000,
			"success": True,
			"page_number": int(page_number),
			"page_size": int(page_size),
			"total": total,
			"data": result.data
		})
	
	def post(self, request, *args, **kwargs):
		req_data = json.loads(request.body)
		req_data["robotToken"] = url_NF + req_data.get("robotToken").split('robot/send?')[-1]
		check_data = TokenSerializers(data=req_data)
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
		token = ProjectToken.objects.filter(projectId=req_data.get("projectId")).first()
		req_data["robotToken"] = url_NF + req_data.get("robotToken").split('robot/send?')[-1]
		if not token:
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": "请确认选项是否存在！"
			})
		check_data = TokenSerializers(instance=token, data=req_data)
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
		
	# delete 方法好像存在 bug 获取 token 列表 get 接口的时候也会触发这个接口
	def delete(self, request, *args, **kwargs):
		req_data = request.GET
		app = ProjectToken.objects.filter(projectId=req_data.get("projectId")).first()
		if not app:
			return JsonResponse({
				"code": 90000,
				"success": False,
				"msg": "请确认选项是否存在！"
			})
		else:
			app.delete()
			return response.Response({
				"code": 10000,
				"success": True,
				"msg": "删除成功！"
			})