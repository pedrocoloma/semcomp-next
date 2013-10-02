from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_PATH.child('database.sqlite3'),
    }
}

WSGI_APPLICATION = 'semcomp.wsgi.dev.application'
