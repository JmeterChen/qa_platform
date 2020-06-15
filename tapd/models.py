from django.db import models


# Create your models here.


class ProjectToken(models.Model):
	projectName = models.CharField(max_length=20, null=False)
	projectId = models.CharField(max_length=8, unique=True, null=False)
	robotToken = models.URLField(max_length=120, null=False)
	userName = models.CharField(max_length=10, null=False)
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	sys_time = models.DateTimeField('保存时间', auto_now=True)
	
	class Meta:
		db_table = 't_token'