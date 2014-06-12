from django.db import models

from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

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
