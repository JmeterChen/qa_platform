from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet,ModelViewSet

from rest_framework import serializers
from django.shortcuts import HttpResponse
from rest_framework import response
from mypro import models
from rest_framework.pagination import PageNumberPagination

#自定义异常类
class ExistsErrors(Exception):
    pass


#分页
class MyPageNumberPagination(PageNumberPagination):

    page_size = 10
    page_size_query_param = 'pageSize'
    page_query_param = 'pageNo'
    max_page_size =10

#ModelSerializer校验
class CaseSerializer(serializers.ModelSerializer):
    main_tasks = serializers.CharField(required=False)
    product_name = serializers.SerializerMethodField("get_product_name")
    project_name = serializers.SerializerMethodField("get_project_name")
    class Meta:
        model = models.TestCase
        fields = '__all__'
        # fields = ['product_id','product_name','project_id','iterable_name','main_tasks','test_cases_url','test_user','operator']

    def get_product_name(self, obj):
        product_name = ""
        if obj.product_id:
            product_id = obj.product_id
            product_name = models.App.objects.filter(product_id=product_id).first().product_name
        return product_name

    def get_project_name(self, obj):
        project_name = ""
        if obj.project_id:
            project_id = obj.project_id
            project_name = models.Project.objects.filter(product_id=project_id).first().project_name
        return project_name

class CaseGet(APIView):
    def get(self,request,*args,**kwargs):
        pageNo = request.GET.get('pageNo')
        pageSize = request.GET.get('pageSize')
        product_id = request.GET.get('product_id')
        project_id = request.GET.get('project_id')
        main_tasks = request.GET.get('main_tasks')

        search_dict = {}
        if product_id:
            search_dict['product_id'] = product_id
        if project_id:
            search_dict['project_id'] = project_id
        try:
            if main_tasks:
                queryset = models.TestCase.objects.filter(**search_dict, main_tasks__contains=main_tasks,
                                                          is_delete=0).order_by('-id')
            if not main_tasks:
                queryset = models.TestCase.objects.filter(**search_dict, is_delete=0).order_by('-id')
            pg = MyPageNumberPagination()
            # 判断传入页面和默认值
            if pageNo == None:
                pageNo = 1
            if pageSize == None:
                pageSize = pg.page_size
            pg_cases = pg.paginate_queryset(queryset=queryset,request=request,view=self)
            ser = CaseSerializer(instance=pg_cases,many=True)

            ret = {'code':0,'msg':'successs'}

            if not queryset.exists():
                raise ExistsErrors()
            ret['pageNo']=pageNo
            ret['pageSize'] = pageSize
            ret['total'] = pg.page.paginator.count
            ret['data']=ser.data
        except ExistsErrors as e:
            response['code'] = 1001
            response['data'] = '查询无结果'
        except Exception as e:
            response['code'] = 1002
            response['data'] = '请稍后再试'
        return response.Response(ret)


# class CaseAdd(ModelViewSet):
#     queryset = models.TestCase.objects.all()
#     serializer_class = CaseSerializer


class CaseAdd(APIView):

    def post(self,request,*args,**kwargs):
        #header增加operator字段
        HTTP_OPERATOR = request.META.get('HTTP_OPERATOR')
        if HTTP_OPERATOR:
            request.data['operator'] = HTTP_OPERATOR
        ser = CaseSerializer(data=request.data)
        if ser.is_valid():
            ser.save()
            return response.Response(ser.data)
        else:
            return response.Response(ser.errors)

