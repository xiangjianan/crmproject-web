from django.urls import re_path
from django.shortcuts import HttpResponse
from django import forms

from stark.service.stark import StarkHandler, get_choice_text
from stark.forms.base import StarkModelForm
from web import models

from .base import PermissionHandler


class PaymentRecordModelForm(StarkModelForm):
    """
    ModelForm配置：缴费申请表（老学员）
    """

    class Meta:
        model = models.PaymentRecord
        fields = ['pay_type', 'paid_fee', 'class_list', 'note']


class StudentPaymentRecordModelForm(StarkModelForm):
    """
    ModelForm配置：缴费申请表（新学员）
    """
    qq = forms.CharField(label='QQ号', max_length=32)
    mobile = forms.CharField(label='手机号', max_length=32)
    emergency_contract = forms.CharField(label='紧急联系人电话', max_length=32)

    class Meta:
        model = models.PaymentRecord
        fields = ['pay_type', 'paid_fee', 'class_list', 'qq', 'mobile', 'emergency_contract', 'note']


class PaymentRecordHandler(PermissionHandler, StarkHandler):
    """
    stark配置：缴费申请表
    """

    def get_model_form_class(self, is_add, request, pk, *args, **kwargs):
        """
        获取自定义ModelForm：老学员使用PaymentRecordModelForm，新学员使用StudentPaymentRecordModelForm
        :param is_add:
        :param request:
        :param pk:
        :return:
        """
        customer_id = kwargs.get('customer_id')
        student_exists = models.Student.objects.filter(customer_id=customer_id).exists()
        if student_exists:
            return PaymentRecordModelForm
        return StudentPaymentRecordModelForm

    # 页面显示列：缴费类型｜金额｜申请班级｜课程顾问｜状态
    list_display = [
        get_choice_text('缴费类型', 'pay_type'),
        'paid_fee', 'class_list', 'consultant',
        get_choice_text('状态', 'confirm_status')
    ]

    def get_list_display(self, request, *args, **kwargs):
        """
        钩子方法：取消默认的编辑删除列
        :return:
        """
        value = []
        if self.list_display:
            value.extend(self.list_display)
        return value

    def get_urls(self):
        """
        预留钩子：重写URL
        :return:
        """
        patterns = [
            re_path(r'^list/(?P<customer_id>\d+)/$', self.wrapper(self.list_view), name=self.get_list_url_name),
            re_path(r'^add/(?P<customer_id>\d+)/$', self.wrapper(self.add_view), name=self.get_add_url_name),
        ]
        patterns.extend(self.extra_urls())
        return patterns

    def get_queryset(self, request, *args, **kwargs):
        """
        预留钩子：获取当前用户指定私有客户的缴费申请
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        return self.model_class.objects.filter(customer_id=customer_id, customer__consultant_id=current_user_id)

    def save(self, request, form, is_update, *args, **kwargs):
        """
        钩子方法：保存前增加业务处理
        :param request:
        :param form:
        :param is_update:
        :return:
        """
        customer_id = kwargs.get('customer_id')
        current_user_id = request.session['user_info']['id']
        # 判断学员是否是当前课程顾问的私有客户
        object_exists = models.Customer.objects.filter(id=customer_id, consultant_id=current_user_id).exists()
        if not object_exists:
            return HttpResponse('非法操作')

        form.instance.customer_id = customer_id
        form.instance.consultant_id = current_user_id

        # 创建缴费记录信息
        form.save()

        # 创建学员信息
        class_list = form.cleaned_data['class_list']
        fetch_student_object = models.Student.objects.filter(customer_id=customer_id).first()
        # 新学员
        if not fetch_student_object:
            qq = form.cleaned_data['qq']
            mobile = form.cleaned_data['mobile']
            emergency_contract = form.cleaned_data['emergency_contract']
            student_object = models.Student.objects.create(customer_id=customer_id, qq=qq, mobile=mobile,
                                                           emergency_contract=emergency_contract)
            student_object.class_list.add(class_list.id)
        # 老学员
        else:
            fetch_student_object.class_list.add(class_list.id)
