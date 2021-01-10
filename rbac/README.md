## rbac组件使用文档

### 1.[起始]
1. 将rbac组件拷贝至项目
2. 全局`urls.py`
    ```python
    from django.urls import path, include
    
    urlpatterns = [
        ...
        path('rbac/', include('rbac.urls', namespace='rbac')),
    ]
    ```

### 2.[用户表结构]
1. 业务系统中的用户表，需要和rbac中的用户表有继承关系
2. `业务app/models.py`
    ```python
    from django.db import models
    from rbac.models import UserInfo as RbacUserInfo
    
    class UserInfo(RbacUserInfo):
        """
        业务系统用户表，继承rbac用户表
        """
        pass
    ```
3. 将业务系统用户表写入`settings.py`配置文件
    ```python   
    # rbac分配权限时，读取业务表中的用户信息
    RBAC_USER_MODLE_CLASS = "app01.models.UserInfo"
    ```     

### 3.[路由分发]
1. 业务系统路由分发
    * 将业务中所有的路由都设置一个name，用于反向生成URL以及粒度控制到按钮级别的权限控制

### 4.[权限信息录入]
1. `settings.py`配置
    ```python
    # 项目URL获取黑名单：自动获取项目中所有URL时，排除以下URL
    AUTO_DISCOVER_EXCLUDE = [
        '/admin/.*',
        '/login/',
        '/logout/',
        '/index/',
    ]
    ```
2. 权限录入
    * 在rbac提供的地址进行操作
        > 菜单管理：http://127.0.0.1:8000/rbac/menu/list/
        > 角色管理：http://127.0.0.1:8000/rbac/role/list/
        > 批量检测URL：http://127.0.0.1:8000/rbac/multi/permissions/
        > 权限分配：http://127.0.0.1:8000/rbac/distribute/permissions/

### 5.[权限初始化]
1. 在业务app中编写一个用户登录逻辑，进行权限初始化，编写一个首页逻辑
    ```python
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
            return render(request, 'login.html')
    
        user = request.POST.get('user')
        pwd = request.POST.get('pwd')
        current_user = models.UserInfo.objects.filter(name=user, password=gen_md5(pwd)).first()
        if not current_user:
            return render(request, 'login.html', {'msg': '用户名或密码错误'})
    
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
    ``` 

### 6.[权限校验]
1. 通过rbac中间件进行权限校验，`settings.py`配置
    ```python
    # 权限校验
    MIDDLEWARE = [
      'django.middleware.security.SecurityMiddleware',
      'django.contrib.sessions.middleware.SessionMiddleware',
      'django.middleware.common.CommonMiddleware',
      'django.middleware.csrf.CsrfViewMiddleware',
      'django.contrib.auth.middleware.AuthenticationMiddleware',
      'django.contrib.messages.middleware.MessageMiddleware',
      'django.middleware.clickjacking.XFrameOptionsMiddleware',
      'rbac.middlewares.rbac.RbacMiddleware',
    ]
    
    # 权限白名单：rbac中间件对用户访问的URL做权限校验时，排除以下URL
    PERMISSION_VALID_URL_LIST = [
        '/login/',
        '/admin/.*',
    ]
    
    # 权限白名单（登录后）
    NO_PERMISSION_URL_LIST = [
        '/index/',
        '/logout/',
    ]
    ```
2. 粒度控制到按钮级别

### 7.[总结]
1. 目的
    * 希望在任意系统中应用权限系统
    * 用户登录 + 用户首页 + 用户注销 业务逻辑
2. 注意：开发时候灵活的去设置layout.html中的两个inclusion_tag
    ```html
    <div class="pg-body">
        <!-- 左侧二级菜单 -->
        <div class="left-menu">
            <div class="menu-body">
                <!-- 开发时，去掉此功能 -->
                {% multi_menu request %}  
            </div>
        </div>
    
        <!-- 右侧信息表格 -->
        <div class="right-body">
    
            <!-- 路径导航 -->
            <div>
                <!-- 开发时，去掉此功能 -->
                {% breadcrumb request %}
            </div>
    
            <!-- 信息表格 -->
            {% block content %}
    
            {% endblock %}
        </div>
    </div>
    ```
3. 配置文件总结
    ```python
    # 注册APP
    INSTALLED_APPS = [
      ...
      'rbac.apps.RbacConfig'
    ]
    # 应用中间件
    MIDDLEWARE = [
      ...
      'rbac.middlewares.rbac.RbacMiddleware',
    ]
    
    # 权限在Session中存储的key
    PERMISSION_SESSION_KEY = "permission_url_list_key"
    
    # 菜单在Session中存储的key
    MENU_SESSION_KEY = "permission_menu_key"
    
    # 权限白名单：rbac中间件对用户访问的URL做权限校验时，排除以下URL
    PERMISSION_VALID_URL_LIST = [
        '/login/',
        '/admin/.*',
    ]
    
    # 权限白名单（登录后）
    NO_PERMISSION_URL_LIST = [
        '/index/',
        '/logout/',
    ]
    
    # 项目URL获取黑名单：自动获取项目中所有URL时，排除以下URL
    AUTO_DISCOVER_EXCLUDE = [
        '/admin/.*',
        '/login/',
        '/logout/',
        '/index/',
    ]
    
    # 业务中的用户表：rbac分配权限时，读取业务表中的用户信息
    RBAC_USER_MODEL_CLASS = "web.models.UserInfo"
    ```