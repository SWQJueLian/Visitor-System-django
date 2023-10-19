"""
Django settings for vistor project.

Generated by 'django-admin startproject' using Django 3.2.20.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-&w%%nikxf3athx&3l&j9mu5^vnzi63(^@#268m*5540a@tqp31'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [
    "127.0.0.1",
    "192.168.2.73",
]


# Application definition

EXACT_APPS = [
    # DRF要注册这个子应用
    'rest_framework',
    'corsheaders',
    # django-rest-framework-jwt 本地化翻译，（可选..）
    'rest_framework_simplejwt',
]

LOCAL_APPS = [
    'invite.apps.InviteConfig',
    'oauth.apps.OauthConfig',
]

DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS = DJANGO_APPS + EXACT_APPS + LOCAL_APPS

MIDDLEWARE = [
    # cors跨域的中间层必须放在最上面
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vistor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'vistor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'zh-Hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# 执行py manager.py collectstatic时会将所有静态文件存放到该目录下
STATIC_ROOT = BASE_DIR / 'collect_static_files'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


######### Django-restframework #########
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # 使用drf-JWT验证(我改过的认证)
        'common.authentication.MyJWTAuthentication',
        # 关闭drf session认证中的csrf
        'common.mixins.NoneCSRFSessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
        # 基于Django的模型权限校验
        # 'rest_framework.permissions.DjangoModelPermissions',
    ],
    # 定义统一异常处理函数
    'EXCEPTION_HANDLER': "common.exceptions.exception_handlers.custom_exception_handler",
    # 非模型字段异常时的key的名称，默认为non_field_errors
    # "NON_FIELD_ERRORS_KEY": "other_error",
    # 这个是用来给DRF自带的openapi用的，和yasg没啥关系，但是需要用来展示对比swagger、redoc和自带的区别
    # 'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'
}

#########  日志配置  ##########
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,  # 是否禁用已经存在的日志器
    'formatters': {  # 日志信息显示的格式
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(module)s %(lineno)d %(message)s'
        },
    },
    'filters': {  # 对日志进行过滤
        'require_debug_true': {  # django在debug模式下才输出日志
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {  # 日志处理方法
        'console': {  # 向终端中输出日志
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {  # 向文件中输出日志
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs/vistor.log',  # 日志文件的位置
            'maxBytes': 300 * 1024 * 1024,
            'backupCount': 10,
            'formatter': 'verbose'
        },
    },
    'loggers': {  # 日志器
        'django': {  # 定义了一个名为django的日志器
            'handlers': ['console', 'file'],  # 可以同时向终端与文件中输出日志
            'propagate': True,  # 是否继续传递日志信息
            'level': 'INFO',  # 日志器接收的最低日志级别
        },
    }
}

#############  跨域设置  #############

# 允许跨域时携带cookie，不加一样不能跨域
CORS_ALLOW_CREDENTIALS = True

# 注意:在Django 2.1中增加了SESSION_COOKIE_SAMESITE设置，默认设置为'Lax'，这将防止Django的会话cookie被跨域发送。将其更改为“None”以绕过此安全限制。

SESSION_COOKIE_SAMESITE = None

NGROK_SUBDOMAN = 'https://661a-116-22-22-232.ngrok-free.app'

# 设置允许跨域的源
CORS_ALLOWED_ORIGINS = [
    'http://127.0.0.1:8080',
    'http://127.0.0.1:5173',
    'http://localhost:5173',
    'http://localhost:8080',
    NGROK_SUBDOMAN,
]

# 使用正则表达式来配置允许的源
# CORS_ALLOWED_ORIGIN_REGEXES = [
#     r"^https://\w+\.example\.com$",
# ]

# 允许所有源
# CORS_ALLOW_ALL_ORIGINS = True

#### 企业微信相关信息 ####
WXWORK_COPRID = '填你自己的'
WXWORK_APP_SECRET = '填你自己的'
WXWORK_APP_AGENT_ID = '填你自己的'
WXWORK_REDIRECT_URI = NGROK_SUBDOMAN + '/wxwork-oauth'


SIMPLE_JWT = {
    "TOKEN_OBTAIN_SERIALIZER": "common.token_serializer.WxworkTokenObtainPairSerializer",
    "USER_ID_FIELD": 'employee_id',
    # "USER_ID_CLAIM": 'employee_id',
    # ACCESS TOKEN 有效期
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
}
