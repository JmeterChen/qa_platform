from django.shortcuts import render,HttpResponse

from django.views import View
from django.http.response import JsonResponse
from mypro import models
from testcase.forms.case import CaseForm01,CaseForm02


import json
# Create your views here.

class CaseView(View):
    #查询
    def get(self,request):
        #判断前端是否传了查询条件 http://127.0.0.1:8000/formcase?product_name=22房2.0
        #request.GET.get('id')

        res = request.GET.get('product_name')

        if res is not None:
            queryset = models.TestCase.objects.values().filter(product_name=res)#pk=res

            # for row in queryset:
            #     print(row['id'],row['product_name'])
            #判断queryset是否为空
            #QuerySet.exists() > QuerySet.count()==0 > QuerySet
            if queryset.exists():
                print(queryset)
                return JsonResponse({
                    "code": 0,
                    "msg": 'success',
                    "data": list(queryset),
                    # "product_name":row['product_name']
                })
            #传入的res 匹配到数据库中有值
            else:
                return JsonResponse({
                    "code": 1,
                    "msg": "数据不存在"
                })
            #如果前端没有传参数，则查询全部
        else:
            queryset = models.TestCase.objects.values()
            return JsonResponse({
                "code": 0,
                "msg": 'success',
                "data": list(queryset)
            })


    #新增
    def post(self,request):
        #反序列化 解析成json
        form = CaseForm01(json.loads(request.body.decode()))
        #form = BookForm(request.POST)
        if form.is_valid():#如果检验全部通过
            instance = form.save()
            return JsonResponse({
                "code": 0,
                "data": instance.pk #获取主键值,索引
            })
        else:
            return JsonResponse({
                "code": 1,
                "data": form.errors
            })



# #{"title":instance.title,"data":instance.data}
class CaseDetailView(View):
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


        #编辑
    def put(self,request,pk):
        instance = models.TestCase.objects.filter(pk=pk).first()
        #如果不存在
        if not instance:
            return JsonResponse({
                "code": 1,
                "data": '数据不存在'
            })


        form = CaseForm02(instance,json.loads(request.body.decode()))

        if form.is_valid():  # 如果检验全部通过
            instance = form.save()
            return JsonResponse({
                "code": 0,
                "data": instance.pk  # 获取主键值,索引
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

