import json

"""
Django settings for wazieats project.

Generated by 'django-admin startproject' using Django 4.0.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'zotechin_enchird_database',
#         'USER': 'zotechin_enchird_database',
#         'PASSWORD': 'td5Z2JaVre&@Y&BaIBCSfY)k',
#         'HOST': 'localhost',
#         'PORT': '',            # Set to empty string for default
#         'OPTIONS': {
#             'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
#         }
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'enchird_database',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': 'localhost',
        'PORT': '',            # Set to empty string for default
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        }
    }
}


EMAIL_HOST='smtp.gmail.com'
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER='jvperezmbi@gmail.com'
EMAIL_HOST_PASSWORD='qamgdgifrpkuikdn' 
EMAIL_BACKEND='django.core.mail.backends.smtp.EmailBackend'


STRIPE_SECRET_KEY = "sk_test_51OgXepCpGGidDqruGkH0m0MOcY9sV2b7x705PYaeX6TpVvHZzqAEMo2LparLIBohDDkNUHn7Mf0zDdPT0SABkZiS00L34VogCY"

WEBHOOK_SECRET = "whsec_adfa434b2296982dae737e2bd798b52f27bc232cea8a5e93bce79026b41d5380"
