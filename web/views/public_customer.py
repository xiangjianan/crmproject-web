from django.urls import re_path
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render, redirect
from django.db import transaction

from stark.service.stark import StarkHandler, get_choice_text, get_m2m_text
from stark.forms.base import StarkModelForm
from web import models

from .base import PermissionHandler


class PublicCustomerModelForm(StarkModelForm):
    """
    ModelForm配置：客户表（公有）
    """

    class Meta:
        model = models.Customer
        exclude = ['consultant', ]


class PublicCustomerHandler(PermissionHandler, StarkHandler):
    """
    stark配置：客户表（公有）
    """
    # 获取自定义ModelForm
    model_form_class = PublicCustomerModelForm

    def display_record(self, obj=None, is_header=None, *args, **kwargs):
        """
        自定义跟进记录显示列
        :param obj: 选则的客户对象
        :param is_header:
        :return:
        """
        if is_header:
            return '跟进记录'
        record_url = self.reverse_commons_url(self.get_url_name('record_view'), pk=obj.pk)
        return mark_safe('<a class="text-info" href="%s">查看</a>' % record_url)

    # 页面显示列：复选框｜姓名｜联系方式｜咨询课程｜状态｜跟进记录
    list_display = [
        StarkHandler.display_checkbox,
        'name', 'qq',
        get_m2m_text('咨询课程', 'course'),
        get_choice_text('状态', 'status'),
        display_record,
    ]

    def extra_urls(self):
        """
        预留钩子：新增URL
        :return:
        """
        patterns = [
            re_path(r'^record/(?P<pk>\d+)/$', self.wrapper(self.record_view),
                    name=self.get_url_name('record_view')),
        ]
        return patterns

    def get_queryset(self, request, *args, **kwargs):
        """
        预留钩子：获取没有课程顾问的客户（公有客户）
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        return self.model_class.objects.filter(consultant__isnull=True)

    def record_view(self, request, pk):
        """
        视图函数：查看跟进记录
        :param request:
        :param pk: 要查看的客户的id
        :return:
        """
        record_list = models.ConsultRecord.objects.filter(customer_id=pk)
        return render(request, 'record_view.html', {'record_list': record_list})

    def action_multi_apply(self, request, *args, **kwargs):
        """
        批量操作：公户到私户
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        current_user_id = request.session['user_info']['id']
        pk_list = request.POST.getlist('pk')

        # 私户个数限制
        private_customer_count = models.Customer.objects.filter(consultant_id=current_user_id, status=2).count()
        if (private_customer_count + len(pk_list)) > models.Customer.MAX_PRIVATE_CUSTOMER_COUNT:
            return HttpResponse('做人不要太贪心，私户中已有%s个客户，最多还能申请%s' % (
                private_customer_count, models.Customer.MAX_PRIVATE_CUSTOMER_COUNT - private_customer_count))

        # 数据库中加锁
        flag = False
        with transaction.atomic():  # 事务
            # 在数据库中加锁，销售选定的客户中有已报名的、或被其他销售抢先的，则不允许添加
            origin_queryset = models.Customer.objects.filter(id__in=pk_list, status=2,
                                                             consultant__isnull=True).select_for_update()
            if len(origin_queryset) == len(pk_list):
                models.Customer.objects.filter(id__in=pk_list, status=2,
                                               consultant__isnull=True).update(consultant_id=current_user_id)
                flag = True

        if flag:
            # 添加成功刷新页面
            return redirect(self.memory_reverse())
        else:
            return HttpResponse('手速太慢了，选中的客户已被其他人申请，请重新选择')

    action_multi_apply.text = "添加到私户"

    # 批量操作：删除｜公户到私户
    action_list = [StarkHandler.action_multi_delete, action_multi_apply, ]
