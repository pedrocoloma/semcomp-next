import os
from .base import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('SEMCOMP17_DB_NAME'),
        'USER': os.getenv('SEMCOMP17_DB_USER'),
        'PASSWORD': os.getenv('SEMCOMP17_DB_PASS'),
        'HOST': os.getenv('DB_PORT_5432_TCP_ADDR'),
    }
}
INSTALLED_APPS += ('djrill',)
MANDRILL_API_KEY = os.getenv("API_KEY_MANDRILL")
EMAIL_BACKEND = "djrill.mail.backends.djrill.DjrillBackend"

SECRET_KEY = os.getenv('SEMCOMP17_SECRET_KEY')

ALLOWED_HOSTS = ['semcomp.icmc.usp.br']

WSGI_APPLICATION = 'semcomp.wsgi.prod'

MEDIA_ROOT = '/data/media/'
MEDIA_URL = '/17/media/'

STATIC_ROOT = '/data/static/'
STATIC_URL = '/17/static/'

COMPRESS_ENABLED = False
