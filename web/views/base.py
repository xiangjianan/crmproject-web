from crmProject import settings


class PermissionHandler(object):
    """
    stark配置的基类：权限的粒度控制到按钮
    """

    def get_add_btn(self, request, *args, **kwargs):
        """
        预留钩子：根据用户权限，粒度控制到添加按钮的显示
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        get_add_url_name = 'stark:%s' % self.get_add_url_name
        if get_add_url_name not in permission_dict:
            return None
        return super(PermissionHandler, self).get_add_btn(request, *args, **kwargs)

    def get_list_display(self, request, *args, **kwargs):
        """
        预留钩子：根据用户权限，粒度控制到编辑删除按钮的显示
        :return:
        """
        value = []
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        get_edit_url_name = 'stark:%s' % self.get_edit_url_name
        get_del_url_name = 'stark:%s' % self.get_del_url_name
        if self.list_display:
            value.extend(self.list_display)
            # 当前用户有编辑和删除权限
            if get_edit_url_name in permission_dict and get_del_url_name in permission_dict:
                value.append(type(self).display_edit_del)
            # 当前用户只有编辑权限
            elif get_edit_url_name in permission_dict:
                value.append(type(self).display_edit)
            # 当前用户只有删除权限
            elif get_del_url_name in permission_dict:
                value.append(type(self).display_del)
        return value
