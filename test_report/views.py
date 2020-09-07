from django.http import JsonResponse
from mypro.models import *
import datetime
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
import json
import urllib.parse
# Create your views here.


# 新增测试报告
@require_POST
def add_report(request):
    # 存储请求参数
    db_data = {}
    # 获取请求头中的操作人：由于信息经过url编码了，故需要解码
    oper_user_name = urllib.parse.unquote(request.META.get('HTTP_OPERATOR', ''))  # 不设置默认值会报错
    # 获取请求参数
    if request.body:
        res = json.loads(request.body.decode())
    else:
        res = {}
    # 存储成功插入数据库的测试报告信息
    report = {}
    # 请求参数必含以下字段
    request_must_param = ['product_id', 'project_id', 'iter_name', 'main_func', 'report_url', 'test_user']
    # 用于存储POST请求中的请求参数
    if oper_user_name and res:
        for v in request_must_param:
            if v in res.keys():
                db_data[v] = res[v]
            else:
                resp = {'code': 4002, 'success': False, 'msg': '请求参数字段不符合要求', 'data': {}}
                return JsonResponse(resp)
        db_data['operator'] = oper_user_name
        now = datetime.datetime.now()
        now_date = now.strftime("%Y-%m-%d %H:%M:%S")
        db_data['create_time'] = now_date
        db_data['update_time'] = now_date
        try:
            TestReport.objects.create(product_id=db_data['product_id'], project_id=db_data['project_id'],
                                      iterable_name=db_data['iter_name'], mainTasks=db_data['main_func'],
                                      test_report_url=db_data['report_url'], test_user=db_data['test_user'],
                                      create_time=db_data['create_time'], update_time=db_data['update_time'],
                                      operator=db_data['operator'])
        except:
            resp = {'code': 4003, 'success': False, 'msg': '新增测试报告失败', 'data': {}}
        else:
            # 取数据库最新的一条数据：返回的是一个object对象
            insert_data = TestReport.objects.order_by('-id')[0]
            report['id'] = insert_data.id
            report['product_id'] = insert_data.product_id
            report['project_id'] = insert_data.project_id
            report['iter_name'] = insert_data.iterable_name
            report['main_func'] = insert_data.mainTasks
            report['report_url'] = insert_data.test_report_url
            report['test_user'] = insert_data.test_user
            report['create_time'] = insert_data.create_time
            report['update_time'] = insert_data.update_time
            report['operator'] = insert_data.operator
            resp = {'code': 2000, 'success': True, 'msg': '新增测试报告成功', 'data': report}
    else:
        resp = {'code': 4001, 'success': False, 'msg': '无操作人信息或无请求数据', 'data': {}}
    return JsonResponse(resp)


# 查询测试报告
@require_GET
def get_reports(request):
    # 查询条件:产品线和项目组
    query_param = {}
    query = {}
    product_id = request.GET.get('product_id', '')
    project_id = request.GET.get('project_id', '')
    main_func = request.GET.get('main_func', '')
    page_num = request.GET.get('page_num', 1)
    page_size = request.GET.get('page_size', 10)
    if product_id:
        query_param['product_id'] = product_id
    if project_id:
        query_param['project_id'] = project_id
    # 查询条件为product_id,project_id,main_func
    if len(query_param) > 0 and main_func:
        query_data = TestReport.objects.filter(**query_param, mainTasks__contains=main_func, is_delete='0').\
            order_by('-update_time')
    # 查询条件为main_func
    elif len(query_param) == 0 and main_func:
        query_data = TestReport.objects.filter(mainTasks__contains=main_func, is_delete='0').order_by('-update_time')
    # 查询条件为product_id, project_id
    elif len(query_param) > 0 and len(main_func) == 0:
        query_data = TestReport.objects.filter(**query_param, is_delete='0').order_by('-update_time')
    # 查询条件为空
    else:
        query_data = TestReport.objects.filter(is_delete='0').order_by('-update_time')
    # 查询结果不为空
    if query_data:
        try:
            # 若page_size为负数，则产生的页码也是负数
            page = Paginator(query_data, page_size)
        except:
            # page_size的值非正整数
            query['main_func'] = main_func
            query['page_num'] = page_num
            query['page_size'] = page_size
            resp = {'code': 4001, 'success': False, 'msg': '参数page_size应为非0整数', 'data': {'query': query}}
        else:
            # 最大页码
            page_num_max = page.num_pages
            if page_num_max < 0:
                resp = {'code': 4002, 'success': False, 'msg': '参数page_size为负数', 'data': {}}
            elif int(page_num) < 1:
                resp = {'code': 4002, 'success': False, 'msg': '参数page_num为零或负数', 'data': {}}
            elif page_num_max < int(page_num):
                resp = {'code': 4002, 'success': False, 'msg': '当前页码不存在', 'data': {}}
            else:
                # 说明page_num在最大页码范围内
                page_data = page.page(page_num)
                # 获取对应页码的数据:得到的是一个querySet
                db_data = page_data.object_list
                # 查出的测试报告集
                result_lst = []
                page_info = {}
                for r in db_data:
                    # 返回的数据为querySet[{}]格式
                    product_info = App.objects.filter(product_id=r.product_id).values('product_name')
                    project_info = Project.objects.filter(project_id=r.project_id).values('project_name')
                    product_name = ''
                    project_name = ''
                    if project_info:
                        project_name = project_info[0]['project_name']
                    if product_info:
                        product_name = product_info[0]['product_name']
                    # 单个测试报告数据
                    result = {'id': r.id, 'product_id': r.product_id, 'product_name': product_name,
                              'project_id': r.project_id, 'project_name': project_name,
                              'iter_name': r.iterable_name, 'main_func': r.mainTasks, 'report_url': r.test_report_url,
                              'test_user': r.test_user, 'operator': r.operator}
                    # result['create_time'] = r.create_time
                    # result['update_time'] = r.update_time
                    result_lst.append(result)
                # 当前页码
                page_info['num'] = page_num
                # 每页显示多少数据
                page_info['size'] = page_size
                # 最大分页数
                page_info['max_page_num'] = page_num_max
                # 查询总数
                page_info['count'] = page.count
                # 当前页码，每页显示数据量，查询总数
                # page_info_dict['page_info'] = page_info
                resp = {'code': 2000, 'success': True, 'msg': '查询数据成功', 'data': result_lst, 'page_info': page_info}
    else:
        # 查询结果为空
        query['product_id'] = product_id
        query['project_id'] = project_id
        query['main_func'] = main_func
        query['page_num'] = page_num
        query['page_size'] = page_size
        resp = {'code': 2000, 'success': True, 'msg': '查询结果为空', 'data': {'query': query}}
    return JsonResponse(resp)


# 修改测试报告
def update_report(request):
    # 获取请求头中的操作人：由于信息经过url编码了，故需要解码
    oper_user_name = urllib.parse.unquote(request.META.get('HTTP_OPERATOR', ''))  # 不设置默认值会报错
    # 修改字段最多的情况
    request_max_param = ['product_id', 'project_id', 'iter_name', 'main_func', 'report_url', 'test_user']
    # 存储请求参数的key：report_id除外
    db_keys = []
    # 测试报告id
    report_id = None
    # 真正的请求参数
    db_data = {}
    if request.method.lower() == 'put':
        # 判断请求体中是否有数据
        if request.body and oper_user_name:
            request_data = json.loads(request.body)
            # 将请求参数中与数据库字段不一致的修改成一致
            for key, value in request_data.items():
                if key == 'iter_name':
                    db_data['iterable_name'] = value
                elif key == 'main_func':
                    db_data['mainTasks'] = value
                elif key == 'report_url':
                    db_data['test_report_url'] = value
                else:
                    db_data[key] = value
            # db_data存储除测试报告id外的数据
            for key in list(db_data.keys()):
                if key == 'report_id':
                    report_id = db_data['report_id']
                    db_data.pop('report_id')
                else:
                    db_keys.append(key)
            # 有测试报告id才能进行修改数据
            if report_id:
                if len(db_keys) > 0:
                    for key in db_keys:
                        if key in request_max_param:
                            now = datetime.datetime.now()
                            db_data['update_time'] = now.strftime("%Y-%m-%d %H:%M:%S")
                            db_data['operator'] = oper_user_name
                            try:
                                TestReport.objects.filter(id=report_id).update(**db_data)
                            except:
                                resp = {'code': 4005, 'success': False, 'msg': '更新数据失败', 'data': {'report_id': report_id,
                                                                                                  'info': db_data}}
                            else:
                                resp = {'code': 2000, 'success': True, 'msg': '更新数据成功', 'data': {'report_id': report_id,
                                                                                                 'info': db_data}}
                        else:
                            # 请求参数存在未规定的参数
                            resp = {'code': 4004, 'success': False, 'msg': '请求参数不符合要求', 'data': {'report_id': report_id,
                                                                                                 'info': db_data}}
                else:
                    # 请求参数中仅含测试报告id
                    resp = {'code': 4003, 'success': False, 'msg': '请求参数缺失', 'data': {}}
            else:
                # 请求参数中不含测试报告id
                resp = {'code': 4002, 'success': False, 'msg': '未传测试报告id', 'data': {}}
        else:
            # 无请求数据
            resp = {'code': 4001, 'success': False, 'msg': '无操作人信息或无请求数据', 'data': {}}
    else:
        # 请求方法不对
        resp = {'code': 4000, 'success': False, 'msg': "请求方式必须是PUT", 'data': {}}
    return JsonResponse(resp)


# 删除测试报告:将is_delete置为1
@require_GET
def delete_report(request):
    # 获取请求头中的操作人：由于信息经过url编码了，故需要解码
    oper_user_name = urllib.parse.unquote(request.META.get('HTTP_OPERATOR', ''))  # 不设置默认值会报错
    # 存储数据库中的测试报告id
    report_id_lst = []
    report_id = request.GET.get('report_id', '')
    # 由于report_id是字符串类型，故需要判断字符是否仅含数字，若不是仅有数字组成，则默认值为0
    if not report_id.isdigit():
        report_id = 0
    # 获取库中所有数据
    reports = TestReport.objects.all()
    for r in reports:
        report_id_lst.append(r.id)
    # 当测试报告id在数据库中才能进行删除操作
    if int(report_id) in report_id_lst:
        report = TestReport.objects.filter(id=report_id)
        # 数据库中只有is_delete=0时才能被删除
        if report[0].is_delete == 0:
            now = datetime.datetime.now()
            update_time = now.strftime("%Y-%m-%d %H:%M:%S")
            try:
                TestReport.objects.filter(id=report_id).update(is_delete='1', operator=oper_user_name,
                                                               update_time=update_time)
            except:
                resp = {'code': 4003, 'success': False, 'msg': "修改数据失败", 'data': {'report_id': report_id}}
            else:
                resp = {'code': 2000, 'success': True, 'msg': '数据删除成功', 'data': {'report_id': report_id}}
        else:
            resp = {'code': 4002, 'success': False, 'msg': '数据已被删除，无法进行删除操作', 'data': {'report_id': report_id}}
    else:
        # 说明数据不存在
        resp = {'code': 4001, 'success': False, 'msg': "数据不存在", 'data': {'report_id': report_id}}
    return JsonResponse(resp)

