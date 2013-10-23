# coding: utf-8

from menus.base import NavigationNode, Menu, Modifier
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _
from cms.menu_bases import CMSAttachMenu

class SemcompUserMenu(Menu):
	name = _(u'Menu de usuário')

	def get_nodes(self, request):
		nodes = []

		if request.user.is_authenticated():
			n = NavigationNode(_(u'Área de usuário'), '/account/', 1)
		else:
			n = NavigationNode(_(u'Login'), '/accounts/login/', 1)
		nodes.append(n)
		return nodes

menu_pool.register_menu(SemcompUserMenu)
