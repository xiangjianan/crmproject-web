from django.shortcuts import render, redirect

from rbac.service.init_permission import init_permission
from web import models
from web.utils.md5 import gen_md5


def login(request):
    """
    登录
    :param request:
    :return:
    """
    if request.method == 'GET':
        return render(request, 'login-action.html')

    user = request.POST.get('user')
    pwd = request.POST.get('pwd')
    current_user = models.UserInfo.objects.filter(name=user, password=gen_md5(pwd)).first()
    if not current_user:
        return render(request, 'login-action.html', {'msg': '用户名或密码错误'})

    # session初始化：用户信息
    request.session['user_info'] = {'id': current_user.id, 'nickname': current_user.nickname}

    # session初始化：用户权限
    init_permission(current_user, request)

    return redirect('/index/')


def index(request):
    """
    首页
    :param request:
    :return:
    """
    return render(request, 'index.html')


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.delete()
    return redirect('/login/')
