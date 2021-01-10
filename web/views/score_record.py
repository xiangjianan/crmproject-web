from django.urls import re_path

from stark.service.stark import StarkHandler
from stark.forms.base import StarkModelForm
from web import models

from .base import PermissionHandler


class ScoreModelForm(StarkModelForm):
    """
    ModelForm配置：积分记录表
    """

    class Meta:
        model = models.ScoreRecord
        fields = ['content', 'score']


class ScoreHandler(PermissionHandler, StarkHandler):
    """
    stark配置：积分记录表
    """
    # 获取自定义ModelForm
    model_form_class = ScoreModelForm

    # 页面展示列：评分理由｜分值｜执行人
    list_display = ['content', 'score', 'user']

    def get_list_display(self, request, *args, **kwargs):
        """
        预留钩子：取消默认编辑删除列
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
        return value

    def get_urls(self):
        """
        预留钩子：URL重写
        :return:
        """
        patterns = [
            re_path(r'^list/(?P<student_id>\d+)/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^add/(?P<student_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns

    def get_queryset(self, request, *args, **kwargs):
        """
        预留钩子：获取指定学生的分数
        :param request:
        :return:
        """
        student_id = kwargs.get('student_id')
        return self.model_class.objects.filter(student_id=student_id)

    def save(self, request, form, is_update, *args, **kwargs):
        """
        钩子方法：保存前增加业务处理
        :param request:
        :param form:
        :param is_update:
        :param args:
        :param kwargs:
        :return:
        """
        student_id = kwargs.get('student_id')
        current_user_id = request.session['user_info']['id']

        # 设置默认值
        form.instance.student_id = student_id
        form.instance.user_id = current_user_id
        form.save()

        # 分数处理
        score = form.instance.score
        if score > 0:
            form.instance.student.score += abs(score)
        else:
            form.instance.student.score -= abs(score)
        form.instance.student.save()
