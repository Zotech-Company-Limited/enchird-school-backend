"""
Django settings for enchird_backend project.

Generated by 'django-admin startproject' using Django 4.2.6.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from .env import *
from pathlib import Path
from datetime import timedelta
from rest_framework.settings import api_settings

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-j_tya--8(3c9l^%yx@@nv3*47^7%-bx22jlbwq_qo3q-nuqvae'

# For encyption of assessment questions
FERNET_KEY = '4aBCu0mbi2XbC_ItJZz0iFa6V81xAkIjpRasQnbF_8Q='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['enchird.biz',
                  'https://enchird.biz',
                  '127.0.0.1',
                  'localhost'
]

# Application definition

INSTALLED_APPS = [
    'daphne',
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "corsheaders",
    'core',
    'apis.assessment',
    'apis.applicants',
    'apis.messaging',
    'apis.payments',
    'apis.teachers',
    'apis.students',
    'apis.courses',
    'apis.faculty',
    'apis.users',
    'rest_framework',
    'knox',
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'enchird_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # 'DIRS': ['templates'], 
        'DIRS': [os.path.join(BASE_DIR, 'core', 'templates')],
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

ASGI_APPLICATION = 'enchird_backend.asgi.application'

WSGI_APPLICATION = 'enchird_backend.wsgi.application'


CHANNEL_LAYERS = {
    "default": {"BACKEND": "channels.layers.InMemoryChannelLayer"},
} 

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             # "hosts": [("127.0.0.1", 6379)],
#             "hosts": [("localhost", 6379)],

#         },
#     },
# }


REST_FRAMEWORK = { 
    'DEFAULT_AUTHENTICATION_CLASSES': [ 
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'knox.auth.TokenAuthentication',
    ], 
} 


REST_KNOX = {
  'SECURE_HASH_ALGORITHM': 'cryptography.hazmat.primitives.hashes.SHA512',
  'AUTH_TOKEN_CHARACTER_LENGTH': 64,
  'TOKEN_TTL': timedelta(hours=4),
  'USER_SERIALIZER': 'knox.serializers.UserSerializer',
  'TOKEN_LIMIT_PER_USER': 2,
  'AUTO_REFRESH': False,
  'EXPIRY_DATETIME_FORMAT': api_settings.DATETIME_FORMAT,
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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



AUTH_USER_MODEL = "users.User"


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'filter_info_level': {
            '()': 'core.log_middleware.FilterLevels',
            'filter_levels': [
                "INFO"
            ]
        },
        'filter_error_level': {
            '()': 'core.log_middleware.FilterLevels',
            'filter_levels': [
                "ERROR"
            ]
        },
        'filter_warning_level': {
            '()': 'core.log_middleware.FilterLevels',
            'filter_levels': [
                "WARNING"
            ]
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        }
    },
    'formatters': {
        'info-formatter': {
            'format': '%(levelname)s : %(asctime)s : %(user)s : %(msecs)d : %(message)s : %(module)s : %(exc_info)s'
        },
        'error-formatter': {
            'format': '%(levelname)s : %(asctime)s : %(user)s : %(msecs)d : {%(module)s} : [%(funcName)s] : %(message)s : [in %(pathname)s:%(filename)s:%(lineno)d]',
            'datefmt': '%Y-%m-%d %H:%M'
        },
        'short': {
            'format': '%(levelname)s : %(asctime)s : %(user)s : %(msecs)d : %(message)s : %(module)s : [in %(pathname)s:%(filename)s:%(lineno)d]'
        }
    },
    'handlers': {
        'customHandler_1': {
            'formatter': 'info-formatter',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/logs.log'),
            'encoding': 'utf8',
            'filters': ['filter_info_level'],
        },
        'customHandler_2': {
            'formatter': 'error-formatter',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/logs.log'),
            'encoding': 'utf8',
            'filters': ['filter_error_level'],
        },
        'customHandler_3': {
            'formatter': 'short',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/logs.log'),
            'encoding': 'utf8',
            'filters': ['filter_warning_level'],
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
            'email_backend': 'django.core.mail.backends.filebased.EmailBackend'
        },
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'myLogger': {
            'handlers': [
                'customHandler_1',
                'customHandler_2',
                'customHandler_3',
                'mail_admins',
                'console'
            ],
            'level': 'DEBUG',
        },
    },
}


CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ALL_ORIGINS = True


CORS_ALLOWED_ORIGINS = [
    "http://localhost:8080",
    "http://127.0.0.1:8000",
]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


MEDIA_URL = '/media/'

# if DEBUG:
    
#   STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# else:

#   STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

