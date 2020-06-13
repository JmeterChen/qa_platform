import json

from django.http import JsonResponse
from django.shortcuts import render

from index.models import *


# Create your views here.


def base(request):
	return render(request, 'index/base.html')


def hello(request):
	return render(request, 'index/hello.html')


def user_list(request):
	users = Users.objects.all()
	data_list = []
	for i in users:
		i_dict = {"id": i.id, "username": i.username, "phoneNumber": i.phoneNumber, "sex": "男" if i.sex == 1 else "女",
		          "email": i.email}
		data_list.append(i_dict)
	return JsonResponse(data_list, safe=False)


def user(request):
	users = Users.objects.all()
	userList = []
	for i in users:
		i_dict = {"id": i.id, "username": i.username, "phoneNumber": i.phoneNumber, "sex": "男" if i.sex == 1 else "女",
		          "email": i.email}
		userList.append(i_dict)
	return render(request, 'index/user.html', {"userList": userList})


def user_add(request):
	data_dict = json.loads(request.body)
	username = data_dict.get("username")
	print(username)
	phoneNumber = data_dict.get("phoneNumber")
	print(phoneNumber)
	email = data_dict.get("email")
	print(email)
	sex = 2 if data_dict.get("sex") == '女' else 1
	if username and phoneNumber and email:
		print(len(phoneNumber), email.__contains__("@"))
		if len(phoneNumber) == 11 and email.__contains__("@" and '.'):
			p = Users.objects.filter(phoneNumber=phoneNumber)
			e = Users.objects.filter(email=email)
			if not p.exists() and not e.exists():
				Users.objects.create(username=username, phoneNumber=phoneNumber, email=email, sex=sex)
				return JsonResponse({"code": 200, 'msg': '新增用户成功'})
			else:
				data = {'code': 10001,  'msg': '电话号码或者邮箱已存在！'}
		else:
			data = {'code': 10002, 'msg': '电话号码或邮箱格式不对！'}
	else:
		data = {'code': 10003, 'msg': '缺少必填参数！'}
	# return render(request, 'error.html', {"info": info})
	return JsonResponse(data)


def user_delete(request):
	pass




