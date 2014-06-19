import os
from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin


from solid_i18n.urls import solid_i18n_patterns

if os.getenv('DJANGO_SETTINGS_MODULE').endswith('prod'):
	from djrill import DjrillAdminSite
	admin.site = DjrillAdminSite()

admin.autodiscover()

urlpatterns = solid_i18n_patterns('',
    url(r'^contato/', include('contact_form.urls')),
    url(r'^djangoadmin/', include(admin.site.urls)),
	url(r'^accounts/', include('signup.urls')),
	# isso tem que ficar antes do cms.urls
	url(r'^account/', include('account.urls')),
	url(r'^', include('cms.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

