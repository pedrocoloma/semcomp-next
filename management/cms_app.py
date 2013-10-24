# coding: utf-8

from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class SemcompAdminApphook(CMSApp):
	name = _(u'Administração')
	urls = ['management.urls']
	#menus = [SemcompUserMenu]

apphook_pool.register(SemcompAdminApphook)


