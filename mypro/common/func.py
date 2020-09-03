# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-08-19


from datetime import datetime, timedelta
import pymysql, os
from conf.config import db_mysql
import time, calendar


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
	_db = db_mysql["master"]
	cur = pymysql.connect(**_db)
	cur = cur.cursor()
	cur.execute(sql)
	res = cur.fetchall()
	cur.close()
	return res


def mondayOfWeek():
	"""
	:return:            获取本周周一日期
	"""
	dayOfWeek = datetime.now().isoweekday()
	nowDate = datetime.now()
	delta = timedelta(days=dayOfWeek - 1)
	monday = nowDate - delta
	return monday.strftime("%Y-%m-%d")


def sundayOfWeek():
	"""
	:return:            获取本周周日日期
	"""
	dayOfWeek = datetime.now().isoweekday()
	nowDate = datetime.now()
	delta = timedelta(days=7 - dayOfWeek)
	monday = nowDate + delta
	return monday.strftime("%Y-%m-%d")


def monthOfTime():
	day_now = time.localtime()
	day_begin = '%d-%02d-01' % (day_now.tm_year, day_now.tm_mon)
	wday, monthRange = calendar.monthrange(day_now.tm_year, day_now.tm_mon)
	day_end = '%d-%02d-%02d' % (day_now.tm_year, day_now.tm_mon, monthRange)
	return day_begin, day_end
	
	
if __name__ == '__main__':
	# _str = '2020-08-17'
	# _str_list = list(map(lambda x: int(x), _str.split("-")))
	# print(_str_list)
	# print(get_week_of_month(_str_list[0], _str_list[1], _str_list[2]))
	print(monthOfTime())