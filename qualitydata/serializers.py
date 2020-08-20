from rest_framework import serializers
from mypro.models import Iterable, OnlineBug


class IterableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Iterable
        fields = ('id', 'project_id', 'product_id', 'publish_num', 'cases_num', 'bugs_num', 'test_user_id', 'year',
                  'week', 'month', 'create_time', 'update_time', 'is_delete')


class OnlineBugSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnlineBug
        fields = ('id', 'project_id', 'product_id', 'back_bugs', 'online_bugs', 'online_accidents', 'year', 'week',
                  'month', 'create_time', 'update_time', 'is_delete')
