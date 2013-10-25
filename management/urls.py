from django.conf import settings
from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	url(r'^$', 'management.views.manage_overview', name='management_overview'),
	url(r'^palestras/$', 'management.views.manage_lectures', name='management_lectures'),
	url(r'^minicursos/$', 'management.views.manage_courses', name='management_courses'),
	url(r'^empresas/$', 'management.views.manage_companies', name='management_companies'),
	url(r'^empresas/adicionar/$', 'management.views.companies_add', name='management_companies_add'),
)
