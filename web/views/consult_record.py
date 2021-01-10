from django.utils.safestring import mark_safe
from django.urls import re_path
from django.shortcuts import HttpResponse

from stark.service.stark import StarkHandler
from stark.forms.base import StarkModelForm
from web import models

from .base import PermissionHandler


class ConsultRecordModelForm(StarkModelForm):
    """
    ModelForm配置：跟进记录表
    """

    class Meta:
        model = models.ConsultRecord
        fields = ['note', ]


class ConsultRecordHandler(PermissionHandler, StarkHandler):
    """
    stark配置：跟进记录表
    """
    # 获取自定义ModelForm
    model_form_class = ConsultRecordModelForm

    # 页面显示列：跟进内容｜课程顾问｜日期｜自定义编辑删除操作
    list_display = [
        'note', 'consultant', 'date',
    ]

    def display_edit_del(self, obj=None, is_header=None, *args, **kwargs):
        """
        预留钩子：自定义编辑删除列
        :param obj:
        :param is_header:
        :param args:
        :param kwargs:
        :return:
        """
        if is_header:
            return '操作'
        customer_id = kwargs.get('customer_id')
        tpl = """
            <div class="pull-right">
                <a class="text-primary" style="margin-right: 10px;" href="%s">
                    编辑
                </a>
                <a class="text-danger" href="%s">
                    删除
                </a>
            </div>""" % (self.reverse_edit_url(pk=obj.pk, customer_id=customer_id),
                         self.reverse_del_url(pk=obj.pk, customer_id=customer_id))
        return mark_safe(tpl)

    # 自定义html模板
    list_template = 'consult_record.html'

    def get_urls(self):
        """
        预留钩子：重写URL
        :return:
        """
        patterns = [
            re_path(r'^list/(?P<customer_id>\d+)/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^add/(?P<customer_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_url_name),
            re_path(r'^edit/(?P<customer_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.edit_view),
                    name=self.get_edit_url_name),
            re_path(r'^del/(?P<customer_id>\d+)/(?P<pk>\d+)/$', self.wrapper(self.del_view),
                    name=self.get_del_url_name),
        ]

        patterns.extend(self.extra_urls())
        return patterns

    def get_queryset(self, request, *args, **kwargs):
        """
        预留钩子：获取当前用户指定私有客户的跟进记录
        :param request:
        :param args:
        :param kwargs: 指定私有客户
        :return:
        """
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        return self.model_class.objects.filter(customer_id=customer_id, customer__consultant_id=current_user_id)

    def save(self, request, form, is_update, *args, **kwargs):
        """
        钩子方法：保存前为跟进人和跟进客户设置默认值
        :param request:
        :param form:
        :param is_update:
        :param args:
        :param kwargs:
        :return:
        """
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']

        object_exists = models.Customer.objects.filter(id=customer_id, consultant_id=current_user_id).exists()
        if not object_exists:
            return HttpResponse('非法操作')

        if not is_update:
            form.instance.customer_id = customer_id
            form.instance.consultant_id = current_user_id
        form.save()

    def get_edit_object(self, request, pk, *args, **kwargs):
        """
        预留钩子：获取当前用户选定的跟进记录
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        return models.ConsultRecord.objects.filter(pk=pk, customer_id=customer_id,
                                                   customer__consultant_id=current_user_id).first()

    def del_object(self, request, pk, *args, **kwargs):
        """
        预留钩子：删除当前用户选定的跟进记录
        :param request:
        :param pk:
        :param args:
        :param kwargs:
        :return:
        """
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']

        record_queryset = models.ConsultRecord.objects.filter(pk=pk, customer_id=customer_id,
                                                              customer__consultant_id=current_user_id)

        if not record_queryset.exists():
            return HttpResponse('要删除的记录不存在，请重新选择！')
        record_queryset.delete()
