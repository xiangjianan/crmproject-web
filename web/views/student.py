from django.urls import re_path
from django.utils.safestring import mark_safe
from django.urls import reverse

from stark.service.stark import StarkHandler, get_choice_text, get_m2m_text, Option
from stark.forms.base import StarkModelForm
from web import models

from .base import PermissionHandler


class StudentModelForm(StarkModelForm):
    """
    ModelForm配置：学生表
    """

    class Meta:
        model = models.Student
        fields = ['qq', 'mobile', 'emergency_contract', 'memo']


class StudentHandler(PermissionHandler, StarkHandler):
    """
    学生表：stark配置
    """
    # 获取自定义ModelForm
    model_form_class = StudentModelForm

    def display_score(self, obj=None, is_header=None, *args, **kwargs):
        """
        自定义的学生积分显示列
        :param obj:
        :param is_header:
        :return:
        """
        if is_header:
            return '积分管理'
        record_url = reverse('stark:web_scorerecord_list', kwargs={'student_id': obj.pk})
        return mark_safe('<a href="%s">%s</a>' % (record_url, obj.score))

    # 页面展示列：客户信息｜QQ号｜手机号｜紧急联系人电话｜已报班级｜状态｜积分管理｜编辑
    list_display = [
        'customer', 'qq', 'mobile', 'emergency_contract',
        get_m2m_text('已报班级', 'class_list'),
        get_choice_text('状态', 'student_status'),
        display_score,
    ]

    def get_list_display(self, request, *args, **kwargs):
        """
        预留钩子：进展示编辑列
        :return:
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
            value.append(type(self).display_edit)
        return value

    def get_urls(self):
        """
        预留钩子：重写URL（学生信息不允许被增删）
        :return:
        """
        patterns = [
            re_path(r'^list/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^edit/(?P<pk>\d+)/$', self.wrapper(self.edit_view), name=self.get_edit_url_name),
        ]

        patterns.extend(self.extra_urls())
        return patterns

    # 添加按钮配置：取消
    has_add_btn = False

    # 允许的条件搜索范围：姓名｜qq｜电话
    search_list = ['customer__name', 'qq', 'mobile', ]

    # 允许的组合搜索条件：班级
    search_group = [
        Option('class_list', text_func=lambda x: '%s-%s' % (x.school.title, str(x)))
    ]
