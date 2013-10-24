from django.conf import settings
from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	url(r'^$', 'website.views.manage_overview', name='management_overview'),
	url(r'^palestras/$', 'website.views.manage_lectures', name='management_lectures'),
	url(r'^minicursos/$', 'website.views.manage_courses', name='management_courses'),
)
