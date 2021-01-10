"""
admin后台管理功能，由于选择使用stark组件，该功能不是必须，可选择屏蔽
"""
from django.contrib import admin
from rbac import models


# class PermissionAdmin(admin.ModelAdmin):
#     """
#     权限表在admin页面显示自定义的属性
#     """
#     list_display = ['title', 'url', ]
#
#
# admin.site.register(models.Permission, PermissionAdmin)
# admin.site.register(models.UserInfo)
# admin.site.register(models.Role)
# admin.site.register(models.Menu)
