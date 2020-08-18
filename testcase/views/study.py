from django.views import View
from django.http.response import JsonResponse
from mypro import models
from testcase.forms.modelformcase import CaseModelForm
from django.shortcuts import HttpResponse,render

from django.core.paginator import Paginator

from django.core import serializers
import json

def case_list(request):
    li = models.TestCase.objects.all()
    return render(request,'b.html',{'li':li})



def detail(request,nid):

    if request.method == "GET":
        print(nid)
        case_detail = models.TestCase.objects.filter(id=nid).first()
        mf = CaseModelForm(instance=case_detail)
        return render(request,"a.html",{"mf":mf})


class CaseModelView(View):
    #
    # def get(self,request):
    #     # 返回指定字段
    #     queryset = models.TestCase.objects.values()
    #     return JsonResponse({
    #         "code": 0,
    #         "data": list(queryset)
    #         })
    # ,fields=('product_id','project_id')
    def get(self,request):
        from django.core import serializers
        queryset = models.TestCase.objects.all()
        data = serializers.serialize('json',queryset,fields=('iterable_name','main_tasks','test_cases_url','cases_num','test_user'))
        json_data = json.loads(data)
        #删除返回中的pk,model
        for d in json_data:
            del d['pk']
            del d['model']
        return JsonResponse({
            "code": 0,
            "data": json_data
            })


    def post(self,request):

        obj = CaseModelForm(json.loads(request.body.decode()))
        if obj.is_valid():
            #当前model和多对多关系都会创建
            ins = obj.save()
            # 分步，创建当前model数据和 多对多分开
            # instance = obj.save(False)
            # instance.save()
            # obj.save_m2m()
            print(list(obj))
            return JsonResponse({
                "code": 0,
                "data": ins.pk  # 获取主键值,索引
            })
        else:
            return JsonResponse({
                "code": 1,
                "data": obj.errors
            })


class CaseDetailModelView(View):
    #查询单个详情
    def get(self,request,pk):
        instance = models.TestCase.objects.values().filter(pk=pk)
        if not instance:
            return JsonResponse({
                "code": 1,
                "data": '数据不存在'
            })
        else:
            return JsonResponse({
                "code": 0,
                "data": list(instance)
            })
        #更新
    def put(self,request,pk):
        instance = models.TestCase.objects.filter(pk=pk).first()
        if not instance:
            return JsonResponse({
                "code": 1,
                "data": '数据不存在'
            })
        #更新数据
        form = CaseModelForm(json.loads(request.body.decode()),instance=instance)
        if form.is_valid():  # 如果检验全部通过
            obj = form.save()
            return JsonResponse({
                "code": 0,
                "data": obj.pk  # 获取主键值,索引
            })
        else:
            return JsonResponse({
                "code": 1,
                "data": form.errors
            })

    #删除
    def delete(self,request,pk):
        models.TestCase.objects.filter(pk=pk).delete()
        return JsonResponse({
            "code": 0,
            "data": []
        })
