from collections import OrderedDict
from django import template
from django.conf import settings

from rbac.service import urls

register = template.Library()


@register.inclusion_tag('rbac/multi_menu.html')
def multi_menu(request):
    """
    创建页面左侧的可折叠二级菜单
    :param request:
    :return:
    """
    # 获取菜单字典，并使之有序
    menu_dict = request.session.get(settings.MENU_SESSION_KEY)
    key_list = sorted(menu_dict)

    # 空的有序字典
    ordered_dict = OrderedDict()

    for key in key_list:
        val = menu_dict[key]
        val['class'] = ''
        for per in val['children']:
            # 设置默认选中的二级菜单
            if per['id'] == request.current_selected_permission:
                per['class'] = 'active'
                val['class'] = ''
            else:
                per['class'] = ''
                val['class'] = ''
        ordered_dict[key] = val
    return {
        'menu_dict': ordered_dict
    }


@register.inclusion_tag('rbac/breadcrumb.html')
def breadcrumb(request):
    """
    根据当前页面生成路径导航
    :param request:
    :return:
    """
    print('request.current_breadcrumb_list', request.current_breadcrumb_list)
    return {
        'breadcrumb_list': request.current_breadcrumb_list
    }


@register.filter
def has_permission(request, name):
    """
    判断用户是否有访问当前URL的权限
    :param request:
    :param name: 可被Django反向解析成URL的唯一字符串
    :return:
    """
    permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
    if name in permission_dict:
        return True


@register.simple_tag
def memory_url(request, name, *args, **kwargs):
    """
    生成带有原搜索条件的URL（替代了模板中的url）
    :param request:
    :param name: 带参数的原URL
    :return: 带有原参数的新URL
    """
    return urls.memory_url(request, name, *args, **kwargs)
