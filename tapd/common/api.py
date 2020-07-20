# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-06-11

"""接受 tapd 中转服务提供接口
"""

import requests
import base64
from jsonpath import jsonpath


apiUser = 'vP3^rsNM'
apiPassword = 'F23DD8F2-0EAE-F59B-09BC-78CECCDFC214'
userPassword = (apiUser + ':' + apiPassword)
userBASE64 = base64.b64encode(userPassword.encode()).decode()
headers = {"Authorization": "Basic " + userBASE64}


def get_work_detail_by_id(proId, objId):
	"""
	:param proId:      项目ID
	:param objId:      工作ID，缺陷ID，需求ID或任务ID等；
	:return:            指定项目下的工作对象详情；
	"""
	url = 'https://api.tapd.cn/bugs'
	r = requests.get(url=url + f'?workspace_id={proId}&id={objId}', headers=headers)
	if r.status_code == 200:
		r_data = r.json()
	else:
		r_data = {}
	return r_data


def get_users_by_proId(proId, *args):
	"""
	:param proId:      # 项目ID
	:param args:        # 其他参数
	:return:            # 返回指定项目的成员信息
	"""
	url = 'https://api.tapd.cn/workspaces/users'
	if not args:
		r = requests.get(url=url + f'?workspace_id={proId}', headers=headers)
	else:
		# print(url + f'?workspace_id={pro_id}&fields=' + ','.join(args))
		r = requests.get(url=url + f'?workspace_id={proId}&fields=' + ','.join(args), headers=headers)
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


def get_user_email_by_name(proId, OwnerList) -> list:
	"""
	:param proId:      # 项目ID
	:param OwnerList:   # 处理人name
	:return:            # 处理人房多多邮箱账号
	"""
	res = get_users_by_proId(proId, "user", "email")
	dataList = jsonpath(res, "$..UserWorkspace")
	if len(OwnerList) == 1:
		for i in dataList:
			if i["user"] == OwnerList[0]:
				return [i["email"]]
	else:
		emailList = []
		for m in OwnerList:
			for i in dataList:
				if i["user"] == m:
					emailList.append(i["email"])
		return emailList
	
	
def get_iterations_by_id(pro_id) -> dict:
	"""
	:param pro_id:      # 项目ID
	:return:            # 指定项目迭代信息
	"""
	url = 'https://api.tapd.cn/iterations'
	params = {"workspace_id": pro_id}
	res = requests.get(url=url, params=params, headers=headers)
	if res.status_code == 200:
		return res.json()


if __name__ == '__main__':
	projectId = 60765812
	work_id = 1160765812001017396
	# # print(get_user_email_by_name(project_id, "文建"))
	# data = get_work_detail_by_id(project_id, work_id).get("data", {}).get("Bug", {})
	# print(data)
	# get_work_detail_by_id(project_id, work_id).get("data", {}).get("Bug", {})
	# current_owner = get_usersList(data.get("current_owner"))
	# print(current_owner)
	# email = get_user_email_by_name(project_id, current_owner)
	print(get_users_by_proId(projectId, "email", "user"))
	
	# project_id = 40618851
	# work_id = 1140618851001017847
	# data = get_work_detail_by_id(project_id, work_id).get("data", {}).get("Bug", {})
	# print(data)
	# userStr = data.get("current_owner")
	# userList = get_usersList(userStr)
	# print(userList)
	# emailList = get_user_email_by_name(projectId, userList)
	# print(emailList)
	# print(get_users_by_proId(projectId))