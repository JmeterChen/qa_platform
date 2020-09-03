from mypro.models import *
from rest_framework import serializers
import datetime
import calendar


# 获取统计数据属于那一年
def get_year(start_time, end_time):
    pre_date = datetime.datetime.strptime(start_time, '%Y-%m-%d').date()
    last_date = datetime.datetime.strptime(end_time, '%Y-%m-%d').date()
    if (calendar.monthrange(pre_date.year, pre_date.month)[1]) - pre_date.day >= last_date.day:
        year = pre_date.year
    else:
        year = last_date.year
    return year

# 获取统计数据属于那一个月
def get_month(start_time, end_time):
    pre_date = datetime.datetime.strptime(start_time, '%Y-%m-%d').date()
    last_date = datetime.datetime.strptime(end_time, '%Y-%m-%d').date()
    if (calendar.monthrange(pre_date.year, pre_date.month)[1]) - pre_date.day >= last_date.day:
        month = pre_date.month
    else:
        month = last_date.month
    return month


class ProjectSerializers(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField("get_product_name")
    project_name = serializers.SerializerMethodField("get_project_name")

    class Meta:
        model = Project
        fields = ["product_name", "product_id", "project_name", "project_id"]

    def get_product_name(self, obj):
        product_name = ""
        if obj.product_id:
            product_id = obj.product_id
            product_name = App.objects.filter(product_id=product_id).first().product_name if App.objects.filter(
                product_id=product_id).first() else ""
        return product_name

    def get_project_name(self, obj):
        project_name = ""
        if obj.project_id:
            project_id = obj.project_id
            project_name = Project.objects.filter(project_id=project_id).first().project_name if Project.objects.filter(
                project_id=project_id).first() else ""
        return project_name

