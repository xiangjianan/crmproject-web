from django import forms
from django.urls import re_path
from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponse, render, redirect
from django.core.exceptions import ValidationError

from stark.service.stark import StarkHandler, get_choice_text, Option
from stark.forms.base import StarkModelForm, StarkForm
from web import models
from web.utils.md5 import gen_md5

from .base import PermissionHandler


class UserInfoAddModelForm(StarkModelForm):
    """
    ModelForm配置：员工表（添加）
    """
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'password', 'confirm_password', 'nickname', 'gender', 'phone', 'email', 'depart', 'roles']

    def clean_confirm_password(self):
        try:
            password = self.cleaned_data['password']
            confirm_password = self.cleaned_data['confirm_password']
            if password != confirm_password:
                raise ValidationError('密码输入不一致')
        except:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        try:
            password = self.cleaned_data['password']
            self.cleaned_data['password'] = gen_md5(password)
        except:
            raise ValidationError('')
        return self.cleaned_data


class UserInfoChangeModelForm(StarkModelForm):
    """
    ModelForm配置：员工表（编辑）
    """

    class Meta:
        model = models.UserInfo
        fields = ['name', 'nickname', 'gender', 'phone', 'email', 'depart', 'roles']


class ResetPasswordForm(StarkForm):
    """
    Form配置：员工表（重置密码）
    """
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        try:
            password = self.cleaned_data['password']
            confirm_password = self.cleaned_data['confirm_password']
            if password != confirm_password:
                raise ValidationError('密码输入不一致')
        except:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        try:
            password = self.cleaned_data['password']
            self.cleaned_data['password'] = gen_md5(password)
        except:
            raise ValidationError('')
        return self.cleaned_data


#class UserInfoHandler(StarkHandler):
class UserInfoHandler(PermissionHandler, StarkHandler):
    """
    stark配置：员工表（用户表）
    """

    def get_model_form_class(self, is_add, request, pk, *args, **kwargs):
        """
        获取自定义ModelForm
        :param is_add:
        :param request:
        :param pk:
        :return:
        """
        if is_add:
            return UserInfoAddModelForm
        return UserInfoChangeModelForm

    def display_reset_pwd(self, obj=None, is_header=None, *args, **kwargs):
        """
        自定义的重置密码显示列
        :param obj: 要重置密码的记录对象
        :param is_header: 是否是表头
        :return:
        """
        if is_header:
            return '密码'
        reset_url = self.reverse_commons_url(self.get_url_name('reset_pwd'), pk=obj.pk)
        return mark_safe("<a href='%s'>重置</a>" % reset_url)

    # 页面显示列：复选框｜姓名｜员工昵称｜性别｜手机号｜邮箱｜部门｜重置密码｜默认编辑删除操作
    list_display = [
        StarkHandler.display_checkbox,
        'name', 'nickname',
        get_choice_text('性别', 'gender'),
        'phone', 'email', 'depart',
        display_reset_pwd,
    ]

    # 允许的条件搜索范围：昵称｜姓名｜邮箱｜手机
    search_list = ['nickname__contains', 'name__contains', 'email__contains', 'phone__contains']

    # 允许的组合搜索条件：性别｜部门
    search_group = [
        Option('gender', ),
        Option('depart', is_multi=True, db_condition={'id__gt': 0})
    ]

    # 允许的批量操作：删除
    action_list = [StarkHandler.action_multi_delete, ]

    def reset_password(self, request, pk):
        """
        视图函数：重置密码
        :param request:
        :param pk:
        :return:
        """
        userinfo_object = models.UserInfo.objects.filter(id=pk).first()
        if not userinfo_object:
            return HttpResponse('用户不存在，无法进行密码重置！')

        if request.method == 'GET':
            form = ResetPasswordForm()
            return render(request, 'stark/edit.html', {'form': form})

        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            userinfo_object.password = form.cleaned_data['password']
            userinfo_object.save()
            return redirect(self.memory_reverse())
        return render(request, 'stark/edit.html', {'form': form})

    def extra_urls(self):
        """
        预留钩子：新增URL
        :return:
        """
        patterns = [
            re_path(r'^reset/password/(?P<pk>\d+)/$', self.wrapper(self.reset_password),
                    name=self.get_url_name('reset_pwd')),
        ]
        return patterns
