# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-06-11


import requests


url = 'http://ddcorp.dc.fdd/robot/send?access_token=a3828e9a8a8ac0e4440e1326b32007d301d247a48c5390f98d9318612035e8c1'


# 推送钉钉消息调用方法（消息内容@email）
def push_ding(email, content=None):
	"""
	:param email:           推送消息指定@对象，传入参数为 list对象，必填参数
	:param content:         推送消息内容，默认为None， 非必填
	:return:
	"""
	if email:
		robot_body = {
			"msgtype": "text",
			"text": {
				"content": content
			},
			"at": {
				"atMobiles": email,
				"isAtAll": False
			}
			# "touser": mobile
		}
		
		r = requests.post(url, json=robot_body)
		if r.status_code == 200:
			return r.status_code