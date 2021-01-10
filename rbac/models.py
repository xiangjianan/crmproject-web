from django.db import models


class Menu(models.Model):
    """
    菜单表
    菜单名｜菜单图标
    """
    title = models.CharField(verbose_name='菜单', max_length=32)
    icon = models.CharField(verbose_name='图标', max_length=32)

    def __str__(self):
        return self.title


class Permission(models.Model):
    """
    权限表
    权限名称｜权限url｜可被Django反向解析成URL的唯一字符串｜外键关联的菜单id（一级菜单）｜自关联的父级权限id（二级菜单）
    """
    title = models.CharField(verbose_name="权限名称", max_length=32)
    url = models.CharField(verbose_name="含正则的url", max_length=128)
    name = models.CharField(verbose_name='代码', max_length=64, null=True, blank=True, unique=True)
    menu = models.ForeignKey(verbose_name='所属菜单', to='Menu', null=True, blank=True, on_delete=models.CASCADE,
                             help_text='null表示非菜单')
    pid = models.ForeignKey(verbose_name='默认选中权限', to='Permission', related_name='ps', null=True, blank=True,
                            help_text="对于无法作为菜单的URL，可以为其选择一个可以作为菜单的父权限，那么访问URL时，则默认选中此父权限",
                            limit_choices_to={'menu__isnull': False}, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Role(models.Model):
    """
    角色表
    角色名称｜该角色拥有的所有权限
    """
    title = models.CharField(verbose_name='角色名称', max_length=32)
    permissions = models.ManyToManyField(verbose_name='拥有的所有权限', to='Permission', blank=True)

    def __str__(self):
        return self.title


class UserInfo(models.Model):
    """
    用户表
    用户名｜密码｜邮箱｜该用户拥有的所有角色
    """
    name = models.CharField(verbose_name='姓名', max_length=32)
    password = models.CharField(verbose_name='密码', max_length=64)
    email = models.EmailField(verbose_name='邮箱', max_length=32, null=True, blank=True)
    roles = models.ManyToManyField(verbose_name='拥有的所有角色', to=Role, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        """
        设置此类为可被其他Model类继承
        """
        abstract = True
