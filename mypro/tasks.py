# -*- coding=utf-8 -*-
# Author: BoLin Chen
# @Date : 2020-08-24


import time
from jsonpath import jsonpath
from mypro.models import Services,SonarReport
from mypro.common.func import get_year_month_week_day_byString, execute_sql
from celery import shared_task


def getServiceDBData():
	db_data = Services.objects.filter(is_delete=0)
	res_data = []
	s_list = jsonpath(list(db_data.values("product_id").distinct()), expr="$..product_id")  # 拿到产品线
	for m in s_list:
		project_list = jsonpath(list(db_data.filter(product_id=m).values("project_id").distinct()), expr="$..project_id")  # 拿到产品线下对应的项目组
		for n in project_list:
			s_name_list = jsonpath(list(db_data.filter(product_id=m, project_id=n).values("service_name").distinct()), expr="$..service_name")
			res_data.append((m, n, s_name_list, len(s_name_list)))
	return res_data


@shared_task
def saveJenkinsData(tags=None):
	t = time.localtime()
	t_str = time.strftime('%Y-%m-%d', t)
	t_tuple = get_year_month_week_day_byString(t_str)
	s_tuple = getServiceDBData()
	for i in s_tuple:
		sql_template = f"""
			SELECT
			  COUNT(1),
			  CASE
				WHEN `issue_type` = 1
				THEN '异味'
				WHEN `issue_type` = 2
				THEN 'bugs'
				WHEN `issue_type` = 3
				THEN '漏洞'
				ELSE `issue_type`
			  END '问题类型'
			FROM
			  issues i
			WHERE i.`project_uuid` IN
				(SELECT
					project_uuid
				FROM
					projects p
				WHERE p.`name` IN
					{((i[2])[0], (i[2])[0]) if i[3]==1 else tuple(i[2])}
				)
			AND i.`status` = 'OPEN'
			GROUP BY i.`issue_type` ;
		"""
		sql_res = execute_sql(sql_template)
		data = {}
		for m in sql_res:
			data[m[1]] = m[0]
		if not tags:
			SonarReport.objects.create(product_id=i[0], project_id=i[1], service_num=i[3], sonar_holes=data.get("漏洞", 0),
			                           sonar_bugs=data.get("bugs", 0), year=t_tuple[0], month=t_tuple[1], week=t_tuple[2],
			                           day=t_tuple[3])
		else:
			SonarReport.objects.create(product_id=i[0], project_id=i[1], service_num=i[3], sonar_holes=data.get("漏洞", 0),
			                           sonar_bugs=data.get("bugs", 0), year=t_tuple[0], month=t_tuple[1], week=t_tuple[2],
			                           day=t_tuple[3], is_month=1)
