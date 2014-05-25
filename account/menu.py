# coding: utf-8

from menus.base import NavigationNode, Menu, Modifier
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse
from cms.menu_bases import CMSAttachMenu

class SemcompUserMenu(Menu):
	name = _(u'Menu de usuário')

	def get_nodes(self, request):
		return [
			NavigationNode(
				_(u'Área de usuário'),
				reverse('account_overview'),
				1,
				attr={'visible_for_anonymous': False}),
			NavigationNode(
				_(u'Entrar'),
				reverse('login'),
				2,
				attr={'visible_for_authenticated': False})
		]

menu_pool.register_menu(SemcompUserMenu)
