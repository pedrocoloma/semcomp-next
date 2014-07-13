# -*- coding:utf-8 -*-
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db import models
from cms.models.pluginmodel import CMSPlugin
def validaColunas(value):
	if(value > 12 or value < 1):
		raise ValidationError(_(u'Deve haver entre 1 e 12 colunas'))
class MinicursosPluginModel(CMSPlugin):
	colunas = models.IntegerField(
		_(u'Número de colunas'),
		blank=False,
		validators=[validaColunas],
		)
	def __unicode__(self):
		return u'Minicursos: %d colunas' % (self.colunas,)