from django.shortcuts import render

from . import models

# Create your views here.


def list(request):
    '''
    笑话集列表
    :param request:
    :return:
    '''
    jokes = models.Jokeji.objects.all()[:10]
    return render(request, "jokeji/list.html", {"jokes": jokes})


def detail(request, id):
    '''
    商品详情页
    :param request:
    :param g_id:
    :return:
    '''
    joke = models.Jokeji.objects.get(pk=id)
    return render(request, "jokeji/detail.html", {"joke": joke})

