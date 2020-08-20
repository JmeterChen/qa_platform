# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-08-19


from datetime import datetime
import pymysql, os
from conf.config import db_mysql


def get_week_of_month(year, month, day):
	"""
	获取指定的某天是某个月中的第几周
	周一作为一周的开始
	"""
	end = int(datetime(year, month, day).strftime("%W"))
	begin = int(datetime(year, month, 1).strftime("%W"))
	return end - begin + 1


def get_year_month_week_day_byString(time_str) ->tuple:
	"""
	:param time_str:        时间字符串如: '2020-08-20'
	:return:                tuple格式:  year, month, week, day
	"""
	time_list = list(map(lambda x: int(x), time_str.split("-")))
	time_tuple = datetime(time_list[0], time_list[1], time_list[2])
	end = int(time_tuple.strftime("%W"))
	begin = int(datetime(time_list[0], time_list[1], 1).strftime("%W"))
	week = end - begin + 1
	year = int(time_tuple.strftime("%Y"))
	month = int(time_tuple.strftime("%m"))
	day = int(time_tuple.strftime("%d"))
	return year, month, week, day


def execute_sql(sql):
	env = os.getenv('FDD_ENV')
	if env:
		_db = db_mysql[env]
	else:
		_db = db_mysql["test"]
	cur = pymysql.connect(**_db)
	cur = cur.cursor()
	cur.execute(sql)
	res = cur.fetchall()
	cur.close()
	return res


if __name__ == '__main__':
	_str = '2020-08-17'
	_str_list = list(map(lambda x: int(x), _str.split("-")))
	print(_str_list)
	print(get_week_of_month(_str_list[0], _str_list[1], _str_list[2]))