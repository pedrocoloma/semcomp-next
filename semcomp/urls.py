# coding: utf-8

import os
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin


from solid_i18n.urls import solid_i18n_patterns

admin.autodiscover()

urlpatterns = solid_i18n_patterns('',
    url(r'^djangoadmin/', include(admin.site.urls)),
	url(r'^accounts/', include('signup.urls')),
	url(r'^select2/', include('django_select2.urls')),
	url(r'^', include('website.urls')),
	url(r'^', include('cms.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# isso está aqui porque esse módulo só é carregado quando chega a primeira
# requisição. ela é colocada aqui porque ela precisa que as tabelas já existam
# e assim ela é executada só uma vez antes de todo o resto
from website.utils import create_semcomp_config
create_semcomp_config()
