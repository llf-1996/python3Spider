from django.shortcuts import render
from django.core.paginator import Paginator

from . import models
from django.conf import settings


# Create your views here.


def list(request, pageNow=1):
    '''
    笑话集列表
    :param request:
    :return:
    '''
    # 分页
    # 从 setting 配置文件中获取指定的每页显示的条数
    pageSize = settings.PAGESIZE
    # 获取所有笑话条数
    jokes = models.Jokeji.objects.all()
    # 构建Paginator对象
    # 参数：数据列表，每页显示条数
    paginator = Paginator(jokes, pageSize)
    # 获取分页对象的列表，参数是当前页码
    page = paginator.page(pageNow)

    # 计算列表页中分页的页数列表
    pageNow = int(pageNow)
    remainder = pageNow % 5
    if remainder:
        page_list_start = pageNow - remainder + 1
    else:
        page_list_start = pageNow - 4
    page_list_end = page_list_start + 5
    if page_list_end > paginator.num_pages + 1:
        page_list_end = paginator.num_pages + 1
    page_list = range(page_list_start, page_list_end)
    context = {
        "page": page,
        "pageSize": pageSize,
        'page_list': page_list,
    }
    return render(request, "jokeji/list.html", context)


def detail(request, id):
    '''
    商品详情页
    :param request:
    :param g_id:
    :return:
    '''
    joke = models.Jokeji.objects.get(pk=id)
    return render(request, "jokeji/detail.html", {"joke": joke})

