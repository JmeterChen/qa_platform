import json
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from tapd.common.api import *
from tapd.models import *
from django.db.models import Q

from tapd.common.dingDing import *
from datetime import datetime
from tapd.common.readLogger import ReadLogger

# Create your views here.

url_NF = 'http://ddcorp.dc.fdd/robot/send?'  # 智敏的服务

logger = None


def init_logger():
	global logger
	logger = ReadLogger().get_logger()


def get_tapd_data(request):
	if not logger:
		init_logger()
	data_dict = json.loads(request.body)
	logger.debug(f"请求操作            :腾讯发起操作")
	logger.debug(f"请求参数            :{data_dict}")
	# 从请求中获取请求参数
	event = data_dict.get("event")
	if event == 'bug::create':
		projectId = data_dict.get("workspace_id")
		workId = data_dict.get("id")
		
		# 获取新建的工作对象详情
		data = get_work_detial_by_id(projectId, workId).get("data", {}).get("Bug", {})
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
	if not logger:
		init_logger()
	users = ProjectToken.objects.all().values("projectName", "projectId", "robotToken", "userName")
	return render(request, 'tapd/token.html', {"userList": list(users)})


def tokens_api(request):
	if not logger:
		init_logger()
	users = ProjectToken.objects.all().values("projectName", "projectId", "robotToken", "sys_time", "userName")
	return JsonResponse(list(users), safe=False)


def del_token(request):
	del_data = json.loads(request.body)
	logger.debug(f"请求操作            :删除")
	logger.debug(f"请求参数            :{del_data}")
	projectId = del_data.get("projectId")
	try:
		ProjectToken.objects.filter(projectId=projectId).delete()
		res = {"code": 200, 'msg': "删除数据成功"}
		logger.debug(f"数据删除状态         :✅")
	except Exception as e:
		res = {"code": 99999, 'msg': f"删除数据出现异常：{e}"}
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