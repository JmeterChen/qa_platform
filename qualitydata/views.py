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
        # 查询周报
        if req.get('type') == '1':
            if req.get('start_time'):
                #结束时间大于等于前端传的开始时间
                conditions['end_time__gte'] = req.get('start_time')
            if req.get('end_time'):
                # 开始时间大于等于前端传的结束时间
                conditions['start_time__lte'] = req.get('end_time')
            # 查询出数据库的所有数据
            start_time = datetime.datetime.strptime(req.get('start_time'), '%Y-%m-%d').date()
            end_time = datetime.datetime.strptime(req.get('end_time'), '%Y-%m-%d').date()
            db_data = Iterable.objects.filter(**conditions).values('id', 'product_id', 'project_id', 'publish_num', 'cases_num', 'bugs_num', 'start_time', 'end_time', 'create_time','op_user_name')
            # 移除不在统计周期内的数据
            for data in db_data:
                # 移除数据库统计结束时间在统计周期内且统计时间超过一半不在此周期内的数据
                if data['end_time']>start_time and data['end_time'] < end_time and data['start_time']<start_time and (start_time - data['start_time']).days>(data['end_time'] - start_time).days:
                    db_data = db_data.exclude(id=data['id'])
                # 移除数据库统计开始时间在统计周期内且统计时间超过一半不在此周期内的数据
                if data['start_time'] > start_time and data['start_time'] <end_time and data['end_time'] > end_time and (data['start_time'] - start_time).days > (end_time - data['start_time']).days:
                    db_data = db_data.exclude(id=data['id'])
                # 移除超过一半时间不在查询范围内的数据
                if data['start_time']< start_time and data['end_time']>end_time and (data['end_time'] - data['start_time']).days > (end_time-start_time).days*2:
                    db_data = db_data.exclude(id=data['id'])
        # 查询月报
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
        # 查询产品名称
        product_info_list = App.objects.filter(product_id__in=product_id_list).values('product_id', 'product_name')
        # 查询项目名称
        project_info_list = Project.objects.filter(project_id__in=project_id_list).values('project_id', 'project_name')
        product_info_map = {i['product_id']: i['product_name'] for i in product_info_list}
        project_info_map = {i['project_id']: i['project_name'] for i in project_info_list}
        result_data_list = []
        for data in page_data.object_list:
            data['product_name'] = product_info_map[data['product_id']]
            data['project_name'] = project_info_map[data['project_id']]
            if req.get('type') == '2':
                data['start_time'] = datetime.datetime.strptime(req.get('start_time'), '%Y-%m-%d').date()
                data['end_time'] = datetime.datetime.strptime(req.get('end_time'), '%Y-%m-%d').date()
            result_data_list.append(data)

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
        # 查询周报
        if req.get('type') == '1':
            if req.get('start_time'):
                #结束时间大于等于前端传的开始时间
                conditions['end_time__gte'] = req.get('start_time')
            if req.get('end_time'):
                # 开始时间大于等于前端传的结束时间
                conditions['start_time__lte'] = req.get('end_time')
            # 查询出数据库的所有数据
            start_time = datetime.datetime.strptime(req.get('start_time'), '%Y-%m-%d').date()
            end_time = datetime.datetime.strptime(req.get('end_time'), '%Y-%m-%d').date()
            db_data = Iterable.objects.filter(**conditions).values('id', 'product_id', 'project_id', 'back_bugs', 'online_bugs', 'online_accidents', 'start_time', 'end_time', 'create_time', 'op_user_name')
            # 移除不在统计周期内的数据
            for data in db_data:
                # 移除数据库统计结束时间在统计周期内且统计时间超过一半不在此周期内的数据
                if data['end_time']>start_time and data['end_time'] < end_time and data['start_time']<start_time and (start_time - data['start_time']).days>(data['end_time'] - start_time).days:
                    db_data = db_data.exclude(id=data['id'])
                # 移除数据库统计开始时间在统计周期内且统计时间超过一半不在此周期内的数据
                if data['start_time'] > start_time and data['start_time'] <end_time and data['end_time'] > end_time and (data['start_time'] - start_time).days > (end_time - data['start_time']).days:
                    db_data = db_data.exclude(id=data['id'])
                # 移除超过一半时间不在查询范围内的数据
                if data['start_time']< start_time and data['end_time']>end_time and (data['end_time'] - data['start_time']).days > (end_time-start_time).days*2:
                    db_data = db_data.exclude(id=data['id'])
        # 查询月报
        if req.get('type') == '2':
            if req.get('start_time'):
                conditions['year__gte'] = datetime.datetime.strptime(req.get('start_time'), '%Y-%m-%d').year
                conditions['month__gte'] = datetime.datetime.strptime(req.get('start_time'), '%Y-%m-%d').month
            if req.get('end_time'):
                conditions['year__lte'] = datetime.datetime.strptime(req.get('end_time'), '%Y-%m-%d').year
                conditions['month__lte'] = datetime.datetime.strptime(req.get('end_time'), '%Y-%m-%d').month
            db_data = Iterable.objects.filter(**conditions).values('product_id', 'project_id').annotate(
                back_bugs=Sum('back_bugs'), online_bugs=Sum('online_bugs'), online_accidents=Sum('online_accidents'))
        page_data = Paginator(db_data, page_size).get_page(page_no)
        total = Paginator(db_data, default_pageSize).count
        if req.get('type') == '1':
            project_id_list = [i['project_id'] for i in page_data.object_list]
            product_id_list = [i['product_id'] for i in page_data.object_list]
        if req.get('type') == '2':
            project_id_list = [i['project_id'] for i in page_data.object_list.values('project_id')]
            product_id_list = [i['product_id'] for i in page_data.object_list.values('product_id')]
        # 查询产品名称
        product_info_list = App.objects.filter(product_id__in=product_id_list).values('product_id', 'product_name')
        # 查询项目名称
        project_info_list = Project.objects.filter(project_id__in=project_id_list).values('project_id', 'project_name')
        product_info_map = {i['product_id']: i['product_name'] for i in product_info_list}
        project_info_map = {i['project_id']: i['project_name'] for i in project_info_list}
        result_data_list = []
        for data in page_data.object_list:
            data['product_name'] = product_info_map[data['product_id']]
            data['project_name'] = project_info_map[data['project_id']]
            if req.get('type') == '2':
                data['start_time'] = datetime.datetime.strptime(req.get('start_time'), '%Y-%m-%d').date()
                data['end_time'] = datetime.datetime.strptime(req.get('end_time'), '%Y-%m-%d').date()
            result_data_list.append(data)

        res = {"code": 20000, "success": True, "data": {"pageData": result_data_list},
               "page_no": page_no, "page_size": page_size, "total": total}
        return JsonResponse(res, json_dumps_params={'ensure_ascii': False}, safe=False)

    def post(self, request, *args, **kwargs):
        req_data = json.loads(request.body)
        if req_data:
            product_id, project_id, back_bugs, online_bugs, online_accidents, test_user_id, start_time, end_time = req_data.get(
                "product_id"), req_data.get("project_id"), req_data.get("back_bugs"), req_data.get(
                "online_bugs"), req_data.get("online_accidents"), req_data.get(
                "test_user_id"), req_data.get("start_time"), req_data.get("end_time")
            req_data["create_time"] = time
            op_user_name = request.META.get("HTTP_NAME", '')
            if product_id and project_id and back_bugs and online_bugs and online_accidents and test_user_id and start_time and end_time and op_user_name:
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
                                   "back_bugs": back_bugs, "online_bugs": online_bugs, "end_time": end_time,
                                   "op_user_name": op_user_name,
                                   "start_time": start_time, "online_accidents": online_accidents, "test_user_id": test_user_id,
                                   "create_time": time, "update_time": time, 'year': year, 'month':month, "is_delete": 0}
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
                        product_id, project_id, back_bugs, online_bugs, online_accidents, test_user_id, start_time, end_time = req_data.get(
                            "product_id"), req_data.get("project_id"), req_data.get(
                            "back_bugs"), req_data.get(
                            "online_bugs"), req_data.get("online_accidents"), req_data.get(
                            "test_user_id"), req_data.get("start_time"), req_data.get("end_time")
                        op_user_name = request.META.get("HTTP_NAME", '')
                        if product_id and project_id and back_bugs and online_bugs and online_accidents and test_user_id and start_time and end_time and op_user_name:
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
                                                                          back_bugs=back_bugs,
                                                                          online_bugs=online_bugs, online_accidents=online_accidents,
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