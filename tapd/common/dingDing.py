# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-06-11


import requests
from tapd.models import *

url0 = 'http://ddcorp.dc.fdd/robot/send?access_token=a3828e9a8a8ac0e4440e1326b32007d301d247a48c5390f98d9318612035e8c1'
url1 = 'http://ddcorp.dc.fdd/robot/send?access_token=7d3aa078cd4eef5682d64c1eecf94d584c8a9d9fbec64fe26f3ca51498df313d'


# 推送钉钉消息调用方法（消息内容@email）
def push_ding(emailList, content=None, project_id=None, work_id=None, **kwargs):
	"""
	:param emailList:       推送消息指定@对象，传入参数为 list对象，必填参数
	:param content:         推送消息内容，默认为None， 非必填
	:param project_id：     项目ID
	:param work_id:         对象ID，这里暂时为bugID
	:return:
	"""
	
	bugLink = f"https://www.tapd.cn/{project_id}/bugtrace/bugs/view?bug_id={work_id}"
	to_person = '@' + ' @'.join(emailList)
	
	if emailList:
		robot_body = {
			"msgtype": "text",
			"text": {
				"content": f'你有一个新BUG：{content.get("title")} \n {to_person} \n BUG来源: {content.get("lastmodify")} \n BUG处理人: {content.get("current_owner")} \n BUG链接: {bugLink}'
			},
			"at": {
				"atMobiles": emailList,
				"isAtAll": False
			}
			# "touser": mobile
		}
		robotUrl = ProjectToken.objects.filter(projectId=project_id).first().robotToken
		r = requests.post(robotUrl, json=robot_body)
		if r.status_code == 200:
			return r.status_code
	
	# if emailList:
	# 	robot_body = {
	# 			"msgtype": "markdown",
	# 			"markdown": {
	# 				"title": "测试BUG待处理",
	# 				"text": f'##### 你有一个新BUG：{content.get("title")} \n {to_person} \n  - bug来源: {content.get("lastmodify")} \n  - bug 处理人: {content.get("current_owner")} \n  - [bug链接: {bugLink[0:28]}...]({bugLink})'
	# 			},
	# 			"at": {
	# 				"atMobiles": emailList,
	# 				"isAtAll": False
	# 			}
	# 			# "touser": mobile
	# 		}
	#
	# 	url = ProjectToken.objects.filter(projectId=project_id).first().robotToken
	# 	r = requests.post(url, json=robot_body)
	# 	if r.status_code == 200:
	# 		return r.status_code
	# 	else:
	# 		return r.status_code

if __name__ == '__main__':
	project_id = 60765812
	url = ProjectToken.objects.filter(projectId=project_id).first().robotToken
	print(url)