from django import forms
from django.utils.safestring import mark_safe
from rbac import models
from rbac.forms.base import BootStrapModelForm

ICON_LIST = [
    ['fa-check-square', '<i aria-hidden="true" class="fa fa-check-square"></i>'],
    ['fa-th-large', '<i aria-hidden="true" class="fa fa-th-large"></i>'],
    ['fa-th-list', '<i aria-hidden="true" class="fa fa-th-list"></i>'],
    ['fa-th', '<i aria-hidden="true" class="fa fa-th"></i>'],
    ['fa-save', '<i aria-hidden="true" class="fa fa-save"></i>'],
    ['fa-list-ul', '<i aria-hidden="true" class="fa fa-list-ul"></i>'],
    ['fa-list', '<i aria-hidden="true" class="fa fa-list"></i>'],
    ['fa-minus-square', '<i aria-hidden="true" class="fa fa-minus-square"></i>'],
    ['fa-rocket', '<i aria-hidden="true" class="fa fa-rocket"></i>'],
    ['fa-universal-access', '<i aria-hidden="true" class="fa fa-universal-access"></i>'],
    ['fa-university', '<i aria-hidden="true" class="fa fa-university"></i>'],
    ['fa-user', '<i aria-hidden="true" class="fa fa-user"></i>'],
    ['fa-user-o', '<i aria-hidden="true" class="fa fa-user-o"></i>'],
    ['fa-user-circle-o', '<i aria-hidden="true" class="fa fa-user-circle-o"></i>'],
    ['fa-user-plus', '<i aria-hidden="true" class="fa fa-user-plus"></i>'],
    ['fa-tasks', '<i aria-hidden="true" class="fa fa-tasks"></i>'],
    ['fa-address-card', '<i aria-hidden="true" class="fa fa-address-card"></i>'],
    ['fa-address-card-o', '<i aria-hidden="true" class="fa fa-address-card-o"></i>'],
    ['fa-address-book', '<i aria-hidden="true" class="fa fa-address-book"></i>'],
    ['fa-address-book-o', '<i aria-hidden="true" class="fa fa-address-book-o"></i>'],
    ['fa-handshake-o', '<i aria-hidden="true" class="fa fa-handshake-o"></i>'],
    ['fa-heart', '<i aria-hidden="true" class="fa fa-heart"></i>'],
    ['fa-fa-bar-chart', '<i aria-hidden="true" class="fa fa-bar-chart"></i>'],
    ['fa-briefcase', '<i aria-hidden="true" class="fa fa-briefcase"></i>'],
    ['fa-history', '<i aria-hidden="true" class="fa fa-history"></i>'],
    ['fa-home', '<i aria-hidden="true" class="fa fa-home"></i>'],
    ['fa-hotel', '<i aria-hidden="true" class="fa fa-hotel"></i>'],
    ['fa-hourglass', '<i aria-hidden="true" class="fa fa-hourglass"></i>'],
    ['fa-hourglass-1', '<i aria-hidden="true" class="fa fa-hourglass-1"></i>'],
    ['fa-hourglass-2', '<i aria-hidden="true" class="fa fa-hourglass-2"></i>'],
    ['fa-hourglass-end', '<i aria-hidden="true" class="fa fa-hourglass-end"></i>'],
    ['fa-hourglass-half', '<i aria-hidden="true" class="fa fa-hourglass-half"></i>'],
    ['fa-id-badge', '<i aria-hidden="true" class="fa fa-id-badge"></i>'],
    ['fa-id-card', '<i aria-hidden="true" class="fa fa-id-card"></i>'],
    ['fa-id-card-o', '<i aria-hidden="true" class="fa fa-id-card-o"></i>'],
    ['fa-image', '<i aria-hidden="true" class="fa fa-image"></i>'],
    ['fa-users', '<i aria-hidden="true" class="fa fa-users"></i>'],
    ['fa-check-circle', '<i aria-hidden="true" class="fa fa-check-circle"></i>'],
    ['fa-retweet', '<i aria-hidden="true" class="fa fa-retweet"></i>'],
    ['fa-wrench', '<i aria-hidden="true" class="fa fa-wrench"></i>']]
# font-awesome图标
for item in ICON_LIST:
    item[1] = mark_safe(item[1])


class MenuModelForm(forms.ModelForm):
    """
    ModelForm配置：一级菜单
    """

    class Meta:
        model = models.Menu
        fields = ['title', 'icon']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'icon': forms.RadioSelect(
                choices=ICON_LIST,
                attrs={'class': 'clearfix'}
            )
        }


class SecondMenuModelForm(BootStrapModelForm):
    """
    ModelForm配置：二级菜单
    """

    class Meta:
        model = models.Permission
        exclude = ['pid']


class PermissionModelForm(BootStrapModelForm):
    """
    ModelForm配置：不能做菜单的权限（三级菜单）
    """

    class Meta:
        model = models.Permission
        # 三级菜单的pid默认设置为用户当前选中的二级菜单id
        fields = ['title', 'name', 'url']


class MultiAddPermissionForm(forms.Form):
    """
    Form配置：批量添加权限
    """
    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': "form-control"}),
        required=False,

    )

    pid_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': "form-control"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')


class MultiEditPermissionForm(forms.Form):
    """
    Form配置：批量修改权限
    """
    id = forms.IntegerField(
        widget=forms.HiddenInput()
    )

    title = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    url = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    name = forms.CharField(
        widget=forms.TextInput(attrs={'class': "form-control"})
    )
    menu_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': "form-control"}),
        required=False,

    )

    pid_id = forms.ChoiceField(
        choices=[(None, '-----')],
        widget=forms.Select(attrs={'class': "form-control"}),
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['menu_id'].choices += models.Menu.objects.values_list('id', 'title')
        self.fields['pid_id'].choices += models.Permission.objects.filter(pid__isnull=True).exclude(
            menu__isnull=True).values_list('id', 'title')
