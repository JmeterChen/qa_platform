from django.http import JsonResponse
from mypro.models import *
import datetime
from django.views.decorators.http import require_GET, require_POST
from django.core.paginator import Paginator
import json

# Create your views here.


# 封装分页函数:默认10条数据为一页
# data = [{},{}]
def my_page(data, page_num=1, page_size=10):
    if data:
        paginator = Paginator(data, page_size)
        pages = paginator.page(page_num)
        return pages
    else:
        return False


# 新增测试报告
@require_POST
def add_report(request):
    # 存储插入数据库的测试报告信息
    report = {}
    # 请求参数必含以下字段
    request_must_param = ['product_id', 'project_id', 'iter_name', 'main_func', 'report_url', 'test_user']
    # 用于存储POST请求中的请求参数
    request_param = []
    for key in request.POST.keys():
        request_param.append(key)
    if len(request_param) == 6:
        # 相等说明请求参数符合要求，即可进行下一步操作
        if request_must_param == request_param:
            now = datetime.datetime.now()
            now_date = now.strftime("%Y-%m-%d %H:%M:%S")
            product_id = request.POST['product_id']
            project_id = request.POST['project_id']
            iterable_name = request.POST['iter_name']
            main_func = request.POST['main_func']
            test_report_url = request.POST['report_url']
            test_user = request.POST['test_user']
            create_time = now_date
            update_time = now_date
            try:
                TestReport.objects.create(product_id=product_id, project_id=project_id, iterable_name=iterable_name,
                                          mainTasks=main_func, test_report_url=test_report_url, test_user=test_user,
                                          create_time=create_time, update_time=update_time)
            except:
                resp = {'code': 203, 'success': False, 'msg': '新增测试报告失败', 'data': {}}
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
                resp = {'code': 200, 'success': True, 'msg': '新增测试报告成功', 'data': {'0': report}}
        else:
            resp = {'code': 202, 'success': False, 'msg': '请求参数不对', 'data': {}}
    else:
        resp = {'code': 201, 'success': False, 'msg': '请求参数缺失', 'data': {}}
    return JsonResponse(resp)


# 查询测试报告
@require_GET
def get_reports(request):
    request_data = {}
    # 所有测试报告
    report_list = []
    # 单个测试报告
    report = {}
    # 判断请求参数是否为空,为空默认获取所有is_delete=0的测试报告
    if len(request.GET.keys()) == 0:
        # 倒叙获取
        reports = TestReport.objects.filter(is_delete='0').order_by('-id')
        for r in reports:
            print(r)
            report['id'] = r.id
            report['product_id'] = r.product_id
            report['project_id'] = r.project_id
            report['iter_name'] = r.iterable_name
            report['main_func'] = r.mainTasks
            report['report_url'] = r.test_report_url
            report['test_user'] = r.test_user
            report_list.append(report)
        print(report_list)
        pages = my_page(data=report_list)
        exit()
        for p in pages:
            print(p)
    else:
        pass
    """
    for key in request.GET.keys():
        print(key)
        exit()
        if key == 'product_id' and request.GET['product_id'] is not None:
            request_data['product_id'] = request.GET['product_id']
        if key == 'project_id' and value is not None:
            request_data['project_id'] = value
        if key == 'main_func' and value is not None:
            request_data['main_func'] = value
        if key == 'page_num':
            if value is None:
                request_data['page_num'] = 1  # 默认取第一页数据
            else:
                request_data['page_num'] = value
        if key == 'page_size':
            if value is None:
                request_data['page_size'] = 10  # 每页取10条数据
            else:
                request_data['page_size'] = value
    print(request_data)
    filter_data = {}
    page_data = {}
    # 对接收到的请求参数进行拆分:request_data仅包含产品线和项目，filter_data包含主要功能和分页参数
    if 'main_func' in request_data.keys():
        filter_data['main_func'] = request_data.pop('main_func')
    elif 'page_num' in filter_data.keys():
        page_data['page_num'] = request_data.pop('page_num')
    elif 'page_size' in request_data.keys():
        page_data['page_size'] = request_data.pop('page_size')
    # 默认取最新的十条数据
    if len(filter_data) == 0 and page_data == 0 and len(request_data) == 0:
        reports = TestReport.objects.all()
        print(reports)
    """
    """
    if len(project_id) == 0 and len(product_id) == 0 and len(main_func) == 0:
        data = TestReport.objects.filter(is_delete='0')
        resp = {'code': 200, 'msg': '查询条件为空，返回全部数据', 'data': data}
        return JsonResponse(resp)
    elif len(product_id) == 0 and len(project_id) == 0:
            data = TestReport.objects.filter(mainTasks__icontains=main_func)
            return data
        elif len(project_id) == 0 and len(main_func) == 0:
            param = {'product_id': product_id}
            data = TestReport.objects.filter(**param)
        elif len(project_id) == 0 and len(main_func) == 0:
            param = {'project_id': project_id}
            data = TestReport.objects.filter(**param)
        elif len(product_id) == 0:
            data = TestReport.objects.filter(project_id=project_id, mainTasks__icontains=main_func)
        elif len(project_id) == 0:
            data = TestReport.objects.filter(product_id=product_id, mainTasks__icontains=main_func)
        elif len(main_func) == 0:
            param = {'product_id': product_id, 'project_id': project_id}
            data = TestReport.objects.filter(**param)
        else:
            data = TestReport.objects.filter(product_id=product_id, project_id=project_id, mainTasks__icontains=main_func)
    return JsonResponse()
    """


# 修改测试报告
def update_report(request):
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
        if request.body:
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

                            try:
                                TestReport.objects.filter(id=report_id).update(**db_data)
                            except:
                                resp = {'code': 405, 'success': False, 'msg': '更新数据失败', 'data': {'report_id': report_id}}
                            else:
                                resp = {'code': 200, 'success': True, 'msg': '更新数据成功', 'data': {'report_id': report_id,
                                                                                                'info': db_data}}
                        else:
                            # 请求参数存在未规定的参数
                            resp = {'code': 404, 'success': False, 'msg': '请求参数不符合要求', 'data': {'report_id': report_id,
                                                                                                'info': db_data}}
                else:
                    # 请求参数中仅含测试报告id
                    resp = {'code': 403, 'success': False, 'msg': '请求参数缺失', 'data': {}}
            else:
                # 请求参数中不含测试报告id
                resp = {'code': 402, 'success': False, 'msg': '未传测试报告id', 'data': {}}
        else:
            # 无请求数据
            resp = {'code': 401, 'success': False, 'msg': '请求数据为空', 'data': {}}
    else:
        # 请求方法不对
        resp = {'code': 400, 'success': False, 'msg': "请求方式必须是PUT", 'data': {}}
    return JsonResponse(resp)


# 删除测试报告:将is_delete置为1
def delete_report(request):
    # 存储数据库中的测试报告id
    report_id_lst = []
    if request.method.lower() == 'delete':
        # 由于请求参数是放在body体中，所以先判断是否有请求数据
        if request.body:
            request_data = json.loads(request.body)
            # 请求删除的测试报告id
            report_id = request_data['id']
            # 获取库中所有的数据
            reports = TestReport.objects.all()
            for r in reports:
                report_id_lst.append(r.id)
            # 当测试报告id在数据库中才能进行删除操作
            if report_id in report_id_lst:
                for r in reports:
                    # 数据库中只有is_delete=0时才能被删除
                    if r.is_delete == 0:
                        try:
                            TestReport.objects.filter(id=report_id).update(is_delete='1')
                        except:
                            resp = {'code': 404, 'success': False, 'msg': "修改数据失败", 'data': {'report_id': report_id}}
                            return JsonResponse(resp)
                        else:
                            resp = {'code': 200, 'success': True, 'msg': '数据删除成功', 'data': {'report_id': report_id}}
                            return JsonResponse(resp)
                    else:
                        resp = {'code': 403, 'success': False, 'msg': '数据已被删除，无法进行删除操作', 'data': {'report_id': report_id}}
                        return JsonResponse(resp)
            else:
                # 说明数据不存在
                resp = {'code': 402, 'success': False, 'msg': "数据不存在", 'data': {'report_id': report_id}}
                return JsonResponse(resp)
        else:
            # 说明body中无请求数据
            resp = {'code': 401, 'success': False, 'msg': '请求数据为空', 'data': {}}
            return JsonResponse(resp)
    else:
        # 说明请求方法不是delete
        resp = {'code': 400, 'success': False, 'msg': "请求方式必须是DELETE", 'data': {}}
        return JsonResponse(resp)

