"""
Django settings for crmProject project.

Generated by 'django-admin startproject' using Django 3.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pony99r0r3!*&s-y%r%m=i8v3zncp5wej--voka5+u$!ga2*v+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rbac.apps.RbacConfig',
    'stark.apps.StarkConfig',
    'web.apps.WebConfig',
]

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

ROOT_URLCONF = 'crmProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'crmProject.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

# sqlite本地数据库
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': BASE_DIR / 'db.sqlite3',
   }
}
# mysql数据库
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'db_crm',  # 要连接的数据库，连接前需要创建好
#         'USER': 'root',  # 连接数据库的用户名
#         'PASSWORD': '12345678',  # 连接数据库的密码
#         'HOST': '0.0.0.0',  # 连接主机，默认本级
#         'PORT': 3306  # 端口 默认3306
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_ROOT = '/root/static/crm_static/'
STATIC_URL = '/static/'

# ######################################## rbac组件相关配置 ##########################################

# 权限在Session中存储的key
PERMISSION_SESSION_KEY = "permission_url_list_key"

# 菜单在Session中存储的key
MENU_SESSION_KEY = "permission_menu_key"

# 权限白名单：rbac中间件对用户访问的URL做权限校验时，排除以下URL
PERMISSION_VALID_URL_LIST = [
    '/login/',
    '/admin/.*',
    # '/',
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
