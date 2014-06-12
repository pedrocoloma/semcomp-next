# coding: utf-8

from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.tests.utils import skipIfCustomUser
from django.core.urlresolvers import reverse
from django.template import Template, Context, RequestContext
from django.test import TestCase
from django.test.client import RequestFactory
from django.utils import six

from menus.menu_pool import menu_pool

class UserMenuTests(TestCase):
	def setUp(self):
		UserModel = get_user_model()
		self.factory = RequestFactory()
		self.anon_user = AnonymousUser()
		self.default_user = UserModel.objects.create_user(
			'user',
			'email@provider.com',
			'John Doe',
			'pass',
		)

	def get_menu_titles(self, user):
		# o RequestFactory é um troço bem simples que não lida com sessões ou
		# autenticação. Precisa colocar o atributo do usuário na mão
		request = self.factory.get('/')
		request.user = user

		# Isso aqui é uma lista (gênio)
		menu_nodes = menu_pool.get_nodes(request)
		# a função get_menu_title retorna um objeto do tipo
		# django.utils.functional.__proxy__, que nada mais é do que uma string
		# que foi passada pro gettext como _('string em português'). Pra ela
		# virar uma "string de verdade", precisa chamar unicode(proxy). Mas
		# como em python 3 não existe o tipo "unicode", eu uso six.text_type,
		# que é str em py3 ou unicode em py2 e fica tudo certo
		menu_title_proxies = [n.get_menu_title() for n in menu_nodes]
		menu_titles = map(six.text_type, menu_title_proxies)

		return menu_titles

	def test_user_logged_in_menu(self):
		menu_titles = self.get_menu_titles(self.default_user)

		self.assertIn('Área de usuário', menu_titles)
		self.assertNotIn('Entrar', menu_titles)

	def test_user_not_logged_in_menu(self):
		menu_titles = self.get_menu_titles(self.anon_user)

		self.assertNotIn('Área de usuário', menu_titles)
		self.assertIn('Entrar', menu_titles)

