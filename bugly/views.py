from django.shortcuts import render
from django.http import JsonResponse
import json
from mypro.common.func import ding_push
# Create your views here.
from bugly.models import BuglyData
from bugly import tasks


def bugly_data(request):
	# return HttpResponse("Hello world!")
	try:
		req_data = json.loads(request.body)
		data_to_db = []
		row_data = req_data["eventContent"]["datas"]
		if row_data:
			for i in row_data:
				row = i.copy()
				row.update({"eventType": req_data.get("eventType"), "timestamp": req_data.get("timestamp"),
				            "signature": req_data.get("signature"),
				            "date": req_data.get("eventContent", {}).get("date"),
				            "appName": req_data.get("eventContent", {}).get("appName"),
				            "appId": req_data.get("eventContent", {}).get("appId"),
				            "appUrl": req_data.get("eventContent", {}).get("appUrl"),
				            "platformId": req_data.get("eventContent", {}).get("platformId")
				            })
				# print(row_data.index(i), row)
				data_to_db.append(row)
				# BuglyData.objects.create(**row)
		tasks.saveBuglyData.delay(data_to_db)
		res = {"code": 10000, "msg": "输入写入成功！", "success": True}
	except Exception as e:
		res = {"code": 90000, "msg": e, "success": False}
	return JsonResponse(res)