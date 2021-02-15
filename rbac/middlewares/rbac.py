import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect
from django.conf import settings


class RbacMiddleware(MiddlewareMixin):
    """
    自定义的rbac中间件
    """

    def process_request(self, request):
        """
        收到用户请求后，在路由分发前，对用户权限进行校验
        :param request:
        :return:
        """

        url_record = [{'title': '首页', 'url': '/index/'}, ]  # 路径导航
        url_current = 0  # 当前访问URL所属的二级菜单，定位active使用

        # 白名单URL无需权限校验，直接通过中间件
        current_url = request.path_info
        for reg in settings.PERMISSION_VALID_URL_LIST:
            if re.match(reg, current_url):
                request.current_breadcrumb_list = url_record
                request.current_selected_permission = url_current
                return None

        # 检查该用户是否登录
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if not permission_dict:
            # return HttpResponse('未获取到用户权限信息，请登录！')
            return redirect('/login/')

        # 需要登录，但无需权限校验
        for url in settings.NO_PERMISSION_URL_LIST:
            if re.match(url, request.path_info):
                request.current_breadcrumb_list = url_record
                request.current_selected_permission = url_current
                return None

        # 遍历用户权限URL，并校验
        for name, item in permission_dict.items():
            title = item['title']
            url = item['url']
            regex = "^%s$" % (url,)
            # 权限校验通过
            if re.match(regex, current_url):
                pid = item['pid']
                p_title = item['p_title']
                p_url = item['p_url']
                if pid:
                    url_record.extend([
                        {'title': p_title, 'url': p_url},
                        {'title': title, 'url': url, 'class': 'active'}
                    ])
                else:
                    url_record.append(
                        {'title': title, 'url': url, 'class': 'active'}
                    )
                url_current = pid or item['id']
                request.current_breadcrumb_list = url_record
                request.current_selected_permission = url_current
                return None
        else:
            # return HttpResponse('无权访问')
            return redirect('/index/')
