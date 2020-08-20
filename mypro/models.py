from django.db import models


# Create your models here.


# class Orders(models.Model):
# 	orderId = models.CharField(primary_key=True, max_length=20)
# 	orderName = models.CharField(max_length=18, null=False)
# 	money = models.IntegerField(null=False, default=0)
# 	status = models.IntegerField(choices=((0, '待支付'), (1, '已支付'), (2, '已取消未退款'), (3, '已取消已退款')), default=0)
# 	createUserName = models.CharField(max_length=10, null=False)
# 	create_time = models.DateTimeField('创建时间', auto_now_add=True)
# 	sys_time = models.DateTimeField('保存时间', auto_now=True)
#
# 	def __str__(self):
# 		return self.orderName
	
	
class App(models.Model):
	product_id = models.CharField(primary_key=True, null=False, max_length=20)
	product_name = models.CharField('产品线名称', null=False, unique=True, max_length=20, default='')
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	update_time = models.DateTimeField('编辑时间', auto_now=True)
	is_delete = models.IntegerField('删除状态', choices=((0, '否'), (1, '是')), default=0)

	class Meta:
		db_table = 'qa_app'


class Project(models.Model):
	project_id = models.CharField(primary_key=True, null=False, max_length=20)
	project_name = models.CharField('项目组名称', null=False, unique=False, max_length=20)
	product_id = models.CharField('所属产品线', null=False, max_length=20)
	test_user_id = models.CharField(null=False, max_length=20)
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	update_time = models.DateTimeField('编辑时间', auto_now=True)
	is_delete = models.IntegerField('删除状态', choices=((0, '否'), (1, '是')), default=0)

	class Meta:
		db_table = 'qa_project'


class Iterable(models.Model):
	project_id = models.CharField(null=False, max_length=20)
	product_id = models.CharField('所属产品线', null=False, max_length=20)
	publish_num = models.IntegerField('发版个数', default=0, null=False)
	cases_num = models.IntegerField('用例条数', default=0, null=False)
	bugs_num = models.IntegerField('用例条数', default=0, null=False)
	test_user_id = models.CharField(null=False, max_length=20)
	week = models.IntegerField(null=False, default=1)
	month = models.IntegerField(null=False, default=1)
	year = models.IntegerField(null=False, default=1970)
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	update_time = models.DateTimeField('编辑时间', auto_now=True)
	is_delete = models.IntegerField('删除状态', choices=((0, '否'), (1, '是')), default=0)

	class Meta:
		db_table = 'qa_iterable'


class User(models.Model):
	user_id = models.CharField(primary_key=True, null=False, max_length=20)
	user_name = models.CharField(null=False, max_length=20)
	email = models.EmailField(null=False, unique=True, max_length=20)
	phone_number = models.CharField(null=False, unique=True, max_length=15)
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	update_time = models.DateTimeField('编辑时间', auto_now=True)
	is_delete = models.IntegerField('删除状态', choices=((0, '否'), (1, '是')), default=0)

	class Meta:
		db_table = 'qa_user'


class Devices(models.Model):
	device_id = models.CharField(primary_key=True, null=False, max_length=20)
	device_name = models.CharField(null=False, max_length=20)
	system_name = models.CharField(null=False, max_length=20)
	device_model = models.CharField(null=False, max_length=20)
	system_version = models.CharField(null=False, max_length=20)
	user_id = models.CharField('只记录测试组名下的设备', null=False, max_length=20)
	purchase_date = models.DateTimeField('购买时间')
	location = models.IntegerField(choices=((0, '深圳'), (1, '上海'), (2, '其他')), default=0)
	remark = models.CharField(max_length=100)
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	update_time = models.DateTimeField('编辑时间', auto_now=True)
	is_delete = models.IntegerField('删除状态', choices=((0, '否'), (1, '是')), default=0)

	class Meta:
		db_table = 'qa_devices'


class SonarReport(models.Model):
	product_id = models.CharField(null=False, max_length=20)
	project_id = models.CharField(null=False,  max_length=20)
	service_num = models.IntegerField(default=0)
	sonar_bugs = models.IntegerField(default=0)
	sonar_holes = models.IntegerField(default=0)
	week = models.IntegerField(null=False, default=1)
	month = models.IntegerField(null=False, default=1)
	year = models.IntegerField(null=False, default=1970)
	day = models.IntegerField(null=False, default=1)
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	update_time = models.DateTimeField('编辑时间', auto_now=True)

	class Meta:
		db_table = 'qa_sonar_result'


class OnlineBug(models.Model):
	product_id = models.CharField(null=False, max_length=20)
	project_id = models.CharField(null=False,  max_length=20)
	back_bugs = models.IntegerField(default=0)
	online_bugs = models.IntegerField(default=0)
	online_accidents = models.IntegerField(default=0)
	week = models.IntegerField(null=False, default=1)
	month = models.IntegerField(null=False, default=1)
	year = models.IntegerField(null=False, default=1970)
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	update_time = models.DateTimeField('编辑时间', auto_now=True)
	is_delete = models.IntegerField('删除状态', choices=((0, '否'), (1, '是')), default=0)

	class Meta:
		db_table = 'qa_online_bug'


class TestCase(models.Model):
	product_id = models.CharField(null=False, max_length=20)
	project_id = models.CharField(null=False,  max_length=20)
	iterable_name = models.CharField(null=False, max_length=20)
	main_tasks = models.CharField(null=False, max_length=20)
	test_cases_url = models.URLField(null=False, unique=True, max_length=200)
	# cases_num = models.IntegerField('用例条数', default=0)
	test_user = models.CharField(max_length=20)
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	update_time = models.DateTimeField('编辑时间', auto_now=True)
	is_delete = models.IntegerField('删除状态', choices=((0, '否'), (1, '是')), default=0)

	class Meta:
		db_table = 'qa_test_cases'


class TestReport(models.Model):
	product_id = models.CharField(null=False, max_length=20)
	project_id = models.CharField(null=False, max_length=20)
	iterable_name = models.CharField(null=False, max_length=20)
	mainTasks = models.CharField(null=False, max_length=20)
	test_report_url = models.URLField(null=False,  max_length=200)
	test_user = models.CharField(max_length=20)
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	update_time = models.DateTimeField('编辑时间', auto_now=True)
	is_delete = models.IntegerField('删除状态', choices=((0, '否'), (1, '是')), default=0)

	class Meta:
		db_table = 'qa_test_report'


class ProblemPlus(models.Model):
	# product_id = models.CharField(null=False, max_length=20)
	# project_id = models.CharField(null=False, max_length=20)
	description = models.CharField(null=False, max_length=100)
	resolution = models.CharField(null=False, max_length=100)
	avoid = models.CharField(null=False, max_length=100)
	create_user = models.CharField(max_length=20)
	keyword = models.CharField(null=False, max_length=50)
	case_info_url = models.CharField(null=False, max_length=200)
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	update_time = models.DateTimeField('编辑时间', auto_now=True)

	class Meta:
		db_table = 'qa_problem_plus'


class Services(models.Model):
	type_choices = ((1, 'Gradle'),
	                (2, 'Maven'),
	                (3, 'Node'),
	                (4, 'Python'),
	                (5, 'Go'),
	                (0, 'Others'))
	service_name = models.CharField(null=False, max_length=100)
	service_type = models.IntegerField('项目类型', choices=type_choices, default=0)
	product_id = models.CharField(null=False, max_length=20)
	project_id = models.CharField(null=False, max_length=20)
	coder = models.CharField(null=False, max_length=30)
	test_user_id = models.CharField(null=False, max_length=20)
	create_time = models.DateTimeField('创建时间', auto_now_add=True)
	update_time = models.DateTimeField('编辑时间', auto_now=True)
	is_delete = models.IntegerField('删除状态', choices=((0, '否'), (1, '是')), default=0)

	class Meta:
		db_table = 'qa_services'


