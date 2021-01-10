"""
反向解析带参数的URL，并保留原始URL参数信息
"""
from django.urls import reverse
from django.http import QueryDict


def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的URL（替代了模板中的URL）
    :param request:
    :param name: 带参数的原URL
    :return: 带_filter参数的新URL（原参数存在_filter中）
    """
    basic_url = reverse(name, args=args, kwargs=kwargs)

    # 当前URL中无参数
    if not request.GET:
        new_url = basic_url

    # 当前URL中有参数，把参数打包到_filter
    else:
        param = request.GET.urlencode()
        query_dict = QueryDict(mutable=True)
        query_dict['_filter'] = param
        new_url = "%s?%s" % (basic_url, query_dict.urlencode())

    return new_url


def memory_reverse(request, name, *args, **kwargs):
    """
    自定义反向生成URL，在URL中将原来搜索条件（_filter后的值，如：/menu/add/?_filter=mid%3D2），reverse生成原来的URL，如：/menu/list/?mid=2
    :param request:
    :param name: 带_filter的URL
    :param args:
    :param kwargs:
    :return: 带参数的原URL
    """
    base_url = reverse(name, args=args, kwargs=kwargs)
    param = request.GET.get('_filter')

    if param:
        base_url = "%s?%s" % (base_url, param,)

    return base_url
