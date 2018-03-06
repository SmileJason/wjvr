# -*- coding: utf-8 -*-
"""
Django settings for wjvr project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mj!v0_g9+(a77!=oi7qv)0bl7%f6hd+t=h91ojl8(j*8_u8d*9'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# COMPRESS_ENABLED = True
# COMPRESS_OFFLINE = True
# COMPRESS_OUTPUT_DIR = 'mini'
# COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.CSSMinFilter']
# COMPRESS_ROOT = 'Templates/include/'
# COMPRESS_URL = 'include/'
# COMPRESS_ENABLED = True

ALLOWED_HOSTS = ['123.207.251.42', 'wjvr.json666.cn']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'compressor',

    'xadmin',
    'crispy_forms',
    'DjangoUeditor',

    'vrauth',
    'vrmode',
    'api',
    'favourite',
    'community',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'wjvr.urls'

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

WSGI_APPLICATION = 'wjvr.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DATETIME_FORMAT = 'Y-m-d H:i:s'

DATE_FORMAT = 'Y-m-d'
TIME_FORMAT = 'H:i:s'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# log配置
# LOG_FILE = "./wjvr.log"

# cache配置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'options': {
            'MAX_ENTRIES': 1024,
        }
    },
    'memcache': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        # 'LOCATION': 'unix:/home/billvsme/memcached.sock',
        'LOCATION': '127.0.0.1:11211',
        'options': {
            'MAX_ENTRIES': 1024,
        }
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
   'formatters': {
       'detail': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d[%(pathname)s:%(lineno)d] %(message)s'
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s [%(pathname)s:%(lineno)d] %(message)s'
        },
        'simple':{
            'format': '%(levelname)s %(asctime)s [%(lineno)d] %(message)s'
        },
        'operation': {
            'format': '[%(asctime)s] %(message)s'
        },
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'wjvr.log'),
            'formatter': 'verbose',
            'maxBytes': 1024*1024*20,  # 20MB
            'backupCount': 0,
        },
        'file-socket':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'wjvr-socket.log'),
            'formatter': 'simple',
            'maxBytes': 1024*1024*20,  # 20MB
            'backupCount': 0,
        },
        'file-socket-listener':{
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'wjvr-socket-listener.log'),
            'formatter': 'simple',
            'maxBytes': 1024*1024*20,  # 20MB
            'backupCount': 0,
        },
    },
    'loggers': {
        'wjvr.server': {
            'handlers': ['console', 'file'] if DEBUG else ['file'],
            'level': 'DEBUG' if DEBUG else 'DEBUG' #'INFO'
        },
    }
}

# 设置user model
AUTH_USER_MODEL = "vrauth.VRAuth"

# cache配置
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
        'options': {
            'MAX_ENTRIES': 1024,
        }
    },
    'memcache': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        # 'LOCATION': 'unix:/home/billvsme/memcached.sock',
        'LOCATION': '127.0.0.1:11211',
        'options': {
            'MAX_ENTRIES': 1024,
        }
    },
}

