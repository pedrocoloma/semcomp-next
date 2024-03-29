# coding: utf-8

import datetime

from pathlib import Path
from django.core.urlresolvers import reverse_lazy
from django.utils.translation import ugettext_lazy as _

PROJECT_DIR = Path(__file__).resolve().parents[2]

ADMINS = (
    ('Felipe Bessa Coelho', 'fcoelho.9@gmail.com'),
    ('Bruno Orlandi', 'brorlandi@gmail.com'),
    ('André Badawi Missaglia', 'andre.missaglia@gmail.com'),
)
# usuários em MANAGER receberão os e-mails do form de contato
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
	'website.context_processors.semcomp',
)

ROOT_URLCONF = 'semcomp.urls'

TEMPLATE_DIRS = (
	#PROJECT_DIR.joinpath('templates').as_posix(),
)

CMS_TEMPLATES = (
	('website/main_template.html', 'Main Template'),
	('website/home.html', 'Home'),
	('website/tworows.html', 'tworows'),
	('website/empresas.html', 'empresas'),
  ('website/career_fair.html', 'Career fair')
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
    'semcomp_contact_form',
	'stats',
	# django-cms plugins
	'djangocms_flash',
	'djangocms_googlemap',
	'djangocms_inherit',
	'djangocms_link',
	'djangocms_style',
	'djangocms_text_ckeditor',
	'cmsplugin_filer_file',
	'cmsplugin_filer_folder',
	'cmsplugin_filer_image',
	'cmsplugin_filer_teaser',
	'cmsplugin_filer_video',
	# django-cms
	'cms',
	'mptt',
	'menus',
	#'south',
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
    'contact_form',
	'django_gravatar',
)


SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

#COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ['compressor.filters.cssmin.CSSMinFilter']

SEMCOMP_START_DATE = datetime.date(2014, 8, 18)
SEMCOMP_END_DATE = datetime.date(2014, 8, 23)

LOGIN_URL = 'login'
LOGOUT_URL = 'logout'
LOGIN_REDIRECT_URL = 'account_overview'


SOUTH_MIGRATION_MODULES = {
	'easy_thumbnails': 'easy_thumbnails.south_migrations',
}
SOUTH_TESTS_MIGRATE = False

THUMBNAIL_PROCESSORS = (
	'easy_thumbnails.processors.colorspace',
	'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
	'filer.thumbnail_processors.scale_and_crop_with_subject_location',
	'easy_thumbnails.processors.filters',
)

AUTH_USER_MODEL = 'website.SemcompUser'

SIGNUP_FORM_CLASS = 'website.forms.UserSignupForm'
SIGNUP_ALLOWED = 'website.utils.signup_allowed'

SEMCOMP_CONFIG = {
	# Esses são os valores padrão, podem ser alterados em runtime
	'REGISTRATION_DATE': (
		u'Abertura das inscrições',
		'datetime',
		datetime.datetime(2014, 7, 23, 12)),
	'COURSE_REGISTRATION_DATE': (
		u'Abertura das inscrições para minicursos',
		'datetime',
		datetime.datetime(2014, 8, 11, 12)),
	'PAYMENT_DATE': (
		u'Início dos pagamentos',
		'datetime',
		datetime.datetime(2014, 8, 4)),
	'COURSE_CHANGE_DATE_LIMIT': (
		u'Limite para troca de inscrição de minicurso',
		'datetime',
		datetime.datetime(2014, 8, 17)),
}

ELASTICSEARCH_INDEX = 'semcomp-17'
