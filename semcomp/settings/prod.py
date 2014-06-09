from .base import *

import os

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DB_ENV_DB'),
        'USER': os.getenv('DB_ENV_USER'),
        'PASSWORD': os.getenv('DB_ENV_PASS'),
        'HOST': os.getenv('DB_PORT_5432_TCP_ADDR'),
    }
}

SECRET_KEY = os.getenv('SEMCOMP17_SECRET_KEY')

ALLOWED_HOSTS = ['semcomp.icmc.usp.br']

WSGI_APPLICATION = 'semcomp.wsgi.prod'

MEDIA_ROOT = '/data/media/'
MEDIA_URL = '/17/media/'

STATIC_ROOT = '/data/static/'
STATIC_URL = '/17/static/'

COMPRESS_ENABLED = True
