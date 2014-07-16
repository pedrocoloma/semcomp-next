# -*- coding:utf-8 -*-
from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from django.core.exceptions import ValidationError

# Create your models here.
from cms.models.pluginmodel import CMSPlugin

class MultiColumns(CMSPlugin):
       def __unicode__(self):
               return _(u'%s columns') % self.cmsplugin_set.all().count()

class Column(CMSPlugin):
       COLUMN_WIDTH_CHOICES = map(
               lambda x:
                       (str(x), ungettext_lazy(u'%i column', u'%i columns', x) % x),
               range(1,13)
       )

       small_width = models.CharField(
               max_length=2,
               blank=True,
               choices=COLUMN_WIDTH_CHOICES
       )
       large_width = models.CharField(
               max_length=2,
               blank=True,
               choices=COLUMN_WIDTH_CHOICES
       )
       custom_classes = models.CharField(
               max_length=64,
               blank=True,
               help_text=_(u'Este campo tem prioridade sobre os campos acima')
       )

       def get_width_string(self):
               custom = self.custom_classes.strip()
               if custom:
                       return custom

               small = 'small-%s' % self.small_width if self.small_width else ''
               large = 'large-%s' % self.large_width if self.large_width else ''

               return ' '.join([small, large]).strip()

       def __unicode__(self):
               return self.get_width_string()
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
    null=True,
    validators=[validaColunas],
    )
  columns_large = models.IntegerField(
    _(u'Número de colunas (Telas grandes)'),
    blank=True,
    null=True,
    validators=[validaColunas],
    )
  def __unicode__(self):
    return u'Minicursos: (%d/%d/%d) colunas' % (self.columns_small, self.columns_medium, self.columns_large)