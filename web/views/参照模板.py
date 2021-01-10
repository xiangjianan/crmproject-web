from stark.service.stark import StarkHandler
from stark.forms.base import StarkModelForm, StarkForm


class XxxModelForm(StarkModelForm):
    """
    ModelForm配置：...
    """
    pass


class XxxForm(StarkForm):
    """
    Form配置：...
    """
    pass


class XxxHandler(StarkHandler):
    """
    stark配置：...
    """

    # 获取自定义的ModelForm
    model_form_class = ...

    # 页面显示列配置：
    list_display = [
        ...
    ]

    def get_list_display(self, request, *args, **kwargs):
        """
        预留钩子：获取页面显示列
        :return:
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
            value.append(...)
        return value

    # 自定义html模板
    list_template = None
    add_template = None
    edit_template = None
    del_template = None

    # 分页配置：每页显示条数
    per_page_count = 10

    # 添加按钮配置：
    has_add_btn = False

    # 排序配置：
    order_list = [
        ...,
    ]

    # 允许的条件搜索范围：
    search_list = [
        ...,
    ]

    # 允许的组合搜索条件：
    search_group = [
        ...,
    ]

    # 允许的批量操作：
    action_list = [
        ...,
    ]

    def extra_urls(self):
        """
        预留钩子：新增URL
        :return:
        """
        patterns = [
            ...,
        ]
        return patterns

    def get_urls(self):
        """
        预留钩子：重写URL
        :return:
        """
        patterns = [
            ...,
        ]
        patterns.extend(self.extra_urls())
        return patterns
