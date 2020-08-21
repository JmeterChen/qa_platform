from django.views import View
from django.http.response import JsonResponse
from mypro import models
from testcase.forms.modelformcase import CaseModelForm
from django.shortcuts import HttpResponse,render

from django.core.paginator import Paginator

from django.core import serializers
import json


class CaseGet(View):

    def get(self,request):
        if request.method == "GET":
            pageNo = request.GET.get('pageNo')
            pageSize = request.GET.get('pageSize')
            product_id = request.GET.get('product_id')
            project_id = request.GET.get('project_id')
            main_tasks = request.GET.get('main_tasks')
            #判断传入页面和默认值
            if pageNo == None :
                pageNo = 1
            if pageSize == None:
                pageSize =10
            search_dict = {}
            if product_id:
                search_dict['product_id'] = product_id
            if project_id:
                search_dict['project_id'] = project_id
            if main_tasks:
                queryset = models.TestCase.objects.filter(**search_dict, main_tasks__contains=main_tasks).order_by('id')
            if not main_tasks:
                queryset = models.TestCase.objects.filter(**search_dict).order_by('id')
            # 增加排序 修复分页器warning 增加main_tasks模糊查询
            #分页器
            ptr = Paginator(queryset, pageSize)
            masters = ptr.page(pageNo)

            json_data = json.loads(serializers.serialize("json", masters))
            # 先将Testcase表的id取出来 再分别去app和project表取name值，最后添加到响应的字典中
            # 方法1 需要多次操作数据库并且双循环 效率低
            #         for d in json_data:
            #             prod_id = d['fields']['product_id']
            #
            #             prod_name = models.App.objects.filter(product_id=prod_id).values('product_name')
            #             print(prod_name)
            #             for q in prod_name:
            #                 d['fields']['product_name'] = q['product_name']
            # 方法二 内存中操作和赋值 效率更快
            prod_id = []
            for d in json_data:
                prod_id.append(d['fields']['product_id'])
                d['fields']['id']=int(d['pk'])
                d['pageNo']=pageNo
                d['pageSize'] = pageSize
                d['total'] = ptr.count
                del d['pk']
                del d['model']
                # 查询出所有product_name

            prod_name = models.App.objects.filter(product_id__in=prod_id).values('product_name', 'product_id')
            prod_name = list(prod_name)
            dic = {}
            for p in prod_name:
                dic[p['product_id']] = p['product_name']

            # 赋值
            for d in json_data:
                d['fields']['product_name'] = dic[d['fields']['product_id']]

            # project_name获取
            proj_id = []
            for d in json_data:
                proj_id.append(d['fields']['project_id'])
            proj_name = models.Project.objects.filter(project_id__in=proj_id).values('project_name', 'project_id')
            proj_name = list(proj_name)

            dic = {}
            for p in proj_name:
                dic[p['project_id']] = p['project_name']

            for d in json_data:
                d['fields']['project_name'] = dic[d['fields']['project_id']]

            return JsonResponse({
                "code": 0,
                "msg":"success",
                "data": json_data,
            })

class CaseAdd(View):
    def post(self,request):
        obj = CaseModelForm(json.loads(request.body.decode()))
        if obj.is_valid():
            ins = obj.save()
            print(list(obj))
            return JsonResponse({
                "code": 0,
                "msg":'success',
                "data": ins.pk  # 获取主键值,索引
            })
        else:
            return JsonResponse({
                "code": 1,
                "msg": obj.errors
            })


class CaseUpdate(View):
    def put(self,request):
        update_set = json.loads(request.body.decode())
        update_id = update_set.get('id')
        if update_id:
            instance = models.TestCase.objects.filter(pk=update_id).first()
            if not instance:
                return JsonResponse({
                    "code": 1,
                    "data": '数据不存在'
                })
            # 更新数据
            form = CaseModelForm(update_set, instance=instance)
            if form.is_valid():
                obj = form.save()
                return JsonResponse({
                    "code": 0,
                    "msg":"success",
                    "data": obj.pk
                })
            else:
                return JsonResponse({
                    "code": 1,
                    "data": form.errors
                })


class CaseDel(View):

    def delete(self,request):
        #从请求body中获取ID 序列化
        delete_set = json.loads(request.body.decode())
        delete_id = delete_set.get('id')
        models.TestCase.objects.filter(id=delete_id).update(is_delete=1)
        return JsonResponse({
            "code": 0,
            "msg":"sucess"
        })
