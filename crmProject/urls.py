"""crmProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from stark.service.stark import site
from web.views import account

urlpatterns = [
    path('admin/', admin.site.urls),

    # rbac
    path('rbac/', include('rbac.urls', namespace='rbac')),

    # 业务系统：stark入口
    path('stark/', site.urls),

    # 基本登录
    path('', account.login),
    path('login/', account.login),
    path('logout/', account.logout, name='logout'),
    path('index/', account.index, name='index'),
]
