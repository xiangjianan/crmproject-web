## CRM系统

### 1.[功能描述]
1. 对以下数据的基本增删改查管理
    * 菜单、角色、权限
    * 部门、员工、客户
    * 客户跟进记录、客户缴费记录
    * 学校、班级、课程、班主任、讲师、学员
    * 上课记录、考勤记录、学分
2. 支持角色管理，根据业务需求分出销售、销售主管、学员、讲师等角色
3. 支持权限分配
4. 允许销售创建、跟进客户信息，提交客户缴费申请
5. 允许销售主管签审缴费申请
6. 允许讲师提交上课记录、学员签到、学分设置

### 2.[开发环境]
1. 操作系统：macOS10.15.7
2. 解释器版本：python3.7.9
3. web框架：Django3.1.1

### 3.[项目结构简介]
1. crmProject
    * Project
2. rbac
    * App：通用的、达到对象级别的权限控制组件，且允许用户自定制权限
3. stark
    * App：通用的、可插拔式的增删改查组件
4. web
    * App：CRM业务
5. db.sqlite3
    * 数据库：仅做为示例
6. manage.py
7. README

### 4.[启动方式]
#### 方式一：使用示例sqlite数据库
1. pycharm直接运行，或终端输入`python3 manage.py runserver 127.0.0.1:8080`
2. 浏览器访问`http://127.0.0.1:8000/login/`，进行登录
3. 登录信息
    * 管理员账号：admin，密码：admin
    * 讲师账号：小强，密码：123
    * 班主任账号：小红，密码：123
    * 销售账号：小李，密码：123
    * 销售主管账号：小明，密码：123
#### 方式二：自建mysql数据库，需按以下方式初始化权限相关数据：
1. 开启mysql数据库
    * 创建一个新库以存放表
    ```mysql
    create database db_crm;
    ```
    * 修改`crmProject/settings.py`数据库连接配置
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'db_crm',  # 数据库名
            'USER': '****',  # mysql账号
            'PASSWORD': '******',  # mysql密码
            'HOST': '127.0.0.1',
            'PORT': 3306
        }
    }
    ```
2. 数据库迁移
```
python3 manage.py makemigrations
python3 manage.py migrate
```

##### 注：首次启动项目时，需要按照以下步骤操作：

1. 进入`crmProject/settings.py`，注释掉rbac组件的中间件权限校验
```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'rbac.middlewares.rbac.RbacMiddleware',
]
```
2. 进入`rbac/templates/layout.html`，注释掉左侧二级菜单和路径导航功能
```html
 <div class="pg-body">
    <!-- 左侧二级菜单 -->
    <div class="left-menu">
        <div class="menu-body">
{#            {% multi_menu request %}#}
        </div>
    </div>

    <!-- 右侧信息表格 -->
    <div class="right-body">

        <!-- 路径导航 -->
        <div>
{#            {% breadcrumb request %}#}
        </div>

        <!-- 信息表格 -->
        {% block content %}

        {% endblock %}
    </div>
</div>
```
3. 启动项目：pycharm直接运行，或终端输入`python3 manage.py runserver 127.0.0.1:8080`
4. 浏览器访问`http://127.0.0.1:8000/index/`，进行以下操作：
![125fee516332a0b6d14917132d236ac4](README.resources/06399BAA-8CE9-4BB2-818C-8C45F3B192AA.png)
![1883c8888eb2cab8adb62c5d715a1154](README.resources/CFE13F3A-68B0-4525-9B28-087130B3E07D.png)
![8a8c741533168b13d7ac84bb9c084996](README.resources/417CE1BB-AB31-43B7-9905-C2E1D32F3778.png)
![4213e47e4fc0e909b2e83448ad777f25](README.resources/162F5F52-6339-48CC-98DC-3D34972820D4.png)
![bde709e1190bd069a070062ceee67b0a](README.resources/E33E9E29-0A67-4C47-93E2-696EE0330F3F.png)
5. 完成以上操作后，进入项目恢复被注释的代码，并重新启动项目
6. 注销账户，或浏览器访问`http://127.0.0.1:8000/login/`，重新登录，以将带权限的用户权限等信息重新写入session
7. 至此，即可正常使用CRM系统，进行创建用户、角色、权限分配和客户关系管理等操作

### 5.[运行效果]
1. 基于角色的访问控制
* 销售
![c8914b9284463fdd5ebb3fc4d827870c](README.resources/1ACAC9EA-0C6F-4AD7-BFC2-A251557E2AFA.png)
* 销售主管
![52955acf9db2ad823a0ebc0568948bae](README.resources/B81298C6-498D-4D93-BCB3-75F8836D1D76.png)
* 班主任
![22c606ba99272d29589b5e270005f32a](README.resources/B76BEC89-12BD-44A3-A1A0-063AB30E010C.png)
* 讲师
![73e56a84b5066731aa2cd188a7122ce7](README.resources/A0CEE772-8381-41E1-9D5D-ABE27E2F1E6A.png)
![9d31f2a15fc32e44865ce2ceb184053c](README.resources/8A2AE276-2FC2-45D8-88AA-0EC772ED0548.png)
![7dadf2f284fa661d408984a14962fb8c](README.resources/D4DD78EC-F252-4268-8AF9-B146A19819BF.png)
![b46671c40bc3b1e27f24e8a70da31416](README.resources/A99920CA-71FA-45A8-9F77-CBA7034FDA1C.png)
* CEO、管理员
![6a79066369b421078913e5c6d51d52e8](README.resources/8AB28AFB-5C5C-496A-8CD2-C0543A132A53.png)








