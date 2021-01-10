from django.urls import re_path

from rbac.views import menu
from rbac.views import role
from rbac.views import user

app_name = '[rbac]'

urlpatterns = [
    # 角色：增删改查
    re_path(r'^role/list/$', role.role_list, name='role_list'),
    re_path(r'^role/add/$', role.role_add, name='role_add'),
    re_path(r'^role/edit/(?P<pk>\d+)/$', role.role_edit, name='role_edit'),
    re_path(r'^role/del/(?P<pk>\d+)/$', role.role_del, name='role_del'),

    # 用户：增删改查，推荐使用业务中的用户表（已继承rbac用户表）
    # re_path(r'^user/list/$', user.user_list, name='user_list'),
    # re_path(r'^user/add/$', user.user_add, name='user_add'),
    # re_path(r'^user/edit/(?P<pk>\d+)/$', user.user_edit, name='user_edit'),
    # re_path(r'^user/del/(?P<pk>\d+)/$', user.user_del, name='user_del'),
    # re_path(r'^user/reset/password/(?P<pk>\d+)/$', user.user_reset_pwd, name='user_reset_pwd'),

    # 菜单（一级菜单）：增删改查
    re_path(r'^menu/list/$', menu.menu_list, name='menu_list'),
    re_path(r'^menu/add/$', menu.menu_add, name='menu_add'),
    re_path(r'^menu/edit/(?P<pk>\d+)/$', menu.menu_edit, name='menu_edit'),
    re_path(r'^menu/del/(?P<pk>\d+)/$', menu.menu_del, name='menu_del'),

    # 可做菜单的权限（二级菜单）：增删改
    re_path(r'^second/menu/add/(?P<menu_id>\d+)/$', menu.second_menu_add, name='second_menu_add'),
    re_path(r'^second/menu/edit/(?P<pk>\d+)/$', menu.second_menu_edit, name='second_menu_edit'),
    re_path(r'^second/menu/del/(?P<pk>\d+)/$', menu.second_menu_del, name='second_menu_del'),

    # 不可做菜单的权限（三级菜单）：增删改
    re_path(r'^permission/add/(?P<second_menu_id>\d+)/$', menu.permission_add, name='permission_add'),
    re_path(r'^permission/edit/(?P<pk>\d+)/$', menu.permission_edit, name='permission_edit'),
    re_path(r'^permission/del/(?P<pk>\d+)/$', menu.permission_del, name='permission_del'),

    # 批量操作权限：增删改查
    re_path(r'^multi/permissions/$', menu.multi_permissions, name='multi_permissions'),
    re_path(r'^multi/permissions/del/(?P<pk>\d+)/$', menu.multi_permissions_del, name='multi_permissions_del'),

    # 为用户分配角色和权限
    re_path(r'^distribute/permissions/$', menu.distribute_permissions, name='distribute_permissions'),
]
