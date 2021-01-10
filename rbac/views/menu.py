"""
菜单增删改查及权限分配相关的视图函数
"""
from collections import OrderedDict

from django.shortcuts import render, redirect, HttpResponse
from django.forms import formset_factory
from django.utils.module_loading import import_string

from crmProject import settings

from rbac.forms.menu import *
from rbac.service.urls import memory_reverse
from rbac.service.routes import get_all_url_dict
from rbac.service.init_permission import init_permission

from web.models import UserInfo


def reload_session(request):
    """
    修改菜单数据成功后，重新加载用户权限到session，以重新渲染菜单
    :param request:
    :return:
    """
    user_id = request.session['user_info']['id']
    current_user = UserInfo.objects.filter(pk=user_id).first()
    # session初始化：用户信息
    request.session['user_info'] = {'id': current_user.id, 'nickname': current_user.nickname}
    # session初始化：用户权限
    init_permission(current_user, request)


def menu_list(request):
    """
    初始化菜单（一级、二级）和权限列表
    :param request:
    :return:
    """
    menus = models.Menu.objects.all()

    # 用户选择的菜单
    menu_id = request.GET.get('mid')
    second_menu_id = request.GET.get('sid')

    # 防止用户手动输入错误的mid
    menu_exists = models.Menu.objects.filter(id=menu_id).exists()
    if not menu_exists:
        menu_id = None
    if menu_id:
        second_menus = models.Permission.objects.filter(menu_id=menu_id)
    else:
        second_menus = []

    # 防止用户手动输入错误的sid
    second_menu_exists = models.Permission.objects.filter(id=second_menu_id).exists()
    if not second_menu_exists:
        second_menu_id = None
    if second_menu_id:
        permissions = models.Permission.objects.filter(pid_id=second_menu_id)
    else:
        permissions = []

    return render(
        request,
        'rbac/menu_list.html',
        {
            'menus': menus,
            'menu_id': menu_id,
            'second_menus': second_menus,
            'second_menu_id': second_menu_id,
            'permissions': permissions,
        }
    )


def menu_add(request):
    """
    添加菜单（一级）
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = MenuModelForm()
        return render(request, 'rbac/edit.html', {'form': form})

    form = MenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/edit.html', {'form': form})


def menu_edit(request, pk):
    """
    编辑菜单（一级）
    :param request:
    :param pk: 要编辑的一级菜单ID
    :return:
    """
    obj = models.Menu.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('菜单不存在')
    if request.method == 'GET':
        form = MenuModelForm(instance=obj)
        return render(request, 'rbac/edit.html', {'form': form})

    form = MenuModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        reload_session(request)
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/edit.html', {'form': form})


def menu_del(request, pk):
    """
    删除菜单（一级）
    :param request:
    :param pk: 要删除的一级菜单ID
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Menu.objects.filter(id=pk).delete()
    return redirect(url)


def second_menu_add(request, menu_id):
    """
    添加菜单（二级）
    :param request:
    :param menu_id: 已选择的一级菜单ID（用于设置默认值）
    :return:
    """

    menu_object = models.Menu.objects.filter(id=menu_id).first()

    if request.method == 'GET':
        # 设置一级菜单默认值
        form = SecondMenuModelForm(initial={'menu': menu_object})
        return render(request, 'rbac/edit.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/edit.html', {'form': form})


def second_menu_edit(request, pk):
    """
    编辑菜单（二级）
    :param request:
    :param pk: 要编辑的二级菜单ID
    :return:
    """

    permission_object = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = SecondMenuModelForm(instance=permission_object)
        return render(request, 'rbac/edit.html', {'form': form})

    form = SecondMenuModelForm(data=request.POST, instance=permission_object)
    if form.is_valid():
        form.save()
        reload_session(request)
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/edit.html', {'form': form})


def second_menu_del(request, pk):
    """
    删除菜单（二级）
    :param request:
    :param pk: 要删除的二级菜单ID
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def permission_add(request, second_menu_id):
    """
    添加权限（三级菜单）
    :param request:
    :param second_menu_id: 已选择的二级菜单ID（做为三级菜单pid的默认值）
    :return:
    """
    if request.method == 'GET':
        form = PermissionModelForm()
        return render(request, 'rbac/edit.html', {'form': form})

    form = PermissionModelForm(data=request.POST)
    if form.is_valid():
        # 防止用户手动输入错误的sid
        second_menu_object = models.Permission.objects.filter(id=second_menu_id).first()
        if not second_menu_object:
            return HttpResponse('二级菜单不存在，请重新选择！')
        form.instance.pid = second_menu_object
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/edit.html', {'form': form})


def permission_edit(request, pk):
    """
    编辑权限（三级菜单）
    :param request:
    :param pk: 当前要编辑的权限ID
    :return:
    """

    permission_object = models.Permission.objects.filter(id=pk).first()

    if request.method == 'GET':
        form = PermissionModelForm(instance=permission_object)
        return render(request, 'rbac/edit.html', {'form': form})

    form = PermissionModelForm(data=request.POST, instance=permission_object)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:menu_list'))

    return render(request, 'rbac/edit.html', {'form': form})


def permission_del(request, pk):
    """
    删除权限（三级菜单）
    :param request:
    :param pk: 当前要删除的权限ID
    :return:
    """
    url = memory_reverse(request, 'rbac:menu_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def multi_permissions(request):
    """
    批量操作权限（添加、修改）
    :param request:
    :return:
    """
    # 获取用户操作的类型（批量添加 or 批量修改）
    post_type = request.GET.get('type')
    generate_formset_class = formset_factory(MultiAddPermissionForm, extra=0)
    update_formset_class = formset_factory(MultiEditPermissionForm, extra=0)

    # 错误信息标志位
    has_generate_error = False
    has_update_error = False

    # 增：批量添加权限
    if request.method == 'POST' and post_type == 'generate':
        formset = generate_formset_class(data=request.POST)
        if formset.is_valid():
            object_list = []
            # formset中没有错误信息，则将用户提交的数据获取到
            post_row_list = formset.cleaned_data
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                try:
                    new_object = models.Permission(**row_dict)
                    # 唯一校验：检查当前对象在数据库是否存在
                    new_object.validate_unique()
                    object_list.append(new_object)
                except Exception as e:
                    formset.errors[i].update(e)
                    generate_formset_error = formset
                    has_generate_error = True
            if not has_generate_error:
                # 获取所有数据后，再统一添加到数据库
                models.Permission.objects.bulk_create(object_list, batch_size=100)
        else:
            generate_formset_error = formset
            has_generate_error = True

    # 改：批量修改权限
    if request.method == 'POST' and post_type == 'update':
        formset = update_formset_class(data=request.POST)
        if formset.is_valid():
            post_row_list = formset.cleaned_data
            for i in range(0, formset.total_form_count()):
                row_dict = post_row_list[i]
                # 指定当前修改的权限id
                permission_id = row_dict.pop('id')
                try:
                    row_object = models.Permission.objects.filter(id=permission_id).first()
                    # 通过反射批量更新row_object对象的属性值
                    for k, v in row_dict.items():
                        setattr(row_object, k, v)
                    # 唯一校验通过，直接保存到数据库
                    row_object.validate_unique()
                    row_object.save()
                except Exception as e:
                    formset.errors[i].update(e)
                    update_formset_error = formset
                    has_update_error = True
        else:
            update_formset_error = formset
            has_update_error = True

        reload_session(request)

    # 查：
    # 1. 获取项目中所有的URL
    all_url_dict = get_all_url_dict()
    router_name_set = set(all_url_dict.keys())

    # 2 获取数据库中所有的URL
    permissions = models.Permission.objects.all().values('id', 'title', 'name', 'url', 'menu_id', 'pid_id')
    permission_dict = OrderedDict()
    permission_name_set = set()
    for row in permissions:
        permission_dict[row['name']] = row
        permission_name_set.add(row['name'])

    # 3 项目url和数据库url比较
    for name, value in permission_dict.items():
        router_row_dict = all_url_dict.get(name)
        if not router_row_dict:
            continue
        if value['url'] != router_row_dict['url']:
            value['url'] = '路由和数据库中不一致'

    # 3.1 计算出应该增加的name
    generate_name_list = router_name_set - permission_name_set
    generate_formset = generate_formset_class(
        initial=[row_dict for name, row_dict in all_url_dict.items() if name in generate_name_list])

    # 3.2 计算出应该删除的name
    delete_name_list = permission_name_set - router_name_set
    delete_row_list = [row_dict for name, row_dict in permission_dict.items() if name in delete_name_list]

    # 3.3 计算出应该更新的name
    update_name_list = permission_name_set & router_name_set
    update_formset = update_formset_class(
        initial=[row_dict for name, row_dict in permission_dict.items() if name in update_name_list])

    # 判断是否有错误信息
    generate_formset = generate_formset_error if has_generate_error else generate_formset
    update_formset = update_formset_error if has_update_error else update_formset

    return render(
        request,
        'rbac/multi_permissions.html',
        {
            'generate_formset': generate_formset,
            'delete_row_list': delete_row_list,
            'update_formset': update_formset,
        }
    )


def multi_permissions_del(request, pk):
    """
    批量删除权限
    :param request:
    :param pk: 要删除的权限ID
    :return:
    """
    url = memory_reverse(request, 'rbac:multi_permissions')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel': url})

    models.Permission.objects.filter(id=pk).delete()
    return redirect(url)


def distribute_permissions(request):
    """
    权限分配
    :param request:
    :return:
    """
    # 获取用户操作的类型（更新角色 or 更新权限）
    post_type = request.POST.get('type')

    # 获取uid，并防止用户手动输入错误uid
    user_id = request.GET.get('uid')
    # 业务中的用户表 ，"web.models.UserInfo""
    user_model_class = import_string(settings.RBAC_USER_MODEL_CLASS)
    user_object = user_model_class.objects.filter(id=user_id).first()
    # user_object = models.UserInfo.objects.filter(id=user_id).first()
    if not user_object:
        user_id = None

    # 获取rid，防止用户手动输入错误rid
    role_id = request.GET.get('rid')
    role_object = models.Role.objects.filter(id=role_id).first()
    if not role_object:
        role_id = None

    # 更新角色
    if request.method == 'POST' and post_type == 'role':
        role_id_list = request.POST.getlist('roles')
        if not user_object:
            return HttpResponse('请选择用户，然后再分配角色！')
        # 用户和角色关系添加到第三张表（关系表）
        user_object.roles.set(role_id_list)

    # 更新权限
    if request.method == 'POST' and post_type == 'permission':
        permission_id_list = request.POST.getlist('permissions')
        if not role_object:
            return HttpResponse('请选择角色，然后再分配权限！')
        # 角色和权限关系添加到第三张表（关系表）
        role_object.permissions.set(permission_id_list)

    # 获取当前用户拥有的所有角色
    if user_id:
        user_has_roles = user_object.roles.all()
    else:
        user_has_roles = []
    # 设置成字典类型，提高查询效率
    user_has_roles_dict = {row.id: None for row in user_has_roles}

    # 如果选中角色，优先显示选中角色拥有的所有权限
    if role_object:
        user_has_permissions = role_object.permissions.all()
        user_has_permissions_dict = {row.id: None for row in user_has_permissions}
    # 未选中角色，但选择了用户，优先显示用户拥有的所有权限
    elif user_object:
        user_has_permissions = user_object.roles.filter(permissions__id__isnull=False).values('id',
                                                                                              'permissions').distinct()
        user_has_permissions_dict = {row['permissions']: None for row in user_has_permissions}
    # 都为未选择，设置为空
    else:
        user_has_permissions_dict = {}

    all_user_list = user_model_class.objects.all()
    all_role_list = models.Role.objects.all()

    # 所有一级菜单，QuerySet类型
    all_menu_list = models.Menu.objects.values('id', 'title')
    # 设置成字典类型，提高查询效率，并利用浅拷贝原理间接更新all_menu_list
    all_menu_dict = {}
    for row in all_menu_list:
        # 初始化一级菜单的字典类型数据结构
        row['children'] = []
        all_menu_dict[row['id']] = row

    # 所有二级菜单（能做菜单的权限）
    all_second_menu_list = models.Permission.objects.filter(menu__isnull=False).values('id', 'title', 'menu_id')
    all_second_menu_dict = {}
    for row in all_second_menu_list:
        # 初始化二级菜单的字典类型数据结构
        row['children'] = []
        all_second_menu_dict[row['id']] = row
        # 将二级菜单添加到一级菜单
        menu_id = row['menu_id']
        all_menu_dict[menu_id]['children'].append(row)

    # 所有三级菜单（不能做菜单的权限）
    all_permission_list = models.Permission.objects.filter(menu__isnull=True).values('id', 'title', 'pid_id')
    for row in all_permission_list:
        # 将三级菜单添加到二级菜单
        pid = row['pid_id']
        if not pid:
            continue
        all_second_menu_dict[pid]['children'].append(row)

    return render(
        request,
        'rbac/distribute_permissions.html',
        {
            'user_list': all_user_list,
            'role_list': all_role_list,
            'all_menu_list': all_menu_list,
            'user_id': user_id,
            'role_id': role_id,
            'user_has_roles_dict': user_has_roles_dict,
            'user_has_permissions_dict': user_has_permissions_dict,
        }
    )
