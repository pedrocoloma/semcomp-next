from .base import *

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_DIR.joinpath('database.sqlite3').as_posix(),
    }
}

WSGI_APPLICATION = 'semcomp.wsgi.dev.application'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'