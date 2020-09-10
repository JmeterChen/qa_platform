from django.db import models

# Create your models here.


class BuglyData(models.Model):
	eventType = models.CharField("事件", null=False, max_length=50)
	timestamp = models.CharField("发布该数据时间搓", null=False, max_length=50)
	date = models.CharField("数据收集日期", null=False, max_length=10)
	appName = models.CharField('APP名称', null=False, max_length=20)
	appId = models.CharField('AppID', null=False, max_length=20)
	appUrl = models.URLField("数据查询链接",  null=False, max_length=200)
	version = models.CharField("APP版本",  null=False, max_length=50)
	platformId = models.IntegerField("APP平台", null=False, default=1)
	signature = models.CharField(null=False, max_length=50)
	accessCount = models.IntegerField("联网总次数", null=False)
	accessUser = models.IntegerField("联网总人数", null=False)
	crashCount = models.IntegerField("奔溃总次数", null=False)
	crashUser = models.IntegerField("奔溃总人数", null=False)
	url = models.URLField("该条数据查询链接",  null=False, max_length=200)
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	is_delete = models.IntegerField('删除状态', choices=((0, '否'), (1, '是')), default=0)

	class Meta:
		db_table = 'qa_bugly'
