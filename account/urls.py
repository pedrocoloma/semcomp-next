from django.conf import settings
from django.conf.urls import patterns, url, include

urlpatterns = patterns('',
	url(r'^$', 'account.views.account_overview', name='account_overview'),
	url(r'^pagamento/$', 'account.views.payment_overview', name='account_payment'),
	url(r'^pagamento/send/$', 'account.views.payment_send', name='account_payment_send'),
	url(r'^minicursos/$', 'account.views.courses', name='account_courses'),
	url(r'^logout/$', 'account.views.account_logout', name='account_logout'),
)
