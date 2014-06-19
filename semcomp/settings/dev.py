from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_DIR.joinpath('database.sqlite3').as_posix(),
    }
}

SECRET_KEY = 'semcomp-eh-demais-de-legal'

WSGI_APPLICATION = 'semcomp.wsgi.dev.application'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_ROOT = PROJECT_DIR.joinpath('media').as_posix()
MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_DIR.joinpath('static').as_posix()
STATIC_URL = '/static/'

# Para enviar e-mails
EMAIL_HOST = 'smtp.mandrillapp.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'USUARIO DO MANDRILL'
EMAIL_HOST_PASSWORD = 'INSIRA A API KEY DO MANDRIL AQUI'

DEFAULT_FROM_EMAIL = 'contato@semcomp.icmc.usp.br'