# coding: utf-8

from django.conf import settings
from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	# versões com e sem slug para os dois casos
	url(r'^programacao/evento/(\d+)/$', 'website.views.event_details', name='event_details'),
	url(r'^programacao/evento/(\d+)/([-\w]+)/$', 'website.views.event_details', name='event_details_slug'),
	url(r'^programacao/minicurso/(\d+)/$', 'website.views.course_details', name='course_details'),
	url(r'^programacao/minicurso/(\d+)/([-\w]+)/$', 'website.views.course_details', name='course_details_slug'),
)
