from django.conf import settings
from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	url(r'^$', 'management.views.manage_overview', name='management_overview'),

	url(r'^mensagens/$', 'management.views.manage_messages', name='management_messages'),
	url(r'^mensagens/(\d+)/$', 'management.views.messages_detail', name='management_messages_detail'),
	url(r'^mensagens/apagar/(\d+)/$', 'management.views.messages_delete', name='management_messages_delete'),

	url(r'^locais/$', 'management.views.manage_places', name='management_places'),
	url(r'^locais/adicionar/$', 'management.views.places_add', name='management_places_add'),
	url(r'^locais/editar/(\d+)/$', 'management.views.places_edit', name='management_places_edit'),
	url(r'^locais/apagar/(\d+)/$', 'management.views.places_delete', name='management_places_delete'),

	url(r'^eventos/$', 'management.views.manage_events', name='management_events'),
	url(r'^eventos/adicionar/$', 'management.views.events_add', name='management_events_add'),
	url(r'^eventos/editar/(\d+)/$', 'management.views.events_edit', name='management_events_edit'),
	url(r'^eventos/apagar/(\d+)/$', 'management.views.events_delete', name='management_events_delete'),

	url(r'^palestras/$', 'management.views.manage_lectures', name='management_lectures'),
	url(r'^palestras/adicionar/$', 'management.views.lectures_add', name='management_lectures_add'),
	url(r'^palestras/editar/(\d+)/$', 'management.views.lectures_edit', name='management_lectures_edit'),
	url(r'^palestras/apagar/(\d+)/$', 'management.views.lectures_delete', name='management_lectures_delete'),

	url(r'^minicursos/$', 'management.views.manage_courses', name='management_courses'),
	url(r'^minicursos/adicionar/$', 'management.views.courses_add', name='management_courses_add'),
	url(r'^minicursos/editar/(\d+)/$', 'management.views.courses_edit', name='management_courses_edit'),
	url(r'^minicursos/apagar/(\d+)/$', 'management.views.courses_delete', name='management_courses_delete'),


	url(r'^usuarios/$', 'management.views.manage_users', name='management_users'),
	url(r'^usuarios/edit/(\d+)$', 'management.views.users_edit', name='management_users_edit'),
	url(r'^usuarios/validate/(\d+)$', 'management.views.users_validate', name='management_users_validate'),

	url(r'^empresas/$', 'management.views.manage_companies', name='management_companies'),
	url(r'^empresas/adicionar/$', 'management.views.companies_add', name='management_companies_add'),
	url(r'^empresas/editar/(\d+)/$', 'management.views.companies_edit', name='management_companies_edit'),
	url(r'^empresas/apagar/(\d+)/$', 'management.views.companies_delete', name='management_companies_delete'),

	url(r'^processos/$', 'management.views.manage_processes', name='management_processes'),
	url(r'^processos/adicionar/$', 'management.views.processes_add', name='management_processes_add'),
	url(r'^processos/editar/(\d+)/$', 'management.views.processes_edit', name='management_processes_edit'),
	url(r'^processos/apagar/(\d+)/$', 'management.views.processes_delete', name='management_processes_delete'),

	url(r'^palestras-empresariais/$', 'management.views.manage_business_lectures', name='management_business_lectures'),
	url(r'^palestras-empresariais/adicionar/$', 'management.views.business_lectures_add', name='management_business_lectures_add'),
	url(r'^palestras-empresariais/editar/(\d+)/$', 'management.views.business_lectures_edit', name='management_business_lectures_edit'),
	url(r'^palestras-empresariais/deletar/(\d+)/$', 'management.views.business_lectures_delete', name='management_business_lectures_delete'),

	url(r'^configuracoes/$', 'management.views.manage_config', name='management_config'),

)
