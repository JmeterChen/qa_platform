from django.db import models
import django.utils.timezone as timezone

# Create your models here.


class Users(models.Model):
	username = models.CharField(max_length=10, unique=True, null=False)
	phoneNumber = models.CharField(max_length=11, null=False, unique=True)
	sex = models.IntegerField(default=2)
	email = models.EmailField(null=False, unique=True)
	add_date = models.DateTimeField('保存日期', default=timezone.now)
	mod_date = models.DateTimeField('最后修改日期', auto_now=True)
	
	class Meta:
		db_table = 't_users'