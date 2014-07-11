from django.conf import settings
from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	url(r'^programacao/evento/(\d+)/$', 'website.views.event_details', name='event_details'),
	url(r'^programacao/minicurso/(\d+)/$', 'website.views.course_details', name='course_details'),
)
