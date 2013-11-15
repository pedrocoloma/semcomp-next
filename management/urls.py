from django.conf import settings
from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	url(r'^$', 'management.views.manage_overview', name='management_overview'),

	url(r'^locais/$', 'management.views.manage_places', name='management_places'),
	url(r'^locais/adicionar/$', 'management.views.places_add', name='management_places_add'),
	url(r'^locais/editar/(\d+)/$', 'management.views.places_edit', name='management_places_edit'),
	url(r'^locais/apagar/(\d+)/$', 'management.views.places_delete', name='management_places_delete'),

	url(r'^eventos/$', 'management.views.manage_events', name='management_events'),
	url(r'^eventos/adicionar/$', 'management.views.events_add', name='management_events_add'),
	url(r'^eventos/editar/(\d+)/$', 'management.views.events_edit', name='management_events_edit'),
	url(r'^eventos/apagar/(\d+)/$', 'management.views.events_delete', name='management_events_delete'),

	url(r'^palestras/$', 'management.views.manage_lectures', name='management_lectures'),
	url(r'^minicursos/$', 'management.views.manage_courses', name='management_courses'),
	url(r'^usuarios/$', 'management.views.manage_users', name='management_users'),

	url(r'^empresas/$', 'management.views.manage_companies', name='management_companies'),
	url(r'^empresas/adicionar/$', 'management.views.companies_add', name='management_companies_add'),
	url(r'^empresas/editar/(\d+)/$', 'management.views.companies_edit', name='management_companies_edit'),
	url(r'^empresas/apagar/(\d+)/$', 'management.views.companies_delete', name='management_companies_delete'),
)
