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
INSTALLED_APPS += (
	'raven.contrib.django.raven_compat',
)

EMAIL_BACKEND = "sgbackend.SendGridBackend"
SENDGRID_USER = os.getenv('SEMCOMP17_SENDGRID_USER')
SENDGRID_PASSWORD = os.getenv('SEMCOMP17_SENDGRID_PASSWORD')

SECRET_KEY = os.getenv('SEMCOMP17_SECRET_KEY')

ALLOWED_HOSTS = ['semcomp.icmc.usp.br']

WSGI_APPLICATION = 'semcomp.wsgi.prod'

MEDIA_ROOT = '/data/media/'
MEDIA_URL = '/17/media/'

STATICFILES_DIRS = (
	PROJECT_DIR.joinpath('website/static/production').as_posix(),
)

STATIC_ROOT = '/data/static/'
STATIC_URL = '/17/static/'

COMPRESS_ENABLED = False

DEFAULT_FROM_EMAIL = 'Semcomp 17 <no-reply@semcomp.icmc.usp.br>'

RAVEN_CONFIG = {
	'dsn': os.getenv('RAVEN_CONFIG'),
}

