# coding: utf-8

from datetime import datetime
from io import BytesIO
import hashlib
import re

from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core import validators
from django.core.urlresolvers import reverse
from django.core.validators import EMPTY_VALUES
from django.core.validators import ValidationError
from django.db import models
from django.db.models import Max, Min
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.utils.translation import ungettext_lazy

from PIL import Image
from pathlib import Path
from south.modelsinspector import add_introspection_rules

from account.models import CourseRegistration


def _base_upload_to_by_field(instance, image, base_path, field):
	# get image data and reset the fp position
	im = getattr(instance, image)
	data = im.read()
	im.seek(0)

	filename = slugify(field)
	bytes_io = BytesIO(data)

	image = Image.open(bytes_io)

	if image.format == 'JPEG':
		image_format = 'jpg'
	else:
		image_format = image.format.lower()

	path = Path(base_path, '{0}.{1}'.format(filename, image_format))
	return path.as_posix()

def company_upload_to(instance, filename):
	return _base_upload_to_by_field(instance, 'logo', 'empresas', instance.name)

def speaker_upload_to(instance, filename):
	return _base_upload_to_by_field(instance, 'photo', 'palestrantes', instance.name)

def place_map_upload_to(instance, filename):
	name = slugify(instance.name)
	path = Path('mapas', '{0}.png'.format(name))
	return path.as_posix()

def course_upload_to(instance, filename):
	return _base_upload_to_by_field(instance, 'photo', 'minicursos', instance.title)

def comprovantes_upload_to(instance, filename):
	return _base_upload_to_by_field(instance, 'comprovante', 'comprovantes', unicode(hashlib.sha224(instance.user.email).hexdigest()[:10]))

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

	in_fair = models.BooleanField(
		_(u'Vai participar da feira?'),
		default=False
	)

	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return reverse(
			'company_details_slug',
			args=[str(self.id), slugify(self.name)]
		)


class Place(models.Model):
	name = models.CharField(_(u'Nome'), max_length=100)
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
	used_for_attendance = models.BooleanField(
		_(u'Conta presença'),
		default=False,
		help_text=_(u'Não tem efeito em minicursos')
	)

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

	def attendance(self):
		return self.attendance_set.count()

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
	photo = models.ImageField(_(u'Foto'), upload_to=course_upload_to)
	vacancies = models.PositiveIntegerField(_(u'Vagas'), default=0)


	def get_absolute_url(self):
		return reverse(
			'course_details_slug',
			args=[str(self.id), slugify(self.title)]
		)
	def get_remaining_vacancies(self):
		return self.vacancies - CourseRegistration.objects.filter(course=self).count()
	def get_number_of_subscribers(self):
		return CourseRegistration.objects.filter(course=self).count()
	def get_registered_users(self):
		return SemcompUser.objects.filter(courseregistration__course=self)
	def annotate_times(self):
		course_date_time = self.slots.aggregate(
			Min('start_time'), Max('end_time'),
			Min('start_date'), Max('end_date')
		)
		# annotate manually
		self.start_time = course_date_time['start_time__min']
		self.end_time = course_date_time['end_time__max']
		self.start_date = course_date_time['start_date__min']
		self.end_date = course_date_time['end_date__max']
	def __unicode__(self):
		return self.title

	def slug(self, words=-1):
		title = re.split(' |,', self.title)
		return slugify(u' '.join(title[:words]))


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

	def registered(self):
		return self.filter(is_active=True, is_staff=False)

	def paid(self):
		return self.filter(is_active=True, is_staff=False, inscricao__pagamento=True)

	def pending(self):
		return self.filter(is_active=True, is_staff=False, inscricao__pagamento=False, inscricao__avaliado=False).exclude(inscricao__comprovante__exact='')

	def no_payment(self):
		return self.filter(is_active=True, is_staff=False).exclude(inscricao__pagamento=True).exclude(pk__in=self.pending().values('pk'))

	def coffee(self):
		return self.filter(is_active=True, is_staff=False, inscricao__pagamento=True, inscricao__coffee=True)

	def no_coffee(self):
		return self.filter(is_active=True, is_staff=False, inscricao__pagamento=True, inscricao__coffee=False)

	def in_course(self, course):
		return self.filter(courseregistration__course=course)

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
			validators.RegexValidator(r'^\d+$',_(u'Entre com um número USP válido')),
		],
	)

	# campos django-admin
	is_active = models.BooleanField(u'Ativo', default=True)
	is_admin = models.BooleanField(u'Administrador', default=False)
	is_staff = models.BooleanField(u'Organização', default=False)

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
		if self.full_name:
			return self.full_name
		else:
			return self.id_usp

	def inscricao(self):
		return Inscricao.objects.get(user=self)

	@property
	def badge(self):
		if self.id_usp:
			return self.id_usp
		else:
			# colocando o "1000.." _porque sim_. ver motivo em
			# management/models.py
			return u'1' + unicode(self.id).zfill(6)


class NullableCharField(models.CharField):
    description = ""
    __metaclass__ = models.SubfieldBase
    def to_python(self, value):
        if isinstance(value, models.CharField):
            return value
        return value or ''
    def get_prep_value(self, value):
        return value or None

def DV_maker(v):
	if v >= 2:
		return 11 - v
	return 0
def validate_CPF(value):
	"""
	Value can be either a string in the format XXX.XXX.XXX-XX or an
	11-digit number.
	"""
	if value in EMPTY_VALUES:
		return u''
	if not value.isdigit():
		value = re.sub("[-\.]", "", value)
	orig_value = value[:]
	try:
		int(value)
	except ValueError:
		raise ValidationError(_(u'CPF Inválido'))
	if len(value) != 11:
		raise ValidationError(_(u'CPF Inválido'))
	orig_dv = value[-2:]

	new_1dv = sum([i * int(value[idx]) for idx, i in enumerate(range(10, 1, -1))])
	new_1dv = DV_maker(new_1dv % 11)
	value = value[:-2] + str(new_1dv) + value[-1]
	new_2dv = sum([i * int(value[idx]) for idx, i in enumerate(range(11, 1, -1))])
	new_2dv = DV_maker(new_2dv % 11)
	value = value[:-1] + str(new_2dv)
	if value[-2:] != orig_dv:
		raise ValidationError(_(u'CPF Inválido'))

	return orig_value

class Inscricao(models.Model):

	user = models.ForeignKey(SemcompUser,
		primary_key=True
		)
	pagamento = models.BooleanField(default=False)
	coffee = models.BooleanField(u'Coffee Break',
		default=False)
	comprovante = models.ImageField(
		_(u'Comprovante de Pagamento'),
		upload_to=comprovantes_upload_to,
		blank=False,
		null=True,
		)
	numero_documento = NullableCharField(
			_(u'Número do Documento'),
			help_text=_(u'Anote aqui algum número que identifique o comprovante, garantindo que este só seja cadastrado uma única vez'),
			max_length='30',
			null=True,
			blank=True,
			unique=True,
		)
	avaliado = models.BooleanField(default=False)
	CPF = models.CharField(
		_(u'CPF'),
		help_text=_(u'Seu CPF (Somente números!)'),
		max_length='11',
		blank=False,
		validators=[
			validate_CPF
		],)
	def status_pagamento(self):
		if self.pagamento:
			return _(u'OK')
		elif self.comprovante and not self.avaliado:
			return _(u'Pendente')
		else:
			return _(u'Não')
	def unique_error_message(self, model_class, unique_check):
		qs = Inscricao.objects.filter(numero_documento=self.numero_documento).exclude(user=self.user)

		if qs.exists():
			user = qs[0].user
			return _(u'Número de documento já utilizado por: %s ( %s )'
					% (user.full_name, user.email)
				 )
		return super(Inscricao, self).unique_error_message(self, model_class, unique_check)
add_introspection_rules([], ["^website\.models\.NullableCharField"])


class SemcompConfig(models.Model):
	TYPE_CHOICES = (
		('text', _(u'Texto')),
		('datetime', _(u'Data/Hora')),
		('bool', _(u'Booleano')),
	)

	messages = {
		'title_regex': _(u'Só são válidos nomes usando [A-Z_]'),
	}

	name = models.CharField(
		_(u'Nome'),
		max_length=100,
		unique=True,
		help_text=_(u'Nome amigável pro campo'),
		validators=[
			validators.RegexValidator(
				r'^[A-Z_]+$', messages['title_regex'])
		]
	)
	title = models.CharField(
		_(u'Título'),
		max_length=100,
		help_text=messages['title_regex'],
		unique=True,
	)
	type = models.CharField(
		_(u'Tipo'),
		max_length=8,
		choices=TYPE_CHOICES
	)
	value_text = models.TextField(default='')
	value_datetime = models.DateTimeField(auto_now_add=True)
	value_bool = models.BooleanField(default=False)

	def get_value(self):
		return getattr(self, 'value_' + self.type)

	def set_value(self, value):
		setattr(self, 'value_' + self.type, value)

class RecruitmentProcess(models.Model):
	start_datetime = models.DateTimeField(_(u'Horário de início'))
	end_datetime = models.DateTimeField(_(u'Horário de término'))
	place = models.ForeignKey(
		Place,
		blank=True,
		null=True,
		on_delete=models.SET_NULL,
		verbose_name = _(u'Local'),
	)
	company = models.OneToOneField(
		Company,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		verbose_name=_(u'Empresa'),
		related_name='recruitment_process',
	)

class BusinessLecture(models.Model):
	start_datetime = models.DateTimeField(_(u'Horário de início'))
	end_datetime = models.DateTimeField(_(u'Horário de término'))
	place = models.ForeignKey(
		Place,
		blank=True,
		null=True,
		on_delete=models.SET_NULL,
		verbose_name=_(u'Local'),
	)
	company = models.OneToOneField(
		Company,
		null=True,
		blank=True,
		on_delete=models.SET_NULL,
		verbose_name=_(u'Empresa'),
		related_name='business_lecture'
	)
