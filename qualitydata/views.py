from django.views import View
from mypro.models import Iterable, OnlineBug, App, Project
from django.http import JsonResponse
import json
from django.core import serializers
from django.core.paginator import Paginator
import time
import datetime
from django.db.models import Q, Sum
import calendar

default_pageNo = 1
default_pageSize = 10
time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


class IterableView(View):
    def get(self, request, *args, **kwargs):
        req = request.GET
        conditions = {}
        conditions['is_delete'] = 0
        page_size, page_no = req.get("page_size", default_pageSize), req.get("page_no", default_pageNo)
        if req.get('project_id'):
            conditions['project_id'] = req.get('project_id')
        if req.get('product_id'):
            conditions['product_id'] = req.get('product_id')
        if req.get('create_start_time'):
            conditions['create_time__gte'] = datetime.datetime.strptime(req.get('create_start_time'), '%Y-%m-%d')
        if req.get('create_end_time'):
            conditions['create_time__lte'] = datetime.datetime.strptime(req.get('create_end_time'), '%Y-%m-%d') + datetime.timedelta(days=1)
        if req.get('type') == '1':
            if req.get('start_time'):
                conditions['end_time__gte'] = req.get('start_time')
            if req.get('end_time'):
                conditions['start_time__lte'] = req.get('end_time')
            start_time = datetime.datetime.strptime(req.get('start_time'), '%Y-%m-%d')
            end_time = datetime.datetime.strptime(req.get('end_time'), '%Y-%m-%d')
            db_data = Iterable.objects.filter(**conditions).values('product_id', 'project_id', 'publish_num', 'cases_num', 'bugs_num', 'start_time', 'end_time')
            for data in db_data:
                if data['start_time'] < start_time and data['end_time'] < end_time and (data['end_time'] - start_time).days < (start_time - data['start_time']).days:
                    db_data.remove(data)
                if data['start_time'] > start_time and data['start_time'] < end_time and data['end_time'] > end_time and (data['end_time'] - end_time).days > (end_time - data['start_time']).days:
                    db_data.remove(data)
                if data['start_time'] < start_time and data['end_time'] > end_time and (data['end_time'] - data['start_time']).days > (end_time-start_time)*2:
                    db_data.remove(data)

        if req.get('type') == '2':
            if req.get('start_time'):
                conditions['year__gte'] = datetime.datetime.strptime(req.get('start_time'), '%Y-%m-%d').year
                conditions['month__gte'] = datetime.datetime.strptime(req.get('start_time'), '%Y-%m-%d').month
            if req.get('end_time'):
                conditions['year__lte'] = datetime.datetime.strptime(req.get('end_time'), '%Y-%m-%d').year
                conditions['month__lte'] = datetime.datetime.strptime(req.get('end_time'), '%Y-%m-%d').month
            db_data = Iterable.objects.filter(**conditions).values('product_id', 'project_id').annotate(
                publish_num=Sum('publish_num'), cases_num=Sum('cases_num'), bugs_num=Sum('bugs_num'))
        page_data = Paginator(db_data, page_size).get_page(page_no)
        total = Paginator(db_data, default_pageSize).count
        if req.get('type') == '1':
            project_id_list = [i['project_id'] for i in page_data.object_list]
            product_id_list = [i['product_id'] for i in page_data.object_list]
        if req.get('type') == '2':
            project_id_list = [i['project_id'] for i in page_data.object_list.values('project_id')]
            product_id_list = [i['product_id'] for i in page_data.object_list.values('product_id')]
        # 查询product信息
        product_info_list = App.objects.filter(product_id__in=product_id_list).values('product_id', 'product_name')
        # 查询项目信息
        project_info_list = Project.objects.filter(project_id__in=project_id_list).values('project_id', 'project_name')
        # 根据项目id查询统计开始时间和结束时间，同一个项目下取最早的开始时间和最晚的截止时间
        base_info_list = Iterable.objects.filter(project_id__in=project_id_list)
        stat_start_time_map = {}
        stat_end_time_map = {}
        create_time_map = {}
        op_user_map = {}
        for data in base_info_list:
            if not stat_start_time_map.keys().__contains__(data.project_id) or stat_start_time_map[
                data.project_id] > data.start_time:
                stat_start_time_map[data.project_id] = data.start_time
            if not stat_end_time_map.keys().__contains__(data.project_id) or stat_end_time_map[
                data.project_id] < data.end_time:
                stat_end_time_map[data.project_id] = data.end_time
            if not create_time_map.keys().__contains__(data.project_id):
                create_time_map[data.project_id] = data.create_time
            if not op_user_map.keys().__contains__(data.project_id):
                op_user_map[data.project_id] = data.op_user_name

        product_info_map = {i['product_id']: i['product_name'] for i in product_info_list}
        project_info_map = {i['project_id']: i['project_name'] for i in project_info_list}

        result_data_list = []
        for data in page_data.object_list:
            data['product_name'] = product_info_map[data['product_id']]
            data['project_name'] = project_info_map[data['project_id']]
            data['create_time'] = create_time_map[data['project_id']].strftime("%Y-%m-%d")
            data['stat_start_time'] = stat_start_time_map[data['project_id']].strftime("%Y-%m-%d")
            data['stat_end_time'] = stat_end_time_map[data['project_id']].strftime("%Y-%m-%d")
            data['op_user_name'] = op_user_map[data['project_id']]
            result_data_list.append(data)
            # data['start_time'] = req.get('start_time')

        res = {"code": 20000, "success": True, "data": {"pageData": result_data_list},
               "page_no": page_no, "page_size": page_size, "total": total}
        return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)

    def post(self, request, *args, **kwargs):
        req_data = json.loads(request.body)
        if req_data:
            product_id, project_id, publish_num, cases_num, bugs_num, test_user_id, start_time, end_time = req_data.get(
                "product_id"), req_data.get("project_id"), req_data.get("publish_num"), req_data.get(
                "cases_num"), req_data.get("bugs_num"), req_data.get(
                "test_user_id"), req_data.get("start_time"), req_data.get("end_time")
            req_data["create_time"] = time
            op_user_name = request.META.get("HTTP_NAME", '')
            if product_id and project_id and publish_num and cases_num and bugs_num and test_user_id and start_time and end_time and op_user_name:
                product_id_values = App.objects.filter(product_id=product_id).first()
                project_id_values = Project.objects.filter(product_id=product_id, project_id=project_id)
                if project_id_values:
                    pre_day = calendar.monthrange(int(start_time[0:4]), int(start_time[5:7]))[1] - int(start_time[-2:])
                    last_day = int(end_time[-2:]) - 1
                    if pre_day >= last_day:
                        year = int(start_time[0:4])
                        month = int(start_time[5:7])
                    else:
                        year = int(end_time[0:4])
                        month = int(end_time[5:7])
                    try:
                        db_data = {"product_id": product_id, "project_id": project_id,
                                   "publish_num": publish_num, "cases_num": cases_num, "end_time": end_time,
                                   "op_user_name": op_user_name,
                                   "start_time": start_time, "bugs_num": bugs_num, "test_user_id": test_user_id,
                                   "create_time": time, "update_time": time, 'year':year, 'month':month, "is_delete": 0}
                        data = Iterable.objects.create(**db_data)
                        data.save()
                        res = {"code": 20000, "success": True, "msg": "添加成功！", "data": db_data}
                    except Exception as e:
                        res = {"code": 10008, "success": False, "msg": e, "data": ""}
                elif product_id_values:
                    res = {"code": 10000, "success": True, "msg": "产品线与项目组不匹配！", "data": ""}
                else:
                    res = {"code": 10000, "success": True, "msg": "不存在该产品线！", "data": ""}
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
                        product_id, project_id, publish_num, cases_num, bugs_num, test_user_id, start_time, end_time = req_data.get(
                            "product_id"), req_data.get("project_id"), req_data.get(
                            "publish_num"), req_data.get(
                            "cases_num"), req_data.get("bugs_num"), req_data.get(
                            "test_user_id"), req_data.get("start_time"), req_data.get("end_time")
                        op_user_name = request.META.get("HTTP_NAME", '')
                        if product_id and project_id and publish_num and cases_num and bugs_num and test_user_id and start_time and end_time and op_user_name:
                            pre_day = calendar.monthrange(int(start_time[0:4]), int(start_time[5:7]))[1] - int(
                                start_time[-2:])
                            last_day = int(end_time[-2:]) - 1
                            if pre_day >= last_day:
                                year = int(start_time[0:4])
                                month = int(start_time[5:7])
                            else:
                                year = int(end_time[0:4])
                                month = int(end_time[5:7])
                            try:
                                Iterable.objects.filter(id=req_id).update(product_id=product_id, project_id=project_id,
                                                                          publish_num=publish_num,
                                                                          cases_num=cases_num, bugs_num=bugs_num,
                                                                          test_user_id=test_user_id,
                                                                          start_time=start_time, end_time=end_time,
                                                                          op_user_name=op_user_name,
                                                                          update_time=time, year=year,month=month)
                                res = {"code": 20000, "success": True, "msg": "编辑成功！", "data": req_data}
                            except Exception as e:
                                res = {"code": 10014, "success": False, "msg": "编辑失败！", "data": e}
                    else:
                        res = {"code": 10014, "success": False, "msg": "数据库不存在该记录！", "data": ""}
                except Exception as e:
                    res = {"code": 10014, "success": False, "msg": "查询id出错！", "data": e}
        return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)


class OnlineBugView(View):
    def get(self, request, *args, **kwargs):
        req = request.GET
        if req.get('week') and req.get('month') is None:
            res = {"code": 10012, "success": False, "msg": "请选择月份！", "data": ""}
            return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)
        if req.get('month') and req.get('year') is None:
            res = {"code": 10012, "success": False, "msg": "请选择年份！", "data": ""}
            return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)
        conditions = {}
        if req.get('project_id'):
            conditions['project_id'] = req.get('project_id')
        if req.get('product_id'):
            conditions['product_id'] = req.get('product_id')
        if req.get('year'):
            conditions['year'] = req.get('year')
        if req.get('month'):
            conditions['month'] = req.get('month')
        if req.get('week'):
            conditions['week'] = req.get('week')
        if req.get('start_time'):
            conditions['create_time__gte'] = req.get('start_time')
        if req.get('end_time'):
            conditions['create_time__lte'] = req.get('end_time')
        conditions['is_delete'] = 0
        page_size, page_no = req.get("page_size", default_pageSize), req.get("page_no", default_pageNo)

        db_data = OnlineBug.objects.filter(**conditions).order_by('create_time')
        page_data = Paginator(db_data, page_size).get_page(page_no)
        total = Paginator(db_data, default_pageSize).count
        project_id_list = [i['project_id'] for i in page_data.object_list.values('project_id')]
        product_id_list = [i['product_id'] for i in page_data.object_list.values('product_id')]
        # 查询product信息
        product_info_list = App.objects.filter(product_id__in=product_id_list).values('product_id', 'product_name')
        # 查询项目信息
        project_info_list = Project.objects.filter(project_id__in=project_id_list).values('project_id', 'project_name')
        product_info_map = {i['product_id']: i['product_name'] for i in product_info_list}
        project_info_map = {i['project_id']: i['project_name'] for i in project_info_list}

        result_data = serializers.serialize("json", page_data.object_list)
        dict_data = json.loads(result_data)
        result_data_list = [i['fields'] for i in dict_data]
        for data in result_data_list:
            data['product_name'] = product_info_map[data['product_id']]
            data['project_name'] = project_info_map[data['project_id']]

        res = {"code": 20000, "success": True, "data": {"pageData": result_data_list},
               "page_no": page_no, "page_size": page_size, "total": total}
        return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)

    # def get(self, request, *args, **kwargs):
    #     req = request.GET
    #     if not len(req):
    #         db_data = OnlineBug.objects.all().filter(is_delete=0).order_by("create_time")
    #         result_data = serializers.serialize("json", db_data, ensure_ascii=False)
    #         total = Paginator(result_data, default_pageSize).num_pages
    #         dict_data = json.loads(result_data)
    #         result_data_list = []
    #         for data1 in dict_data:
    #             data1["fields"]["product_name"] = App.objects.filter(
    #                 product_id=data1["fields"]["product_id"]).first().product_name
    #             data1["fields"]["project_name"] = Project.objects.filter(
    #                 project_id=data1["fields"]["project_id"]).first().project_name
    #             result_data_list.append(data1['fields'])
    #         res = {"code": 20000, "success": True, "data": {"pageData": result_data_list},
    #                "pageNo": default_pageNo, "pageSize": default_pageSize, "total": total}
    #     else:
    #         product_id, project_id, year, month, week, start_time, end_time = req.get('product_id'), req.get(
    #             'project_id'), req.get('year'), req.get('month'), req.get('week'), req.get('start_time'), req.get(
    #             'end_time')
    #         page_size, page_no = req.get("page_size", default_pageSize), req.get("page_no", default_pageNo)
    #         if year is None and month:
    #             res = {"code": 10012, "success": False, "msg": "请选择年份！", "data": ""}
    #         elif year is None and month is None and week:
    #             res = {"code": 10012, "success": False, "msg": "请选择年份和月份！", "data": ""}
    #         else:
    #             if product_id:
    #                 db_data = OnlineBug.objects.filter(product_id=product_id, is_delete=0)
    #             if project_id:
    #                 db_data = OnlineBug.objects.filter(project_id=project_id, is_delete=0)
    #             if start_time and end_time:
    #                 db_data = OnlineBug.objects.filter(create_time=(start_time, end_time), is_delete=0)
    #             if year and week and month:
    #                 db_data = OnlineBug.objects.filter(year=year, month=month, week=week, is_delete=0)
    #             if year and month:
    #                 db_data = OnlineBug.objects.filter(year=year, month=month, is_delete=0)
    #             data = Paginator(db_data, page_size).get_page(page_no)
    #             total = Paginator(db_data, default_pageSize).num_pages
    #             result_data = serializers.serialize("json", data)
    #             dict_data = json.loads(result_data)
    #             result_data_list = []
    #             for data1 in dict_data:
    #                 data1["fields"]["product_name"] = App.objects.filter(
    #                     product_id=data1["fields"]["product_id"]).first().product_name
    #                 data1["fields"]["project_name"] = Project.objects.filter(
    #                     project_id=data1["fields"]["project_id"]).first().project_name
    #                 result_data_list.append(data1['fields'])
    #             res = {"code": 20000, "success": True, "data": {"pageData": result_data_list},
    #                    "pageInfo": {"pageNo": page_no, "pageSize": page_size, "total": total}}
    #     return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)

    def post(self, request, *args, **kwargs):
        req_data = json.loads(request.body)
        req_data["create_time"] = time
        if req_data:
            product_id, project_id, back_bugs, online_bugs, online_accidents, year, month, week = req_data.get(
                "product_id"), req_data.get("product_id"), req_data.get("back_bugs"), req_data.get(
                "online_bugs"), req_data.get("online_accidents"), req_data.get("year"), req_data.get(
                "month"), req_data.get("week")
            if product_id and project_id and back_bugs and online_bugs and online_accidents and year and month and week:
                product_id_values = App.objects.filter(product_id=product_id).first()
                project_id_values = Project.objects.filter(product_id=product_id, project_id=project_id)
                if project_id_values:
                    try:
                        db_data = {"product_id": product_id, "project_id": project_id, "back_bugs": back_bugs,
                                   "online_bugs": online_bugs, "year": year, "month": month, "week": week,
                                   "online_accidents": online_accidents, "create_time": time, "update_time": time,
                                   "is_delete": 0}
                        data = OnlineBug.objects.create(**db_data)
                        data.save()
                        res = {"code": 20000, "success": True, "msg": "添加成功！", "data": db_data}
                    except Exception as e:
                        res = {"code": 10008, "success": False, "msg": e, "data": ""}
                elif product_id_values:
                    res = {"code": 10000, "success": True, "msg": "产品线与项目组不匹配！", "data": ""}
                else:
                    res = {"code": 10000, "success": True, "msg": "不存在该产品线！", "data": ""}
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
                        product_id, project_id, back_bugs, online_bugs, online_accidents, year, month, week = req_data.get(
                            "product_id"), req_data.get("project_id"), req_data.get("back_bugs"), req_data.get(
                            "online_bugs"), req_data.get("online_accidents"), req_data.get("year"), req_data.get(
                            "month"), req_data.get("week")
                        if product_id and project_id and back_bugs and online_bugs and online_accidents and year and month and week:
                            try:
                                OnlineBug.objects.filter(id=req_id).update(product_id=product_id, project_id=project_id,
                                                                           back_bugs=back_bugs,
                                                                           online_bugs=online_bugs,
                                                                           online_accidents=online_accidents,
                                                                           year=year, month=month, week=week,
                                                                           update_time=time)
                                res = {"code": 20000, "success": True, "msg": "编辑成功！", "data": req_data}
                            except Exception as e:
                                res = {"code": 10014, "success": False, "msg": "编辑失败！", "data": e}
                    else:
                        res = {"code": 10014, "success": False, "msg": "数据库不存在该记录！", "data": ""}
                except Exception as e:
                    res = {"code": 10014, "success": False, "msg": "查询id出错！", "data": e}
        return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)
