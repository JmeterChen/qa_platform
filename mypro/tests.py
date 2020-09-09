from django.test import TestCase

# Create your tests here.


import os
import django
import time


os.environ.setdefault('DJANGO_SETTING_MODULE', 'MyDjango.settings')
django.setup()


from mypro.models import *
import random

App_list = []
Project_list = []
Iterable_list = []
User_list = []
Devices_list = []
OnlineBug_list = []
TestCase_list = []
TestReport_list = []
ProblemPlus_list = []
Services_list = []


for i in range(100):
	
	num = random.randint(1, 99)
	
	product_id = str(round(time.time()))
	product_name = f'ABCD{i}'
	project_name = f'XYZ{i}'
	back_bugs = random.randint(1, 30)
	online_bugs = random.randint(0, 50)
	online_accidents = random.randint(0, 10)
	project_id = f'1{product_id}{online_accidents}'
	count_time = f'2020-07-{back_bugs}'
	test_user_id = f'20{back_bugs}{online_bugs}0'
	cases_num = f'{(i+back_bugs+online_bugs+online_accidents)}'
	bugs_num = random.randint(1, 150)
	user_id = f'{i+3}{online_bugs}'
	user_name = f'ab{i}xy{back_bugs}'
	email = f'{user_name}@qq.com'
	phone_number = f'133{random.randint(10000000, 99999999)}'
	device_id = f'{i+random.randint(10,99)}{i}'
	device_name = f'qwer{i}'
	test_report_url = f'www.{product_name}.com'
	service_name = f'a{i}b{back_bugs}c{online_bugs}'
	
	obj1 = App(
		product_id=product_id,
		product_name=product_name
	)
	
	App_list.append(obj1)
	
	obj2 = Project(
		project_id=project_id,
		project_name=project_name,
		test_user_id=test_user_id,
		product_id=product_id
	)
	
	Project_list.append(obj2)
	
	obj3 = Iterable(
		project_id=project_id,
		project_name=project_name,
		product_id=product_id,
		test_user_id=test_user_id,
		cases_num=cases_num,
		bugs_num=bugs_num
	)
	
	Iterable_list.append(obj3)
	
	obj4 = User(
		user_id=user_id,
		user_name=user_name,
		email=email,
		phone_number=phone_number,
		product_id=product_id,
		project_id=project_id
	)
	
	User_list.append(obj4)
	
	obj5 = Devices(
		device_id=device_id,
		device_name=device_name,
		system_name=product_id,
		device_model=product_id,
		system_version=product_id,
		user_id=user_id,
		purchase_date=count_time,
		remark=product_id,
	)
	
	Devices_list.append(obj5)
	
	obj6 = OnlineBug(
		product_id=product_id,
		project_id=project_id,
		back_bugs=back_bugs,
		online_bugs=online_bugs,
		online_accidents=online_accidents
	)
	
	OnlineBug_list.append(obj6)
	
	obj7 = TestCase(
		product_id=product_id,
		project_id=project_id,
		iterable_name=f'q{i}wer',
		main_tasks=f'{i*2}q1w2er{i}',
		test_cases_url=test_report_url,
		cases_num=cases_num,
		test_user=user_id
	)
	
	TestCase_list.append(obj7)
	
	obj8 = TestReport(
		product_id=product_id,
		project_id=project_id,
		iterable_name=f'q{i}wer',
		mainTasks=f'{i*2}q1w2er{i}',
		test_report_url=test_report_url,
		test_user=user_id,
	)
	
	TestReport_list.append(obj8)
	
	obj9 = ProblemPlus(
		product_id=product_id,
		project_id=project_id,
		description=f'q{i}wer',
		resolution=f'{i*2}q1w2er{i}',
		avoid=product_name,
		create_user=user_id,
		case_info_url=test_report_url,
		keyword=product_name
	)
	
	ProblemPlus_list.append(obj9)
	
	obj10 = Services(
		service_name=service_name,
		service_type=f'{random.randint(0,5)}',
		product_id=product_id,
		project_id=project_id,
		coder=product_name,
		test_user=user_id
	)
	
	Services_list.append(obj10)


if __name__ == '__main__':
	"""
	自己调试的时找准自己需求相关的表哈！！！！
	"""
	App.objects.bulk_create(App_list)
	Iterable.objects.bulk_create(Iterable_list)
	User.objects.bulk_create(User_list)
	Devices.objects.bulk_create(Devices_list)
	OnlineBug.objects.bulk_create(OnlineBug_list)
	TestCase.objects.bulk_create(TestCase_list)
	TestReport.objects.bulk_create(TestReport_list)
	ProblemPlus.objects.bulk_create(ProblemPlus_list)
	Services.objects.bulk_create(Services_list)
	Project.objects.bulk_create(Project_list)
	# obj = Services.objects.filter(product_id=222).filter(project_id=1).values("service_name")
	# print(list(obj))





