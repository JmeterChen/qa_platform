from django.test import TestCase
from mypro.common.func import ding_push

# Create your tests here.

data = {
	"eventType": "bugly_crash_trend",
	"timestamp": 1462780713515,
	"isEncrypt": 0,
	"eventContent": {
		"datas": [
			{
				"accessUser": 12972,
				"crashCount": 21,
				"crashUser": 20,
				"version": "1.2.3",
				"url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
			},
			{
				"accessUser": 15519,
				"crashCount": 66,
				"crashUser": 64,
				"version": "1.2.4",
				"url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
			},
			{
				"accessUser": 15120,
				"crashCount": 1430,
				"crashUser": 1423,
				"version": "1.2.5",
				"url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
			},
			{
				"accessUser": 15420,
				"crashCount": 140,
				"crashUser": 123,
				"version": "1.2.6",
				"url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
			},
			{
				"accessUser": 2599,
				"crashCount": 140,
				"crashUser": 1230,
				"version": "1.2.7",
				"url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
			},
			{
				"accessUser": 100000,
				"crashCount": 140,
				"crashUser": 123,
				"version": "1.2.8",
				"url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
			}
		],
		"appId": "1104512706",
		"platformId": 1,
		"appName": "AF",
		"date": "20160508",
		"appUrl": "http://bugly.qq.com/issueIndex?app=1104512706&pid=1&ptag=1005-10000"
	},
	"signature": "ACE346A4AE13A23A52A0D0D19350B466AF51728A"
}

datas = [
	{
		"accessUser": 12972,
		"crashCount": 21,
		"crashUser": 20,
		"version": "1.2.3",
		"url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
	},
	{
		"accessUser": 15519,
		"crashCount": 66,
		"crashUser": 64,
		"version": "1.2.4",
		"url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
	},
	{
		"accessUser": 15120,
		"crashCount": 1430,
		"crashUser": 1423,
		"version": "1.2.5",
		"url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
	},
	{
		"accessUser": 15420,
		"crashCount": 140,
		"crashUser": 123,
		"version": "1.2.6",
		"url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
	},
	{
		"accessUser": 2599,
		"crashCount": 140,
		"crashUser": 1230,
		"version": "1.2.7",
		"url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
	},
	{
		"accessUser": 100000,
		"crashCount": 140,
		"crashUser": 123,
		"version": "1.2.8",
		"url": "http://bugly.qq.com/realtime?app=1104512706&pid=1&ptag=1005-10003&vers=0.0.0.12.12&time=last_7_day&tab=crash"
	}
]

# res = sorted(datas, key=lambda keys: keys["accessUser"])
# print(res)
# res2 = sorted(datas, key=lambda keys: keys["crashUser"] / keys["accessUser"], reverse=True)
# print(res2)
data["eventContent"]["datas"] = sorted(data["eventContent"]["datas"],
                                       key=lambda keys: keys["crashUser"] / keys["accessUser"],
                                       reverse=True)[:5] if len(data["eventContent"]["datas"]) > 5 else sorted(
	data["eventContent"]["datas"], key=lambda keys: keys["crashUser"] / keys["accessUser"], reverse=True)

# print(data)
print(ding_push(data))
