# Create your views here.

from django.http import JsonResponse
from django.core.paginator import Paginator
from mypro.models import ProblemPlus
from datetime import datetime
from django.db.models import Q
import json

default_page_num = 1
default_page_size = 10


def add_bat_problem_guide(request):
    u"""
    批量新增经典问题指引记录
    :param request:
    :return:
    """
    # 接收参数
    params_list = json.loads(request.body.decode())

    suc_count = 0
    fai_count = 0

    for params in params_list:
        create_user = params.get('create_user', '')  # 创建人
        description = params.get('description', '')  # 问题描述
        resolution = params.get('resolution', '')  # 解决方案
        avoid = params.get('avoid', '')  # 规避方案
        keyword = params.get('keyword', '')  # 问题关键词
        case = params.get('case', '')  # 案例

        if create_user and description:
            # 插入数据库
            try:
                ProblemPlus.objects.create(
                    **{"create_user": create_user, "description": description, "resolution": resolution,
                       "avoid": avoid, "keyword": keyword, "case_info_url": case,
                       "create_time": datetime.now(), "update_time": datetime.now()})
                suc_count += 1
            except Exception as e:
                print(e)
                fai_count += 1
        else:
            fai_count += 1

    result = {'code': '200', 'msg': 'success', 'success_count': suc_count, 'fail_count': fai_count}
    return JsonResponse(result)


def add_problem_guide(request):
    u"""
    新增经典问题指引记录
    :param request:
    :return:
    """
    # 接收参数
    params = json.loads(request.body.decode())
    create_user = params.get('create_user', '')  # 创建人
    description = params.get('description', '')  # 问题描述
    resolution = params.get('resolution', '')  # 解决方案
    avoid = params.get('avoid', '')  # 规避方案
    keyword = params.get('keyword', '')  # 问题关键词
    case = params.get('case', '')  # 案例

    # 判读是否有必填参数
    if create_user and description:
        # 插入数据库

        try:
            add_information = ProblemPlus.objects.create(
                **{"create_user": create_user, "description": description, "resolution": resolution,
                   "avoid": avoid, "keyword": keyword, "case_info_url": case,
                   "create_time": datetime.now(), "update_time": datetime.now()})
            result = {
                'code': 200,
                'msg': 'success',
                'data': {
                    'id': add_information.id,
                    'create_user': add_information.create_user,
                    'description': add_information.description,
                    'resolution': add_information.resolution,
                    'avoid': add_information.avoid,
                    'keyword': add_information.keyword,
                    'case': add_information.case_info_url,
                    'create_time': add_information.create_time,
                    'update_time': add_information.update_time,
                }
            }
        except Exception as e:
            result = {"code": 50001, 'msg': f"添加数据出现异常：{e}"}
            print(e)
    else:
        result = {'code': 50003, 'msg': '缺少必填参数！'}

    return JsonResponse(result)


def edit_problem_guide(request):
    u"""
    编辑经典问题指引记录
    :param request:
    :return:
    """
    result = {
        'code': '200',
        'msg': 'success'
    }

    if request.method != 'PUT':
        result = {'code': 50002, 'msg': '请求方式错误！'}
        return JsonResponse(result)

    # 接收参数
    params = json.loads(request.body.decode())
    p_id = params.get('id')  # 问题指引id
    create_user = params.get('create_user')  # 问题指引编辑人
    description = params.get('description')  # 问题描述
    resolution = params.get('resolution')  # 解决方案
    avoid = params.get('avoid')  # 规避方案
    keyword = params.get('keyword')  # 问题关键词
    case = params.get('case')  # 案例

    # 判断是否有必填参数
    if p_id and create_user:
        # 更新数据库
        try:
            # obj = {"id": p_id, "create_user": create_user, "description": description, "resolution": resolution,
            #        "avoid": avoid, "keyword": keyword, "case_info_url": case, "update_time": datetime.now()}

            obj = {"create_user": create_user, "update_time": datetime.now()}

            if None is not description:
                obj['description'] = description

            if None is not resolution:
                obj['resolution'] = resolution

            if None is not avoid:
                obj['avoid'] = avoid

            if None is not keyword:
                obj['keyword'] = keyword

            if None is not case:
                obj['case_info_url'] = case

            ProblemPlus.objects.filter(id=p_id).update(**obj)
        except Exception as e:
            result = {"code": 50001, 'msg': f"更新数据出现异常：{e}"}
            print(e)
    else:
        result = {'code': 50003, 'msg': '缺少必填参数！'}

    return JsonResponse(result)


def delete_problem_guide(request):
    u"""
    删除经典问题指引记录
    :param request:
    :return:
    """
    result = {
        'code': '200',
        'msg': 'success'
    }

    params = json.loads(request.body.decode())
    p_id = params.get('id')  # 问题指引id
    if p_id:
        try:

            ProblemPlus.objects.filter(id=p_id).delete()
        except Exception as e:
            result = {"code": 50001, 'msg': f"更新数据出现异常：{e}"}
            print(e)
    else:
        result = {'code': 50003, 'msg': '缺少必填参数！'}
    return JsonResponse(result)


def search_problem_guide(request):
    u"""
    查询经典问题指引记录
    :param request:
    :return:
    """
    params = json.loads(request.body.decode())
    description = params.get('description')  # 问题描述
    keyword = params.get('keyword')  # 问题关键词
    page_number = params.get('page_number', default_page_num)  # 页码
    page_size = params.get('page_size', default_page_size)  # 分页大小

    con = Q()
    if description:
        con.add(Q(description__icontains=description), 'AND')

    if keyword:
        con.add(Q(keyword__icontains=keyword), 'AND')

    search_information = ProblemPlus.objects.filter(con).values(
        "description", "resolution", "avoid", "keyword", "case_info_url"
    )

    # 分页
    pgt = Paginator(search_information, page_size)
    datas = pgt.page(page_number)

    result = {
        'code': '200',
        'msg': 'success',
        'page_number': page_number,
        'page_total': pgt.num_pages,
        'data': list(datas)
    }
    return JsonResponse(result)
