
from django.views import View
from mypro.models import Iterable,OnlineBug, App, Project,User
from django.http import JsonResponse
import json
from django.core import serializers
from django.core.paginator import Paginator
import time
import datetime
from django.db.models import Q
#
#
# def add(request):
#     if request.method == "POST":
#         data_dict = json.loads(request.body)
#         product_id = data_dict.get("productId")
#         project_id = data_dict.get("projectId")
#         publish_num = data_dict.get("publishNum")
#         cases_num = data_dict.get("casesNum")
#         bugs_num = data_dict.get("bugsNum")
#         test_user_id = data_dict.get("testUserId")
#         year = data_dict.get("year")
#         month = data_dict.get("month")
#         week = data_dict.get("week")
#         if product_id and project_id and publish_num and cases_num and bugs_num and test_user_id and year and month and week:
#             product_id_values = App.objects.filter(product_id=product_id)
#             project_id_values = Project.objects.filter(product_id=product_id,project_id=project_id)
#             if project_id_values:
#                 create_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#                 data = {"product_id": product_id, "project_id": project_id,
#                             "publish_num": publish_num,
#                             "cases_num": cases_num, "year": year, "month": month, "week": week,
#                             "bugs_num": bugs_num,
#                             "test_user_id": test_user_id, "create_time": create_time, "update_time": create_time,
#                             "is_delete": 0}
#                 print(data)
#                 save_data = Iterable.objects.create(**data)
#                 save_data.save()
#                 res = {"code": 20000, "success": True, "msg": "查询成功！", "data": data}
#                 print(res)
#             elif product_id_values:
#                 res = {"code": 10000, "success": True, "msg": "产品线与项目组不匹配", "data": ""}
#             else:
#                 res = {"code": 10000, "success": True, "msg": "不存在该产品线", "data": ""}
#         else:
#             res = {'code': 10003, 'msg': '请输入必填参数！'}
#         return JsonResponse(res)
#
#
# def edit(request):
#     if request.method == "PUST":
#         data_dict = json.loads(request.body)
#         id = data_dict.get("id")
#         product_id = data_dict.get("productId")
#         project_id = data_dict.get("projectId")
#         publish_num = data_dict.get("publishNum")
#         cases_num = data_dict.get("casesNum")
#         bugs_num = data_dict.get("bugsNum")
#         test_user_id = data_dict.get("testUserId")
#         year = data_dict.get("year")
#         month = data_dict.get("month")
#         week = data_dict.get("week")
#         if id and product_id and project_id and publish_num and cases_num and bugs_num and test_user_id and year and month and week:
#             if Iterable.objects.filter(id=id):
#                 update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#                 if Iterable.objects.filter(id=id):
#                     Iterable.objects.filter(id=id).update(product_id=product_id, project_id=project_id,
#                                                           publish_num=publish_num,
#                                                           cases_num=cases_num, bugs_num=bugs_num,
#                                                           test_user_id=test_user_id, year=year, month=month, week=week,
#                                                           update_time=update_time)
#             else:
#                 res = {'code': 10003, 'msg': '不存在该条数据！'}
#         else:
#             res = {'code': 10003, 'msg': '请输入必填参数！'}
#         return JsonResponse(res)
#
# @api_view(['GET', 'POST'])
# def iterable_list(request):
#     if request.method == 'GET':
#         snippets = Iterable.objects.all()
#         serializer = IterableSerializer(snippets, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = IterableSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def iterable_detail(request, pk):
#     """
#     snippet的读取, 更新 或 删除
#     """
#     try:
#         snippet = Iterable.objects.get(pk=pk)
#     except Iterable.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = IterableSerializer(snippet)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = IterableSerializer(snippet, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         snippet.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
default_pageNo = 1
default_pageSize = 10
time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


class IterableView(View):
    def get(self, request, *args, **kwargs):
        req = request.GET
        if not len(req):
            db_data = Iterable.objects.all().filter(is_delete=0).order_by("create_time")
            result_data = serializers.serialize("json", db_data)
            total = Paginator(result_data, default_pageSize).num_pages
            dict_data = json.loads(result_data)
            result_data_list = []
            for data1 in dict_data:
                data1["fields"]["product_name"] = App.objects.filter(
                    product_id=data1["fields"]["product_id"]).first().product_name
                data1["fields"]["project_name"] = Project.objects.filter(
                    project_id=data1["fields"]["project_id"]).first().project_name
                result_data_list.append(data1['fields'])
            res = {"code": 20000, "success": True, "data": {"pageData": result_data_list},
                   "pageInfo": {"pageNo": default_pageNo, "pageSize": default_pageSize, "total": total}}
        else:
            product_id, project_id, year, month, week, start_time, end_time = req.get('productId'), req.get(
                'projectId'), req.get('year'), req.get('month'), req.get('week'), req.get('startTime'), req.get(
                'endTime')
            page_size, page_no = req.get("pageSize", default_pageSize), req.get("pageNo", default_pageNo)
            if year is None and month:
                res = {"code": 10012, "success": False, "msg": "请选择年份！"}
            elif year is None and month is None and week:
                res = {"code": 10012, "success": False, "msg": "请选择年份和月份！"}
            else:
                if product_id:
                    db_data = Iterable.objects.filter(product_id=product_id, is_delete=0).order_by("create_time")
                if project_id:
                    db_data = Iterable.objects.filter(project_id=project_id, is_delete=0).order_by("create_time")
                if start_time and end_time:
                    db_data = Iterable.objects.filter(create_time=(start_time, end_time), is_delete=0).order_by("create_time")
                if year and week and month:
                    db_data = Iterable.objects.filter(year=year, month=month, week=week, is_delete=0).order_by("create_time")
                if year and month:
                    db_data = Iterable.objects.filter(year=year, month=month, is_delete=0).order_by("create_time")
                data = Paginator(db_data, page_size).get_page(page_no)
                total = Paginator(db_data, default_pageSize).num_pages
                result_data = serializers.serialize("json", data)
                dict_data = json.loads(result_data)
                result_data_list = []
                for data1 in dict_data:
                    data1["fields"]["product_name"] = App.objects.filter(product_id=data1["fields"]["product_id"]).first().product_name
                    data1["fields"]["project_name"] = Project.objects.filter(project_id=data1["fields"]["project_id"]).first().project_name
                    result_data_list.append(data1['fields'])
                res = {"code": 20000, "success": True, "data": {"pageData": result_data_list},
                       "pageInfo": {"pageNo": page_no, "pageSize": page_size, "total": total}}
        return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)

    def post(self, request, *args, **kwargs):
        req_data = json.loads(request.body)
        if req_data:
            product_id, project_id, publish_num, cases_num, bugs_num, test_user_id, year, month, week = req_data.get(
                "productId"), req_data.get("projectId"), req_data.get("publishNum"), req_data.get(
                "casesNum"), req_data.get("bugsNum"), req_data.get(
                "testUserId"), req_data.get("year"), req_data.get("month"), req_data.get("week")
            req_data["create_time"] = time
            if product_id and project_id and publish_num and cases_num and bugs_num and test_user_id and year and month and week:
                product_id_values = App.objects.filter(product_id=product_id).first()
                project_id_values = Project.objects.filter(product_id=product_id, project_id=project_id)
                if project_id_values:
                    try:
                        db_data = {"product_id": product_id, "project_id": project_id,
                                "publish_num": publish_num, "cases_num": cases_num, "year": year, "month": month,
                                "week": week, "bugs_num": bugs_num, "test_user_id": test_user_id,
                                "create_time": time, "update_time": time, "is_delete": 0}
                        data = Iterable.objects.create(**db_data)
                        data.save()
                        res = {"code": 20000, "success": True, "msg": "添加成功！", "data": db_data}
                    except Exception as e:
                        res = {"code": 10008, "success": False, "msg": e, "data": ""}
                elif product_id_values:
                    res = {"code": 10000, "success": True, "msg": "产品线与项目组不匹配", "data": ""}
                else:
                    res = {"code": 10000, "success": True, "msg": "不存在该产品线", "data": ""}
            else:
                res = {"code": 10012, "success": False, "msg": "缺少必填参数！", "data": ""}
        else:
            res = {"code": 10012, "success": False, "msg": "请求参数为空！", "data": ""}
        return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)

    def put(self, request, *args, **kwargs):
        req_data = json.loads(request.body)
        if req_data:
            req_id = req_data.get("id")
            if req_id:
                try:
                    id_data = Iterable.objects.filter(is_delete=0, id=req_id)
                    if id_data:
                        product_id, project_id, publish_num, cases_num, bugs_num, test_user_id, year, month, week = req_data.get(
                            "productId"), req_data.get("projectId"), req_data.get(
                            "publishNum"), req_data.get(
                            "casesNum"), req_data.get("bugsNum"), req_data.get(
                            "testUserId"), req_data.get("year"), req_data.get("month"), req_data.get("week")
                        if product_id and project_id and publish_num and cases_num and bugs_num and test_user_id and year and month and week:
                            try:
                                Iterable.objects.filter(id=req_id).update(product_id=product_id, project_id=project_id,
                                                                          publish_num=publish_num,
                                                                          cases_num=cases_num, bugs_num=bugs_num,
                                                                          test_user_id=test_user_id,
                                                                          year=year, month=month, week=week,
                                                                          update_time=time)
                                res = {"code": 20000, "success": True, "msg": "编辑成功！", "data": req_data}
                            except Exception as e:
                                res = {"code": 10014, "success": False, "msg": "编辑失败", "data": e}
                    else:
                        res = {"code": 10014, "success": False, "msg": "数据库不存在该记录", "data": ""}
                except Exception as e:
                    res = {"code": 10014, "success": False, "msg": "查询id出错", "data": e}
        return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)


class OnlineBugView(View):
    def get(self, request, *args, **kwargs):
        req = request.GET
        if not len(req):
            db_data = OnlineBug.objects.all().filter(is_delete=0).order_by("create_time")
            result_data = serializers.serialize("json", db_data, ensure_ascii=False)
            total = Paginator(result_data, default_pageSize).num_pages
            dict_data = json.loads(result_data)
            result_data_list = []
            for data1 in dict_data:
                data1["fields"]["product_name"] = App.objects.filter(
                    product_id=data1["fields"]["product_id"]).first().product_name
                data1["fields"]["project_name"] = Project.objects.filter(
                    project_id=data1["fields"]["project_id"]).first().project_name
                result_data_list.append(data1['fields'])
            res = {"code": 20000, "success": True, "data": {"pageData": result_data_list},
                   "pageInfo": {"pageNo": default_pageNo, "pageSize": default_pageSize, "total": total}}
        else:
            product_id, project_id, year, month, week, start_time, end_time = req.get('productId'), req.get(
                'projectId'), req.get('year'), req.get('month'), req.get('week'), req.get('startTime'), req.get(
                'endTime')
            page_size, page_no = req.get("pageSize", default_pageSize), req.get("pageNo", default_pageNo)
            if year is None and month:
                res = {"code": 10012, "success": False, "msg": "请选择年份！"}
            elif year is None and month is None and week:
                res = {"code": 10012, "success": False, "msg": "请选择年份和月份！"}
            else:
                if product_id:
                    db_data = OnlineBug.objects.filter(product_id=product_id, is_delete=0)
                if project_id:
                    db_data = OnlineBug.objects.filter(project_id=project_id, is_delete=0)
                if start_time and end_time:
                    db_data = OnlineBug.objects.filter(create_time=(start_time, end_time), is_delete=0)
                if year and week and month:
                    db_data = OnlineBug.objects.filter(year=year, month=month, week=week, is_delete=0)
                if year and month:
                    db_data = OnlineBug.objects.filter(year=year, month=month, is_delete=0)
                data = Paginator(db_data, page_size).get_page(page_no)
                total = Paginator(db_data, default_pageSize).num_pages
                result_data = serializers.serialize("json", data)
                dict_data = json.loads(result_data)
                result_data_list = []
                for data1 in dict_data:
                    data1["fields"]["product_name"] = App.objects.filter(
                        product_id=data1["fields"]["product_id"]).first().product_name
                    data1["fields"]["project_name"] = Project.objects.filter(
                        project_id=data1["fields"]["project_id"]).first().project_name
                    result_data_list.append(data1['fields'])
                res = {"code": 20000, "success": True, "data": {"pageData": result_data_list},
                       "pageInfo": {"pageNo": page_no, "pageSize": page_size, "total": total}}
        return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)

    def post(self, request, *args, **kwargs):
        req_data = json.loads(request.body)
        req_data["create_time"] = time
        if req_data:
            product_id, project_id, feedback_bugs, online_bugs, online_accidents, year, month, week = req_data.get(
                "productId"), req_data.get("projectId"), req_data.get("feedbackBugs"), req_data.get(
                "onlineBugs"), req_data.get("onlineAccidents"), req_data.get("year"), req_data.get(
                "month"), req_data.get("week")
            if product_id and project_id and feedback_bugs and online_bugs and online_accidents and year and month and week:
                product_id_values = App.objects.filter(product_id=product_id).first()
                project_id_values = Project.objects.filter(product_id=product_id, project_id=project_id)
                if project_id_values:
                    try:
                        db_data = {"product_id": product_id, "project_id": project_id, "back_bugs": feedback_bugs,
                                   "online_bugs": online_bugs, "year": year, "month": month, "week": week,
                                   "online_accidents": online_accidents, "create_time": time, "update_time": time,
                                   "is_delete": 0}
                        data = OnlineBug.objects.create(**db_data)
                        data.save()
                        res = {"code": 20000, "success": True, "msg": "添加成功！", "data": db_data}
                    except Exception as e:
                        res = {"code": 10008, "success": False, "msg": e, "data": ""}
                elif product_id_values:
                    res = {"code": 10000, "success": True, "msg": "产品线与项目组不匹配", "data": ""}
                else:
                    res = {"code": 10000, "success": True, "msg": "不存在该产品线", "data": ""}
            else:
                res = {"code": 10012, "success": False, "msg": "缺少必填参数！", "data": ""}
        else:
            res = {"code": 10012, "success": False, "msg": "请求参数为空！", "data": ""}
        return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)

    def put(self, request, *args, **kwargs):
        req_data = json.loads(request.body)
        if req_data:
            req_id = req_data.get("id")
            if req_id:
                try:
                    id_data = OnlineBug.objects.filter(is_delete=0, id=req_id)
                    if id_data:
                        product_id, project_id, feedback_bugs, online_bugs, online_accidents, year, month, week = req_data.get(
                            "productId"), req_data.get("projectId"), req_data.get("feedbackBugs"), req_data.get(
                            "onlineBugs"), req_data.get("onlineAccidents"), req_data.get("year"), req_data.get(
                            "month"), req_data.get("week")
                        if product_id and project_id and feedback_bugs and online_bugs and online_accidents and year and month and week:
                            try:
                                OnlineBug.objects.filter(id=req_id).update(product_id=product_id, project_id=project_id,
                                                                          back_bugs=feedback_bugs,
                                                                          online_bugs=online_bugs, online_accidents=online_accidents,
                                                                          year=year, month=month, week=week,
                                                                          update_time=time)
                                res = {"code": 20000, "success": True, "msg": "编辑成功！", "data": req_data}
                            except Exception as e:
                                res = {"code": 10014, "success": False, "msg": "编辑失败", "data": e}
                    else:
                        res = {"code": 10014, "success": False, "msg": "数据库不存在该记录", "data": ""}
                except Exception as e:
                    res = {"code": 10014, "success": False, "msg": "查询id出错", "data": e}
        return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)
