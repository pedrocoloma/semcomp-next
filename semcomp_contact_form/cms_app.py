from django.utils.translation import ugettext_lazy as _

from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool

class SemcompContatoApphook(CMSApp):
	name = _(u'Contato')
	urls = ['semcomp_contact_form.urls']

apphook_pool.register(SemcompContatoApphook)
