from django.shortcuts import redirect
from django.utils.safestring import mark_safe
from django.urls import reverse

from stark.service.stark import StarkHandler, get_m2m_text, get_choice_text
from stark.forms.base import StarkModelForm
from web import models

from .base import PermissionHandler


class PrivateCustomerModelForm(StarkModelForm):
    """
    ModelForm配置：客户表（私有）
    """

    class Meta:
        model = models.Customer
        exclude = ['consultant', ]


class PrivateCustomerHandler(PermissionHandler, StarkHandler):
    """
    stark配置：客户表（私有）
    """
    # 获取自定义ModelForm
    model_form_class = PrivateCustomerModelForm

    def display_record(self, obj=None, is_header=None, *args, **kwargs):
        """
        自定义跟进记录显示列
        :param obj: 选择的客户对象
        :param is_header:
        :return:
        """
        if is_header:
            return '跟进记录'
        record_url = reverse('stark:web_consultrecord_list', kwargs={'customer_id': obj.pk})
        return mark_safe('<a href="%s">管理</a>' % record_url)

    def display_pay_record(self, obj=None, is_header=None, *args, **kwargs):
        """
        自定义缴费显示列
        :param obj:
        :param is_header:
        :param args:
        :param kwargs:
        :return:
        """
        if is_header:
            return '缴费'
        record_url = reverse('stark:web_paymentrecord_list', kwargs={'customer_id': obj.pk})
        return mark_safe('<a href="%s">管理</a>' % record_url)

    # 页面显示列：复选框｜姓名｜联系方式｜咨询课程｜状态｜跟进记录｜缴费
    list_display = [
        StarkHandler.display_checkbox,
        'name', 'qq',
        get_m2m_text('咨询课程', 'course'),
        get_choice_text('状态', 'status'),
        display_record,
        display_pay_record,
    ]

    def get_queryset(self, request, *args, **kwargs):
        """
        预留钩子：获取当前用户的私有客户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        current_user_id = request.session['user_info']['id']
        return self.model_class.objects.filter(consultant_id=current_user_id)

    def save(self, request, form, is_update, *args, **kwargs):
        """
        钩子方法：保存前设置默认课程顾问为当前登录用户
        :param request:
        :param form:
        :param is_update:
        :param args:
        :param kwargs:
        :return:
        """
        if not is_update:
            current_user_id = request.session['user_info']['id']
            form.instance.consultant_id = current_user_id
        form.save()

    def action_multi_remove(self, request, *args, **kwargs):
        """
        批量操作：私户到公户
        :return:
        """
        current_user_id = request.session['user_info']['id']
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list, consultant_id=current_user_id).update(consultant=None)
        return redirect(self.memory_reverse(*args, **kwargs))

    action_multi_remove.text = "移除到公户"

    # 批量操作：删除｜私户到公户
    action_list = [StarkHandler.action_multi_delete, action_multi_remove]
