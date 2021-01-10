from django.urls import re_path
from django.shortcuts import redirect

from stark.service.stark import StarkHandler, get_choice_text, get_datetime_text
from .base import PermissionHandler


class CheckPaymentRecordHandler(PermissionHandler, StarkHandler):
    """
    stark配置：缴费申请表（签审）
    """
    # 页面展示列：复选框｜客户｜缴费类型｜金额｜申请班级｜申请日期｜状态｜课程顾问
    list_display = [
        StarkHandler.display_checkbox,
        'customer',
        get_choice_text('缴费类型', 'pay_type'),
        'paid_fee', 'class_list',
        get_datetime_text('申请日期', 'apply_date'),
        get_choice_text('申请状态', 'confirm_status'),
        'consultant'
    ]

    def get_list_display(self, request, *args, **kwargs):
        """
        预留钩子：仅显示list_display列表
        :return:
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
        return value

    # 排序配置：id降序｜审批状态
    order_list = ['-id', 'confirm_status']

    # 添加按钮配置：取消
    has_add_btn = False

    def get_urls(self):
        """
        预留钩子：重写URL（审批单不允许增删改）
        :return:
        """
        patterns = [
            re_path(r'^list/$', self.wrapper(self.list_view), name=self.get_list_url_name),
        ]

        patterns.extend(self.extra_urls())
        return patterns

    def action_multi_confirm(self, request, *args, **kwargs):
        """
        批量操作：签审
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pk_list = request.POST.getlist('pk')

        for pk in pk_list:
            # 待签审的缴费记录
            payment_object = self.model_class.objects.filter(id=pk, confirm_status=1).first()
            if not payment_object:
                continue

            # 签审状态->已签审
            payment_object.confirm_status = 2
            payment_object.save()

            # 客户状态->已报名
            payment_object.customer.status = 1
            payment_object.customer.save()

            # 学生状态->在读
            payment_object.customer.student.student_status = 2
            payment_object.customer.student.save()

        return redirect(self.memory_reverse())

    action_multi_confirm.text = '批量签审'

    def action_multi_cancel(self, request, *args, **kwargs):
        """
        批量操作：驳回
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list, confirm_status=1).update(confirm_status=3)

        return redirect(self.memory_reverse())

    action_multi_cancel.text = '批量驳回'

    # 允许的批量操作：签审｜驳回
    action_list = [action_multi_confirm, action_multi_cancel]
