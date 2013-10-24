# coding: utf-8

from unipath import Path
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

PROJECT_DIR = Path(__file__).absolute().ancestor(3)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

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

MEDIA_ROOT = PROJECT_DIR.child('media')
MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_DIR.child('static')
STATIC_URL = '/static/'

SECRET_KEY = 'semcomp-eh-demais-de-legal'

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
	'zinnia.context_processors.version',
)

ROOT_URLCONF = 'semcomp.urls'

TEMPLATE_DIRS = (
	#PROJECT_DIR.child('templates'),
)

CMS_TEMPLATES = (
	('website/main_template.html', 'Main Template'),
	('website/home.html', 'Home'),
)

LANGUAGES = [
	('pt-br', u'Português'),
]

INSTALLED_APPS = (
	# semcomp apps
	'website',
	'account',
	'management',
	# django-cms plugins
	'cms.plugins.file',
	'cms.plugins.flash',
	'cms.plugins.googlemap',
	'cms.plugins.link',
	'cms.plugins.picture',
	#'cms.plugins.snippet', #security hazard
	'cms.plugins.teaser',
	'djangocms_text_ckeditor',
	'cms.plugins.video',
	'cmsplugin_zinnia',
	# django-cms
	'cms',
	'cms.stacks',
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
	'tagging',
	'zinnia',
	'compressor',
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

ZINNIA_AUTO_CLOSE_COMMENTS_AFTER = 0
#ZINNIA_ENTRY_BASE_MODEL = 'cmsplugin_zinnia.placeholder.EntryPlaceholder'
CMSPLUGIN_ZINNIA_APP_MENUS = []
CMSPLUGIN_ZINNIA_TEMPLATES = [
	('blog/latest_entries.html', _(u'Entries with title and date')),
]

#COMPRESS_ENABLED = True
