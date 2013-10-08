from django.db import models
from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin

class Column(CMSPlugin):
	COLUMN_WIDTH_CHOICES = (
		('large-2', _(u'2 columns')),
		('large-4', _(u'4 columns')),
		('large-6', _(u'6 columns')),
		('large-8', _(u'8 columns')),
		('large-10', _(u'10 columns')),
		('large-12', _(u'12 columns')),
	)
	predefined_width = models.CharField(max_length=32, choices=COLUMN_WIDTH_CHOICES)
	custom_width = models.CharField(max_length=32, blank=True)

	def get_width_string(self):
		if self.custom_width:
			return self.custom_width
		else:
			return self.predefined_width
