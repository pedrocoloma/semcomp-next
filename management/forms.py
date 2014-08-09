# coding: utf-8

from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _

from django_select2.widgets import Select2Widget
from django_select2.fields import ModelSelect2Field, AutoModelSelect2Field

from website.models import (
	BusinessLecture,
	Company,
	ContactInformation,
	Course,
	Event,
	EventData,
	Inscricao,
	Lecture,
	Place,
	RecruitmentProcess,
	SemcompConfig,
	SemcompUser,
	Speaker
)
from semcomp_contact_form.models import Message

######### Fields

class SemcompUserSelect2Field(AutoModelSelect2Field):
	queryset = SemcompUser.objects
	search_fields = ['email__icontains', 'full_name__icontains']

######### Forms


class CompanyForm(forms.ModelForm):
	class Meta:
		model = Company
		fields = ['name', 'logo', 'url', 'type', 'description', 'in_fair']

class PlaceForm(forms.ModelForm):
	class Meta:
		model = Place
		fields = ('name', 'latitude', 'longitude', 'zoom')
		widgets = {
				'latitude': forms.HiddenInput(),
				'longitude': forms.HiddenInput(),
				'zoom': forms.HiddenInput(),
		}

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ('type', 'color', 'start_date', 'start_time', 'end_date', 'end_time')

class LectureForm(forms.ModelForm):
	class Meta:
		model = Lecture
		fields = ('slot', 'title', 'description', 'place')

class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = ('slots', 'title', 'photo','track', 'description', 'requirements', 'place')
		widgets = {
			# esse "style" é feio mas é menos feio do que não conseguir ver as opções
			'slots': forms.SelectMultiple(attrs={'style': 'height:100px'})
		}

class SpeakerForm(forms.ModelForm):
	class Meta:
		model = Speaker
		fields = ('name', 'occupation', 'photo', 'bio')

class SemcompConfigForm(forms.Form):
	def __init__(self, *args, **kwargs):
		form_fields = kwargs.pop('form_fields')

		super(SemcompConfigForm, self).__init__(*args, **kwargs)

		# usado de verdade só no save(), mas é declarado aqui pra que não
		# dê erro em alguém que tente acessar esse atributo antes da função
		# save() ser chamada
		self.new_config = []

		for field in form_fields:
			if field.type == 'text':
				field_name = 'config_text_field_{0}'.format(field.pk)
				self.fields[field_name] = forms.CharField(label=field.name)
			elif field.type == 'bool':
				field_name = 'config_bool_field_{0}'.format(field.pk)
				self.fields[field_name] = forms.BooleanField(label=field.name)
			elif field.type == 'datetime':
				field_name = 'config_datetime_field_{0}'.format(field.pk)
				self.fields[field_name] = forms.SplitDateTimeField(label=field.name)

			if field.pk:
				self.initial[field_name] = field.get_value()

	def save(self):
		for field_name in self.changed_data:
			field = self.fields[field_name]
			field_data = self.cleaned_data[field_name]

			config = SemcompConfig.objects.get(name=field.label)
			config.set_value(field_data)
			config.save()

			self.new_config.append(config)



ContactInformationFormset = inlineformset_factory(Speaker, ContactInformation)

EventDataFormset = inlineformset_factory(Event, EventData, max_num=1, can_delete=False)

class UserManagementForm(forms.ModelForm):
	class Meta:
		model = SemcompUser
		fields = {'email', 'full_name', 'id_usp', 'is_active', 'is_admin', 'is_staff'}
		help_texts = {
			'full_name': _(u'Nome completo, como aparecerá no certificado'),
			'id_usp': _(u'Deixe em branco para participantes de de fora da USP')
		}

class InscricaoManagementForm(forms.ModelForm):
	comentario = forms.CharField(
			label=_(u'Comentários'),
			widget=forms.Textarea,
			help_text=_(u'Caso o comprovante seja alterado ou rejeitado, você pode justificar ao usuário neste campo'),
			required=False,
		)
	class Meta:
		model = Inscricao
		fields = {'coffee', 'comprovante', 'CPF', 'numero_documento'}
	def __init__(self, *args, **kwargs):
		super(InscricaoManagementForm, self).__init__(*args, **kwargs)
		self.fields['comprovante'].required = False

class RecruitmentProcessForm(forms.ModelForm):
	class Meta:
		model = RecruitmentProcess
		widgets = {
			'start_datetime': forms.SplitDateTimeWidget,
			'end_datetime': forms.SplitDateTimeWidget
		}

class BusinessLectureForm(forms.ModelForm):
	class Meta:
		model = BusinessLecture
		widgets = {
			'start_datetime': forms.SplitDateTimeWidget,
			'end_datetime': forms.SplitDateTimeWidget
		}

class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ('html_body',)

class NewMessageForm(forms.Form):
	MESSAGE_TYPES = (
		('one', _(u'Individual')),
		('bulk', _(u'Para todos os inscritos')),
		('no_payment', _(u'Para todos os que não pagaram')),
		('pending', _(u'Para todos os pendentes')),
		('paid', _(u'Para todos com pagamento confirmado (participantes)')),
		('coffee', _(u'Para todos os participantes com coffee')),
		('no_coffee', _(u'Para todos os participantes sem coffee')),
	)

	type = forms.ChoiceField(
		choices=MESSAGE_TYPES,
		label=_(u'Tipo de mensagem'),
	)
	to_email = SemcompUserSelect2Field(
		label=_(u'Para'),
		required=False,
	)
	subject = forms.CharField(
		max_length=254,
		label=_(u'Assunto'),
	)
	body = forms.CharField(
		widget=forms.Textarea,
		label=_(u'Mensagem'),
	)
