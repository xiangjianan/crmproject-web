"""
自动获取项目中所有带name别名的URL
"""
import re
from collections import OrderedDict
from django.conf import settings
from django.utils.module_loading import import_string
from django.urls.resolvers import URLResolver, URLPattern


def check_url_exclude(url):
    """
    自动获取项目中所有URL时，排除一些特定的URL
    :param url:
    :return:
    """
    for regex in settings.AUTO_DISCOVER_EXCLUDE:
        if re.match(regex, url):
            return True


def recursion_urls(pre_namespace, pre_url, urlpatterns, url_ordered_dict):
    """
    递归的获取URL
    :param pre_namespace: namespace前缀，以后用于拼接name
    :param pre_url: URL前缀，以后用于拼接URL
    :param urlpatterns: 路由关系列表
    :param url_ordered_dict: 用于保存递归中获取的所有路由
    :return:
    """
    for item in urlpatterns:
        # 非路由分发，直接将路由添加到url_ordered_dict
        if isinstance(item, URLPattern):
            # 没有name属性，不添加
            if not item.name:
                continue
            # 加namespace前缀
            if pre_namespace:
                name = "%s:%s" % (pre_namespace, item.name)
            else:
                name = item.name
            # 加URL前缀（Django3.0以上版本不支持RegexURLPattern的_regex属性，使用URLPattern的pattern属性）
            url = pre_url + str(item.pattern)
            url = url.replace('^', '').replace('$', '')
            # 排除白名单URL
            if check_url_exclude(url):
                continue
            url_ordered_dict[name] = {'name': name, 'url': url}

        # 是路由分发，做递归操作
        elif isinstance(item, URLResolver):
            # 父级有namespace
            if pre_namespace:
                # 当前级有namespace
                if item.namespace:
                    namespace = "%s:%s" % (pre_namespace, item.namespace,)
                # 当前级无namespace
                else:
                    namespace = pre_namespace
            # 父级无namespace
            else:
                # 当前级有namespace
                if item.namespace:
                    namespace = item.namespace
                # 当前级无namespace
                else:
                    namespace = None
            # 加URL前缀
            url = pre_url + str(item.pattern)
            url = url.replace('^', '').replace('$', '')
            # 排除白名单URL
            if check_url_exclude(url):
                continue
            recursion_urls(namespace, url, item.url_patterns, url_ordered_dict)


def get_all_url_dict():
    """
    获取项目中所有的URL（必须有name别名）
    :return:
    """
    url_ordered_dict = OrderedDict()

    # from project import urls
    md = import_string(settings.ROOT_URLCONF)

    # 递归获取所有路由
    recursion_urls(None, '/', md.urlpatterns, url_ordered_dict)

    return url_ordered_dict
