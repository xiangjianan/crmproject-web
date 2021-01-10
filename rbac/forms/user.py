from django import forms
from django.core.exceptions import ValidationError

from rbac import models
from rbac.forms.base import BootStrapModelForm


class UserModelForm(BootStrapModelForm):
    """
    ModelForm配置：用户表
    """
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['name', 'email', 'password', 'confirm_password']

    def clean_confirm_password(self):
        """
        检测密码是否一致
        :return:
        """
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('两次密码输入不一致')
        return confirm_password


class UpdateUserModelForm(BootStrapModelForm):
    """
    ModelForm配置：用户表（更新）
    """
    class Meta:
        model = models.UserInfo
        fields = ['name', 'email', ]


class ResetPasswordUserModelForm(BootStrapModelForm):
    """
    ModelForm：用户表（重置密码）
    """
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfo
        fields = ['password', 'confirm_password']

    def clean_confirm_password(self):
        """
        检测密码是否一致
        :return:
        """
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('两次密码输入不一致')
        return confirm_password
