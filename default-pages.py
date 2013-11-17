# coding: utf-8

from cms.api import create_page, add_plugin
from cms.stacks.models import Stack
import sys
from website.cms_plugins import MultiColumnsPlugin, ColumnPlugin
from cms.models.pluginmodel import CMSPlugin

from cms.models import Page
from cmsplugin_zinnia.cms_app import ZinniaApphook
from cmsplugin_zinnia.cms_plugins import CMSLatestEntriesPlugin
from account.cms_app import SemcompUserApphook
from management.cms_app import SemcompAdminApphook
from contextlib import contextmanager
from website.models import Column
from django.contrib.auth.models import User

@contextmanager
def progress(msg):
	sys.stdout.write('%s... ' % msg)
	sys.stdout.flush()
	yield
	sys.stdout.write('OK!\n')

HOME_TEMPLATE = 'website/home.html'
MAIN_TEMPLATE = 'website/main_template.html'
LANGUAGE_PT_BR = 'pt-br'

pages = [
	('home', {
		'title': u'Home',
		'template': HOME_TEMPLATE,
		'reverse_id': 'home'
	}),
	('sobre', {
		'title': u'Sobre',
	}),
	('programacao', {
		'title': u'Programação',
	}),
	('inscricoes', {
		'title': u'Inscrições',
	}),
	('account', {
		'title': u'Área do usuário',
		'slug': 'account',
		'apphook': SemcompUserApphook,
		'in_navigation': False,
	}),
	('admin', {
		'title': u'Administração',
		'apphook': SemcompAdminApphook,
		'in_navigation': False,
		'reverse_id': 'admin',
	}),

	('sobre-semcomp', {
		'title': u'A Semcomp',
		'slug': 'semcomp',
		'parent': 'sobre'
	}),
	('sobre-contato', {
		'title': u'Contato',
		'parent': 'sobre',
	}),
	('sobre-faq', {
		'title': u'FAQ',
		'parent': 'sobre',
	}),
	('sobre-noticias', {
		'title': u'Notícias',
		'apphook': ZinniaApphook,
		'parent': 'sobre',
		'overwrite_url': '/blog',
	}),

	('programacao-visao-geral', {
		'title': u'Visão geral',
		'redirect': '/programacao/',
		'parent': 'programacao',
	}),
	('programacao-palestras', {
		'title': u'Palestras',
		'parent': 'programacao',
	}),
	('programacao-minicursos', {
		'title': u'Minicursos',
		'parent': 'programacao'
	}),

	('inscricoes-fazer-inscricao', {
		'title': u'Fazer inscrição',
		'parent': 'inscricoes',
	}),
	('inscricoes-precos', {
		'title': u'Preços',
		'parent': 'inscricoes',
	})
]

print 'Deleting existing pages... ',
sys.stdout.flush()
Page.objects.all().delete()
print 'OK!\n'

created_pages = {}

print 'Creating pages...'
for page_name,page_data in pages:
	if 'parent' in page_data:
		page_data['parent'] = created_pages[page_data['parent']]
	
	in_navigation = page_data.pop('in_navigation', True)

	with progress('Creating %s' % page_name):
		sys.stdout.flush()
		created_pages[page_name] = create_page(
			page_data.pop('title'),
			page_data.pop('template', MAIN_TEMPLATE),
			LANGUAGE_PT_BR,
			in_navigation=in_navigation,
			published=True,
			**page_data
		)

with progress('Creating stacks'):
	multicolumn_stacks = [
		{
			'name': 'StackImageLeft',
			'code': 'stack-image-left',
			'columns': [
				'large-4',
				'large-8'
			]
		},
		{
			'name': 'StackImageRight',
			'code': 'stack-image-right',
			'columns': [
				'large-4 push-8',
				'large-8 pull-4'
			]
		}

	]

	for stack in multicolumn_stacks:
		s = Stack(name=stack['name'], code=stack['code'])
		s.save()

		placeholder = s.content
		multi_columns_plugin = add_plugin(placeholder, MultiColumnsPlugin, LANGUAGE_PT_BR)

		for i,column_spec in enumerate(stack['columns']):
			plugin = CMSPlugin(
				plugin_type='ColumnPlugin',
				position=i,
				placeholder=placeholder,
				language=LANGUAGE_PT_BR
			)
			plugin.insert_at(multi_columns_plugin)

			data = Column(custom_classes=column_spec)

			plugin.set_base_attr(data)

			data.save()

with progress('Adding plugins'):
	side_content = created_pages['home'].placeholders.get(slot='side_content')
	add_plugin(side_content, CMSLatestEntriesPlugin, 'pt-br', render_template='blog/latest_entries.html')
	add_plugin(side_content, "TextPlugin", LANGUAGE_PT_BR, body='<h2>Quer ser um patrocinador?</h2><p>Entre em <a href="/sobre/contato">contato</a>!</p>')

with progress('Creating super user'):
	User.objects.create_superuser('admin', 'admin@admin.net', 'senha')

with progress('(Re-)publishing pages'):
	for name, page in created_pages.items():
		page.publish()
