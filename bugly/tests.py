from django.test import TestCase
from mypro.common.func import ding_push
import json
import pymysql
import pickle
import struct

# Create your tests here.

data_android = """{'eventType': 'bugly_crash_trend', 'timestamp': 1599700684892, 'isEncrypt': 0,
                'eventContent': {'date': '20200909', 'appName': '多多卖房', 'datas': [
	                {'crashCount': 1, 'crashUser': 1, 'accessUser': 8, 'accessCount': 375, 'version': '3.4.2',
	                 'url': 'https://bugly.qq.com/v2/crash-reporting/dashboard/5c82afbd34?pid=1&trendVersion=3.4.2&isRealTime=1'},
	                {'crashCount': 1, 'crashUser': 1, 'accessUser': 22, 'accessCount': 319, 'version': '4.0.2',
	                 'url': 'https://bugly.qq.com/v2/crash-reporting/dashboard/5c82afbd34?pid=1&trendVersion=4.0.2&isRealTime=1'},
	                {'crashCount': 1, 'crashUser': 1, 'accessUser': 273, 'accessCount': 2882, 'version': '4.12.0',
	                 'url': 'https://bugly.qq.com/v2/crash-reporting/dashboard/5c82afbd34?pid=1&trendVersion=4.12.0&isRealTime=1'},
	                {'crashCount': 15, 'crashUser': 13, 'accessUser': 3138, 'accessCount': 38488, 'version': '4.17.1',
	                 'url': 'https://bugly.qq.com/v2/crash-reporting/dashboard/5c82afbd34?pid=1&trendVersion=4.17.1&isRealTime=1'},
	                {'crashCount': 68, 'crashUser': 53, 'accessUser': 26891, 'accessCount': 258423, 'version': '4.18.0',
	                 'url': 'https://bugly.qq.com/v2/crash-reporting/dashboard/5c82afbd34?pid=1&trendVersion=4.18.0&isRealTime=1'},
	                {'crashCount': 12, 'crashUser': 4, 'accessUser': 24, 'accessCount': 563, 'version': '4.19.0',
	                 'url': 'https://bugly.qq.com/v2/crash-reporting/dashboard/5c82afbd34?pid=1&trendVersion=4.19.0&isRealTime=1'},
	                {'crashCount': 2, 'crashUser': 1, 'accessUser': 9, 'accessCount': 111, 'version': '4.3.5',
	                 'url': 'https://bugly.qq.com/v2/crash-reporting/dashboard/5c82afbd34?pid=1&trendVersion=4.3.5&isRealTime=1'},
	                {'crashCount': 1, 'crashUser': 1, 'accessUser': 62, 'accessCount': 667, 'version': '4.7.0',
	                 'url': 'https://bugly.qq.com/v2/crash-reporting/dashboard/5c82afbd34?pid=1&trendVersion=4.7.0&isRealTime=1'},
	                {'crashCount': 14, 'crashUser': 1, 'accessUser': 43, 'accessCount': 528, 'version': '4.7.1',
	                 'url': 'https://bugly.qq.com/v2/crash-reporting/dashboard/5c82afbd34?pid=1&trendVersion=4.7.1&isRealTime=1'}],
                                 'appId': '5c82afbd34',
                                 'appUrl': 'https://bugly.qq.com/v2/crash-reporting/dashboard/5c82afbd34?pid=1&from=webhook',
                                 'platformId': 1}, 'signature': 'E8E7D23A058386306ABF1C26001988968FABEF45'}"""

data_iso = """{'eventType': 'bugly_crash_trend', 'timestamp': 1599700227640, 'isEncrypt': 0,
            'eventContent': {'date': '20200909', 'appName': '多多网商_appStore', 'datas': [
	            {'crashCount': 11, 'crashUser': 9, 'accessUser': 1397, 'accessCount': 13865,
	             'version': '4.17.0%284.17.0%29',
	             'url': 'https://bugly.qq.com/v2/crash-reporting/dashboard/b026190ba2?pid=2&trendVersion=4.17.0%284.17.0%29&isRealTime=1'},
	            {'crashCount': 30, 'crashUser': 29, 'accessUser': 8461, 'accessCount': 68632,
	             'version': '4.18.0%284.18.0%29',
	             'url': 'https://bugly.qq.com/v2/crash-reporting/dashboard/b026190ba2?pid=2&trendVersion=4.18.0%284.18.0%29&isRealTime=1'}],
                             'appId': 'b026190ba2',
                             'appUrl': 'https://bugly.qq.com/v2/crash-reporting/dashboard/b026190ba2?pid=2&from=webhook',
                             'platformId': 2}, 'signature': 'D12CC6FEC6B1381FCF29C636432CB3B536B57D5C'}"""

# res = sorted(datas, key=lambda keys: keys["accessUser"])
# print(res)
# res2 = sorted(datas, key=lambda keys: keys["crashUser"] / keys["accessUser"], reverse=True)
# print(res2)
# data["eventContent"]["datas"] = sorted(data["eventContent"]["datas"],
#                                        key=lambda keys: keys["crashUser"] / keys["accessUser"],
#                                        reverse=True)[:5] if len(data["eventContent"]["datas"]) > 5 else sorted(
# 	data["eventContent"]["datas"], key=lambda keys: keys["version"], reverse=True)
# data_android["eventContent"]["datas"] = sorted(data_android["eventContent"]["datas"], key=lambda x: x["version"],
#                                                reverse=True)
#
# data_iso
# print(data_android)
# print(ding_push(data))
# print(str(data_android).replace("\'", '\"'))
# print(str(data_iso).replace("\'", '\"'))

mysql_config = {
	"host": "10.50.110.13",
	"user": "chenwenjian",
	"password": "6RWpoIA0fMMrVb48",
	"port": 3306,
	"database": "fdd_cat"
}

con = pymysql.connect(**mysql_config)
cur = con.cursor()
sql = """
select content from daily_report_content where report_id=728634;
"""
cur.execute(sql)
res = cur.fetchall()
cur.close()
print(type(res[0][0]))
result = res[0][0]  # bytes

# print(result.decode("utf-8"))
print(struct.unpack("17d", result[0:8*17]))
