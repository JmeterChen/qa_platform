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


def get_user_email_by_name(pro_id, name=None):
	"""
	:param pro_id:      # 项目ID
	:param name:        # 处理人name
	:return:            # 处理人房多多邮箱账号
	"""
	res = get_users_by_proId(pro_id, "user", "email")
	data_list = jsonpath(res, "$..UserWorkspace")
	for i in data_list:
		if i["user"] == name:
			return i["email"]


if __name__ == '__main__':
	project_id = 60765812
	print(get_user_email_by_name(project_id, "文建"))