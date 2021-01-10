"""
用户权限的初始化
"""
from django.conf import settings


def init_permission(current_user, request):
    """
    初始化当前用户的权限及可见菜单，并存入session
    :param current_user: 当前用户对象
    :param request: 请求对象
    :return:
    """
    # 获取当前用户所有权限及信息
    permission_queryset = current_user.roles.filter(permissions__isnull=False).values("permissions__id",
                                                                                      "permissions__title",
                                                                                      "permissions__name",
                                                                                      "permissions__url",
                                                                                      "permissions__pid_id",
                                                                                      "permissions__pid__title",
                                                                                      "permissions__pid__name",
                                                                                      "permissions__pid__url",
                                                                                      "permissions__menu_id",
                                                                                      "permissions__menu__title",
                                                                                      "permissions__menu__icon",
                                                                                      ).distinct()

    menu_dict = {}
    permission_dict = {}

    for item in permission_queryset:

        # 录入用户权限
        permission_dict[item['permissions__name']] = {
            'id': item['permissions__id'],
            'title': item['permissions__title'],
            'url': item['permissions__url'],
            'pid': item['permissions__pid_id'],
            'p_title': item['permissions__pid__title'],
            'p_name': item['permissions__pid__name'],
            'p_url': item['permissions__pid__url'],
        }

        # 录入用户可见菜单（即可以做菜单的权限）
        menu_id = item['permissions__menu_id']
        if menu_id:
            menu_node = {
                'id': item['permissions__id'],
                'title': item['permissions__title'],
                'url': item['permissions__url']
            }
            # 构建两级字典的数据结构，以生成页面左侧的两级菜单
            if menu_id in menu_dict:
                menu_dict[menu_id]['children'].append(menu_node)
            else:
                menu_dict[menu_id] = {
                    'title': item['permissions__menu__title'],
                    'icon': item['permissions__menu__icon'],
                    'children': [
                        menu_node
                    ]
                }

    # 将信息存入session
    request.session[settings.PERMISSION_SESSION_KEY] = permission_dict
    request.session[settings.MENU_SESSION_KEY] = menu_dict
