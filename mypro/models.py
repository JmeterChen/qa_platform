from django.db import models


# Create your models here.


class Orders(models.Model):
	orderId = models.CharField(primary_key=True, max_length=20)
	orderName = models.CharField(max_length=18, null=False)
	money = models.IntegerField(null=False, default=0)
	status = models.IntegerField(choices=((0, '待支付'), (1, '已支付'), (2, '已取消未退款'), (3, '已取消已退款')), default=0)
	createUserName = models.CharField(max_length=10, null=False)
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	sys_time = models.DateTimeField('保存时间', auto_now=True)
	
	def __str__(self):
		return self.orderName