"""
Django settings for RbacProject project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '8fmtcntjh4xow$$7@(nyk^q0voy!jy!8ixmnxz&4+-jdc=$90*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rbac',
    'web',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'rbac.middleware.rbac.RbacMiddleware',
]

ROOT_URLCONF = 'RbacProject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
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

WSGI_APPLICATION = 'RbacProject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# ################ RBAC权限相关配置 ################
# 无权限控制的URL
RBAC_NO_AUTH_URL = [
    '/index.html',
    '/login.html',
    '/logout.html',
    '/register.html',
    '/admin.*',
    '/rbac.*',
]

# session中保存权限信息的key
RBAC_PERMISSION_SESSION_KEY = "rbac_permission_session_key"

# Http请求中传入的参数，根据其获取GET、POST、EDIT、等检测用户是否具有相应权限
# 例如：
#   http://www.example.com?md=get   表示获取
#   http://www.example.com?md=post   表示添加
#   http://www.example.com?md=del   表示删除
RBAC_QUERY_KEY = "md"
RBAC_DEFAULT_QUERY_VALUE = "look"

# 无权限访问时，页面提示信息
RBAC_PERMISSION_MSG = "无权限访问"

# session中保存菜单和权限信息的key
RBAC_MENU_PERMISSION_SESSION_KEY = "rbac_menu_permission_session_key"
RBAC_MENU_PERMISSION_KEY = "rbac_menu_permission_key"
RBAC_MENU_KEY = "rbac_menu_key"

# 菜单主题
RBAC_THEME = "default"
# ################ RBAC权限相关配置结束 ################