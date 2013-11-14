# coding: utf-8

from io import BytesIO
from unipath import Path
from PIL import Image

from django.db import models
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

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

def company_upload_to(instance, filename):
	# get image data and reset the fp position
	data = instance.logo.read()
	instance.logo.seek(0)

	filename = slugify(instance.name)
	bytes_io = BytesIO(data)

	image = Image.open(bytes_io)

	if image.format == 'JPEG':
		image_format = 'jpg'
	else:
		image_format = image.format.lower()

	return Path('empresas', '{0}.{1}'.format(filename, image_format))

class Company(models.Model):
	COMPANY_TYPE_CHOICES = (
		('P', _(u'Patrocínio')),
		('A', _(u'Apoio')),
	)

	name = models.CharField(
		_(u'Nome'),
		max_length=64
	)
	logo = models.ImageField(
		_(u'Logo'),
		upload_to=company_upload_to,
		blank=True
	)
	type = models.CharField(
		_(u'Tipo'),
		max_length=1,
		choices=COMPANY_TYPE_CHOICES
	)

class Place(models.Model):
	name = models.CharField(_(u'Nome'), max_length=32)
	latitude = models.DecimalField(max_digits=12, decimal_places=8)
	longitude = models.DecimalField(max_digits=12, decimal_places=8)
	zoom = models.IntegerField()

class Event(models.Model):
	name = models.CharField(_(u'Nome'), max_length=64)
	place = models.ForeignKey('Place')
	start_time = models.DateTimeField(_(u'Início'))
	end_time = models.DateTimeField(_(u'Fim'))
