# coding: utf-8

from datetime import datetime
from PIL import Image
from io import BytesIO
from pathlib import Path

from django.core import validators
from django.core.urlresolvers import reverse
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy


def _base_upload_to_by_field(instance, image, base_path, field):
	# get image data and reset the fp position
	im = getattr(instance, image)
	data = im.read()
	im.seek(0)

	filename = slugify(getattr(instance, field))
	bytes_io = BytesIO(data)

	image = Image.open(bytes_io)

	if image.format == 'JPEG':
		image_format = 'jpg'
	else:
		image_format = image.format.lower()

	path = Path(base_path, '{0}.{1}'.format(filename, image_format))
	return path.as_posix()

def company_upload_to(instance, filename):
	return _base_upload_to_by_field(instance, 'logo', 'empresas', 'name')

def speaker_upload_to(instance, filename):
	return _base_upload_to_by_field(instance, 'photo', 'palestrantes', 'name')

def place_map_upload_to(instance, filename):
	name = slugify(instance.name)
	path = Path('mapas', '{0}.png'.format(name))
	return path.as_posix()

class Company(models.Model):
	COMPANY_TYPE_CHOICES = (
		('A', _(u'Adamantium')),
		('B', _(u'Diamante')),
		('C', _(u'Platina')),
		('D', _(u'Ouro')),
		('E', _(u'Prata')),
		('F', _(u'Feira')),
		('Z', _(u'Apoio')),
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
	description = models.TextField(_(u'Descrição'), blank=True)

	url = models.URLField()


class Place(models.Model):
	name = models.CharField(_(u'Nome'), max_length=32)
	latitude = models.DecimalField(max_digits=12, decimal_places=8)
	longitude = models.DecimalField(max_digits=12, decimal_places=8)
	zoom = models.IntegerField()
	static_map = models.ImageField(
		_(u'Mapa estático'),
		upload_to=place_map_upload_to
	)

	def __unicode__(self):
		return self.name

class EventManager(models.Manager):
	def unused(self, type, dont_remove=None):
		return Event.objects.filter(
			type=type
		).exclude(
			id__in=Lecture.objects.exclude(
				slot_id=None
			).exclude(
				slot_id=dont_remove
			).values_list(
				'slot_id', flat=True
			)
		)

class Event(models.Model):
	EVENT_TYPES = (
		('palestra', _(u'Palestra')),
		('minicurso', _(u'Minicurso')),
		('coffee', _(u'Coffee break')),
		('cultural', _(u'Cultural')),
		('neutro', _(u'Neutro')),
		('outro', _(u'Outro')),
	)

	type = models.CharField(_(u'Tipo'), max_length=16, choices=EVENT_TYPES)
	start_date = models.DateField(_(u'Dia inicial'))
	start_time = models.TimeField(_(u'Horário de início'))
	end_date = models.DateField(_(u'Dia final'))
	end_time = models.TimeField(_(u'Horário de término'))
	# 7 caracteres: #abc123
	color = models.CharField(_(u'Cor'), max_length=7, default='#85144B')

	objects = EventManager()

	def duration(self):
		start = datetime.combine(self.start_date, self.start_time)
		end = datetime.combine(self.end_date, self.end_time)

		return end - start

	def needs_event_data(self):
		return self.type not in ['palestra', 'minicurso', 'coffee']

	def needs_custom_page(self):
		return self.type not in ['coffee', 'neutro']
	
	def name(self):
		if self.type == 'palestra':
			return self.lecture.title
		elif self.type == 'minicurso':
			raise ValueError(u'Minicursos não tem um nome único')
		elif self.type == 'coffee':
			return self.get_type_display()
		else:
			return self.eventdata.name
	
	def description(self):
		if self.type == 'palestra':
			return self.lecture.description
		elif self.type == 'minicurso':
			raise ValueError(u'Minicursos não tem uma descrição única')
		elif self.type == 'coffee':
			return ''
		else:
			return self.eventdata.description

	def place(self):
		if self.type == 'palestra':
			return self.lecture.place
		elif self.type == 'minicurso':
			raise ValueError(u'Minicursos não tem um local único')
		elif self.type == 'coffee':
			return ''
		else:
			return self.eventdata.place

	def slug(self):
		if self.type == 'minicurso':
			return 'minicurso'
		else:
			return slugify(self.name())

	def get_absolute_url(self):
		if self.type == 'palestra':
			return self.lecture.get_absolute_url()
		elif self.type == 'minicurso':
			return reverse('event_details', args=[str(self.id)])
		elif self.type == 'coffee':
			raise ValueError(u'Coffee-breaks não tem URL própria')
		else:
			return reverse(
				'event_details_slug',
				args=[str(self.id), self.slug()]
			)

	def __unicode__(self):
		start_time = self.start_time.strftime('%H:%M')
		end_time = self.end_time.strftime('%H:%M')
		date = self.start_date.strftime('%d/%m')

		if self.start_date == self.end_date:
			return '%s %s-%s' % (date, start_time, end_time)
		else:
			end_date = self.end_date.strftime('%d/%m')
			return '%s@%s - %s@%s' % (date, start_time, end_date, end_time)

class EventData(models.Model):
	slot = models.OneToOneField(Event)
	name = models.CharField(_(u'Nome'), max_length=64, blank=True)
	description = models.TextField(_(u'Descrição'), blank=True)
	place = models.ForeignKey(
		'Place',
		blank=True,
		null=True,
		verbose_name=_(u'Local'),
		on_delete=models.SET_NULL
	)


class Speaker(models.Model):
	name = models.CharField(_(u'Nome'), max_length=100)
	occupation = models.CharField(_(u'Ocupação'), max_length=255, blank=True)
	photo = models.ImageField(_(u'Foto'), upload_to=speaker_upload_to, blank=True)
	bio = models.TextField(_(u'Biografia'), blank=True)

	def __unicode__(self):
		return self.name

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
	slot = models.OneToOneField(Event, null=True, blank=True)
	title = models.CharField(_(u'Título'), max_length=100)
	description = models.TextField(_(u'Descrição'), blank=True)
	place = models.ForeignKey(
		'Place',
		blank=True,
		null=True,
		verbose_name=_(u'Local'),
		on_delete=models.SET_NULL,
	)
	speaker = models.ForeignKey(Speaker, blank=True, null=True, verbose_name=_(u'Palestrante'))

	def get_absolute_url(self):
		return reverse(
			'event_details_slug',
			args=[str(self.slot.id), self.slot.slug()]
		)

class Course(models.Model):
	TRACK_TYPES = (
		('A', _(u'Amarelo')),
		('V', _(u'Verde')),
	)
	# Um minicurso pode estar alocado pra mais de um slot. Por exemplo, se um
	# minicurso ocupa toda a manhã, tem um coffee break no meio, e ele está
	# ocupando dois slots de minicurso, o antes do coffee e depois do coffee
	slots = models.ManyToManyField(Event)
	title = models.CharField(_(u'Título'), max_length=100)
	track = models.CharField(_(u'Pacote'), max_length=1, choices=TRACK_TYPES)
	description = models.TextField(_(u'Descrição'), blank=True)
	requirements = models.TextField(_(u'Pré-requisitos'), blank=True)
	place = models.ForeignKey(
		'Place',
		blank=True,
		null=True,
		verbose_name=_(u'Local'),
		on_delete=models.SET_NULL,
	)
	speaker = models.ForeignKey(Speaker, blank=True, null=True, verbose_name=_(u'Palestrante'))

	def get_absolute_url(self):
		return reverse(
			'course_details_slug',
			args=[str(self.id), slugify(self.title)]
		)


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


