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

#MIDDLEWARE_CLASSES += (
#	'debug_toolbar.middleware.DebugToolbarMiddleware',
#) + MIDDLEWARE_CLASSES

#INTERNAL_IPS = ('127.0.0.1',)

#INSTALLED_APPS += (
#	'debug_toolbar',
#)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'