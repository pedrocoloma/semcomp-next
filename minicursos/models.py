# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from cms.models.pluginmodel import CMSPlugin
def validaColunas(value):
	if(value > 12 or value < 1):
		raise ValidationError(_(u'Deve haver entre 1 e 12 colunas'))
class MinicursosPluginModel(CMSPlugin):
	columns_small = models.IntegerField(
		_(u'Número de colunas (Telas pequenas)'),
		blank=False,
		validators=[validaColunas],
		)
	columns_medium = models.IntegerField(
		_(u'Número de colunas (Telas médias)'),
		blank=True,
		validators=[validaColunas],
		)
	columns_large = models.IntegerField(
		_(u'Número de colunas (Telas grandes)'),
		blank=True,
		validators=[validaColunas],
		)
	def __unicode__(self):
		return u'Minicursos: (%d/%d/%d) colunas' % (self.columns_small, self.columns_medium, self.columns_large)