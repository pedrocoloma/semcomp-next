from django.conf import settings
from django.conf.urls import patterns, url, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin

from solid_i18n.urls import solid_i18n_patterns

admin.autodiscover()

urlpatterns = solid_i18n_patterns('',
	url(r'^djangoadmin/', include(admin.site.urls)),
	url(r'^blog/', include('zinnia.urls')),
	url(r'^', include('cms.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

