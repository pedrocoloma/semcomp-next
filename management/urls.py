from django.conf import settings
from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	url(r'^$', 'management.views.manage_overview', name='management_overview'),
	url(r'^palestras/$', 'management.views.manage_lectures', name='management_lectures'),
	url(r'^minicursos/$', 'management.views.manage_courses', name='management_courses'),
)
