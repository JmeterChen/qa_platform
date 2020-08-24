from rest_framework import views, response, serializers
from rest_framework.pagination import PageNumberPagination
from mypro import models
from mypro.models import User
import time


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = "__all__"
        # fields = (
        #     "user_id",
        #     "user_name",
        #     "email",
        #     "phone_number",
        #     "create_time",
        #     "update_time"
        # )


class MyPagination(PageNumberPagination):
    # 分页器
    # 默认一页显示数据条数
    page_size = 1
    page_query_param = 'PageNo'
    page_size_query_param = "PageSize"


class UserList(views.APIView):
    def get(self, request):
        PageNo = request.GET.get("PageNo")
        PageSize = request.GET.get("PageSize")

        # 获取所有未删除的人员
        user_list = models.User.objects.filter(is_delete=0).order_by("create_time")
        # 计算人员的total
        total = user_list.count()

        # 创建分页对象实例
        page = MyPagination()
        page_user_list = page.paginate_queryset(user_list, request, view=self)
        # 对数据序列化 普通序列化 显示的只是数据
        result = UserSerializers(instance=page_user_list, many=True)

        return response.Response({
            "code": 200,
            "success": True,
            "PageNo": PageNo,
            "PageSize": PageSize,
            "total": total,
            "data": result.data
        })


class UserOne(views.APIView):
    def post(self, request):
        # 生成user_id
        user_id = str(round(time.time()))

        # 将生成user_id 塞到user_data
        user_data = request.data
        user_data['user_id'] = user_id

        user = UserSerializers(data=user_data)

        if user.is_valid():
            instance = user.save()
            return response.Response({
                "code": 200,
                "success": True,
                "data": instance.pk
            })
        else:
            return response.Response({
                "code": 99999,
                "success": False,
                "data": user.errors
            })

    def put(self, request):
        user_id = request.data['user_id']
        old_user = models.User.objects.filter(pk=user_id, is_delete=0).first()
        if not old_user:
            return response.Response({
                "code": 99999,
                "success": False,
                "msg": "该人员不存在!",
                "data": []
            })
        user_new = UserSerializers(instance=old_user, data=request.data)
        if user_new.is_valid():
            user = user_new.save()
            return response.Response({
                "code": 200,
                "success": True,
                "mas": "更新成功！",
                "data": user.pk
            })
        else:
            return response.Response({
                "code": 99999,
                "success": False,
                "mas": "更新失败！",
                "data": user_new.errors
            })


class UserDel(views.APIView):
    def post(self, request):
        user_id = request.data['user_id']
        user = User.objects.filter(pk=user_id, is_delete=0)
        print(user)
        if not user:
            return response.Response({
                "code": 99999,
                "success": False,
                "msg": "该人员不存在!",
                "data": []
            })
        else:
            user = User.objects.get(pk=user_id, is_delete=0)
            user.is_delete = 1
            user.save()
            return response.Response({
                "code": 200,
                "success": True,
                "msg": "删除成功!",
                "data": []
            })


        # user_del = UserSerializers(instance=user, data=)
        # if user_del.is_valid():
        #     user_del.save()
        #     return response.Response({
        #         "code": 200,
        #         "success": True,
        #         "msg": "删除成功!",
        #         "data": []
        #     })
        # else:
        #     return response.Response({
        #         "code": 99999,
        #         "success": False,
        #         "msg": "删除失败!",
        #         "data": []
        #     })

