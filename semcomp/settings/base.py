# coding: utf-8

import datetime

from pathlib import Path
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

PROJECT_DIR = Path(__file__).resolve().parents[2]

ADMINS = (
    ('Felipe Bessa Coelho', 'fcoelho.9@gmail.com'),
)
MANAGERS = ADMINS

TIME_ZONE = 'America/Sao_Paulo'

LANGUAGE_CODE = 'pt-br'

SITE_ID = 1

USE_I18N = True
USE_L10N = True
USE_TZ = True

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',
	'compressor.finders.CompressorFinder',
)

MIDDLEWARE_CLASSES = (
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	#SolidLocaleMiddleware instead of Django's built-in
	#'django.middleware.locale.LocaleMiddleware',
	'solid_i18n.middleware.SolidLocaleMiddleware',
	'django.middleware.doc.XViewMiddleware',
	'django.middleware.common.CommonMiddleware',
	'cms.middleware.page.CurrentPageMiddleware',
	'cms.middleware.user.CurrentUserMiddleware',
	'cms.middleware.toolbar.ToolbarMiddleware',
	'cms.middleware.language.LanguageCookieMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
	'django.contrib.auth.context_processors.auth',
	'django.contrib.messages.context_processors.messages',
	'django.core.context_processors.i18n',
	'django.core.context_processors.request',
	'django.core.context_processors.media',
	'django.core.context_processors.static',
	'cms.context_processors.media',
	'sekizai.context_processors.sekizai',
)

ROOT_URLCONF = 'semcomp.urls'

TEMPLATE_DIRS = (
	#PROJECT_DIR.joinpath('templates').as_posix(),
)

CMS_TEMPLATES = (
	('website/main_template.html', 'Main Template'),
	('website/home.html', 'Home'),
	('website/tworows.html', 'tworows'),
)

CMS_PERMISSION = True

LANGUAGES = [
	('pt-br', u'Português'),
]

INSTALLED_APPS = (
	# semcomp apps
	'website',
	'account',
	'management',
	'semcomp_plugins',
	# django-cms plugins
	'djangocms_file',
	'djangocms_flash',
	'djangocms_googlemap',
	'djangocms_inherit',
	'djangocms_link',
	'djangocms_picture',
	'djangocms_style',
	'djangocms_teaser',
	'djangocms_text_ckeditor',
	'djangocms_video',
	# django-cms
	'cms',
	'mptt',
	'menus',
	'south',
	'sekizai',
	'djangocms_admin_style',
	# django contrib apps
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.comments',
	'django.contrib.sessions',
	'django.contrib.sites',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'django.contrib.admin',
	# third party apps
	'reversion',
	#'compressor',
	'mathfilters',
	'signup',
	'aldryn_blog',
	'aldryn_common',
	'django_select2',
	'easy_thumbnails',
	'filer',
	'taggit',
	'cmsplugin_flickr_slideshow',
)


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
		}
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
#		'django.db.backends': {
#			'level': 'DEBUG',
#			'handlers': ['console'],
#		},
    }
}

#COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.CSSMinFilter']

SEMCOMP_START_DATE = datetime.date(2014, 8, 25)
SEMCOMP_END_DATE = datetime.date(2014, 8, 30)

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'account_overview'


SOUTH_MIGRATION_MODULES = {
	'easy_thumbnails': 'easy_thumbnails.south_migrations',
}

THUMBNAIL_PROCESSORS = (
	'easy_thumbnails.processors.colorspace',
	'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
	'filer.thumbnail_processors.scale_and_crop_with_subject_location',
	'easy_thumbnails.processors.filters',
)

AUTH_USER_MODEL = 'website.SemcompUser'

SIGNUP_FORM_CLASS = 'website.forms.UserSignupForm'
