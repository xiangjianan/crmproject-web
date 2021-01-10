from rbac import models
from rbac.forms.base import BootStrapModelForm


class RoleModelForm(BootStrapModelForm):
    """
    ModelForm配置：角色表
    """
    class Meta:
        model = models.Role
        fields = ['title', ]
