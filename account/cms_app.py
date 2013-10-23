# coding: utf-8

from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

from .menu import SemcompUserMenu

class SemcompUserApphook(CMSApp):
	name = _(u'Área do usuário')
	urls = ['account.urls']
	#menus = [SemcompUserMenu]

apphook_pool.register(SemcompUserApphook)
