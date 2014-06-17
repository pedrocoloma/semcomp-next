# coding: utf-8

from datetime import datetime
from PIL import Image
from io import BytesIO
from pathlib import Path

from django.core import validators
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy



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

	path = Path('empresas', '{0}.{1}'.format(filename, image_format))
	return path.as_posix()

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
	url = models.URLField()

class Place(models.Model):
	name = models.CharField(_(u'Nome'), max_length=32)
	latitude = models.DecimalField(max_digits=12, decimal_places=8)
	longitude = models.DecimalField(max_digits=12, decimal_places=8)
	zoom = models.IntegerField()

	def __unicode__(self):
		return self.name

class Event(models.Model):
	EVENT_TYPES = (
		('palestra', _(u'Palestra')),
		('minicurso', _(u'Minicurso')),
		('coffee', _(u'Coffee break')),
		('cultural', _(u'Cultural')),
		('neutro', _(u'Neutro')),
	)

	type = models.CharField(_(u'Tipo'), max_length=16, choices=EVENT_TYPES)
	start_date = models.DateField(_(u'Dia inicial'))
	start_time = models.TimeField(_(u'Horário de início'))
	end_date = models.DateField(_(u'Dia final'))
	end_time = models.TimeField(_(u'Horário de término'))

	def duration(self):
		start = datetime.combine(self.start_date, self.start_time)
		end = datetime.combine(self.end_date, self.end_time)

		return end - start

class EventData(models.Model):
	slot = models.ForeignKey(Event)
	name = models.CharField(_(u'Nome'), max_length=64, blank=True)
	description = models.TextField(_(u'Descrição'), blank=True)
	place = models.ForeignKey('Place', blank=True, null=True, verbose_name=_(u'Local'))


class Speaker(models.Model):
	name = models.CharField(max_length=100)
	occupation = models.CharField(max_length=255)
	bio = models.TextField(_(u'Biografia'))

class ContactInformation(models.Model):
	CONTACT_TYPES = (
		('W', _(u'Website')),
		('T', _(u'Twitter')),
		('F', _(u'Facebook')),
		('E', _(u'Email')),
		('L', _(u'Linkedin')),
	)

	speaker = models.ForeignKey(Speaker)
	type = models.CharField(max_length=1, choices=CONTACT_TYPES)
	value = models.CharField(max_length=100)


class Lecture(models.Model):
	slot = models.ForeignKey(Event)
	title = models.CharField(_(u'Título'), max_length=100)
	description = models.TextField(_(u'Descrição'), blank=True)
	place = models.ForeignKey('Place', blank=True, null=True, verbose_name=_(u'Local'))
	speaker = models.ForeignKey(Speaker, blank=True, null=True, verbose_name=_(u'Palestrante'))


class Course(models.Model):
	# Um minicurso pode estar alocado pra mais de um slot. Por exemplo, se um
	# minicurso ocupa toda a manhã, tem um coffee break no meio, e ele está
	# ocupando dois slots de minicurso, o antes do coffee e depois do coffee
	slots = models.ManyToManyField(Event)
	title = models.CharField(_(u'Título'), max_length=100)
	description = models.TextField(_(u'Descrição'), blank=True)
	requirements = models.TextField(_(u'Pré-requisitos'), blank=True)
	place = models.ForeignKey('Place', blank=True, null=True, verbose_name=_(u'Local'))
	speaker = models.ForeignKey(Speaker, blank=True, null=True, verbose_name=_(u'Palestrante'))


class SemcompUserManager(BaseUserManager):
	def create_user(self, email, full_name, id_usp='', password=None):
		if not email:
			msg = _(u'Entre com um endereço de email')
			raise ValueError(msg)

		if not full_name:
			msg = _(u'Entre com o nome completo do usuário')
			raise ValueError(msg)


		user = self.model(
			email=SemcompUserManager.normalize_email(email),
			full_name=full_name,
			first_name=full_name.split(None, 1)[:1],
			last_name=full_name.split(None, 1)[1:],
			id_usp=id_usp,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, full_name, id_usp='', password=None):
		user = self.create_user(email, full_name, id_usp, password)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user


class SemcompUser(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(
		_(u'Email'),
		max_length=254,
		unique=True,
		db_index=True
	)

	full_name = models.CharField(
		_(u'Nome completo'),
		help_text=_(u'Seu nome completo, da forma que quer no certificado'),
		max_length=255
	)
	# campos que o django-cms exige
	first_name = models.CharField(max_length=64, blank=True)
	last_name= models.CharField(max_length=64, blank=True)

	id_usp = models.CharField(
		_(u'Número USP'),
		help_text=_(u'Se você não for da USP, deixe em branco'),
		max_length=8,
		blank=True,
		validators=[
			validators.RegexValidator(
				r'\d+', _(u'Entre com um número USP válido')),
		],
	)

	# campos django-admin
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	# pra ver depois quando que cada um se inscreveu
	date_joined = models.DateTimeField(default=timezone.now)

	objects = SemcompUserManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['full_name']

	class Meta:
		verbose_name = _(u'usuário')

	def get_full_name(self):
		return self.full_name

	def get_short_name(self):
		return self.email

	def __unicode__(self):
		return self.full_name


