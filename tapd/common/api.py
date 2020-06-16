# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-06-11

"""接受 tapd 中转服务提供接口
"""

import requests
import base64
from jsonpath import jsonpath


api_user = 'vP3^rsNM'
api_password = 'F23DD8F2-0EAE-F59B-09BC-78CECCDFC214'
user_password = (api_user + ':' +api_password)
user_BASE64 = base64.b64encode(user_password.encode()).decode()
headers = {"Authorization": "Basic " + user_BASE64}


def get_work_detial_by_id(pro_id, obj_id):
	"""
	:param pro_id:      项目ID
	:param obj_id:      工作ID，缺陷ID，需求ID或任务ID等；
	:return:            指定项目下的工作对象详情；
	"""
	url = 'https://api.tapd.cn/bugs'
	r = requests.get(url=url + f'?workspace_id={pro_id}&id={obj_id}', headers=headers)
	if r.status_code == 200:
		r_data = r.json()
	else:
		r_data = {}
	return r_data


def get_users_by_proId(pro_id, *args):
	"""
	:param pro_id:      # 项目ID
	:param args:        # 其他参数
	:return:            # 返回指定项目的成员信息
	"""
	url = 'https://api.tapd.cn/workspaces/users'
	if not args:
		r = requests.get(url=url + f'?workspace_id={pro_id}', headers=headers)
	else:
		# print(url + f'?workspace_id={pro_id}&fields=' + ','.join(args))
		r = requests.get(url=url + f'?workspace_id={pro_id}&fields=' + ','.join(args), headers=headers)
	if r.status_code == 200:
		r_data = r.json()
	else:
		r_data = {}
	return r_data


def get_usersList(userStr) -> list:
	"""
	:param userStr:  人名字符串
	:return:
	"""
	currentOwnerList = userStr.split(';') if userStr.__contains__(';') else [userStr]
	OwnerList = list(filter(None, currentOwnerList))
	return OwnerList


def get_user_email_by_name(pro_id, OwnerList) -> list:
	"""
	:param pro_id:      # 项目ID
	:param OwnerList:   # 处理人name
	:return:            # 处理人房多多邮箱账号
	"""
	res = get_users_by_proId(pro_id, "user", "email")
	data_list = jsonpath(res, "$..UserWorkspace")
	if len(OwnerList) == 1:
		for i in data_list:
			if i["user"] == OwnerList[0]:
				return [i["email"]]
	else:
		email_list = []
		for m in OwnerList:
			for i in data_list:
				if i["user"] == m:
					email_list.append(i["email"])
		return email_list


if __name__ == '__main__':
	project_id = 60765812
	work_id = 1160765812001017396
	# # print(get_user_email_by_name(project_id, "文建"))
	# data = get_work_detial_by_id(project_id, work_id).get("data", {}).get("Bug", {})
	# print(data)
	# get_work_detial_by_id(project_id, work_id).get("data", {}).get("Bug", {})
	# current_owner = get_usersList(data.get("current_owner"))
	# print(current_owner)
	# email = get_user_email_by_name(project_id, current_owner)
	# print(email)
	print(get_users_by_proId(project_id, "email", "user"))
	
	# project_id = 40618851
	# work_id = 1140618851001017847
	# data = get_work_detial_by_id(project_id, work_id).get("data", {}).get("Bug", {})
	# print(data)
	# userStr = data.get("current_owner")
	# userList = get_usersList(userStr)
	# print(userList)
	# emailList = get_user_email_by_name(project_id, userList)
	# print(emailList)
	# print(get_users_by_proId(project_id))