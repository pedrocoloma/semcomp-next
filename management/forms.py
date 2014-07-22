# coding: utf-8

from django import forms
from django.forms.models import inlineformset_factory
from django.utils.translation import ugettext_lazy as _
from website.models import Company, Place, Event, EventData, Lecture, Course, Speaker, ContactInformation, SemcompUser, Inscricao

class CompanyForm(forms.ModelForm):
	class Meta:
		model = Company
		fields = ['name', 'logo', 'url', 'type', 'description']

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

ContactInformationFormset = inlineformset_factory(Speaker, ContactInformation)

EventDataFormset = inlineformset_factory(Event, EventData, max_num=1, can_delete=False)

class UserManagementForm(forms.ModelForm):
	class Meta:
		model = SemcompUser
		fields = {'email', 'full_name', 'id_usp', 'is_active', 'is_admin', 'is_staff'}
class InscricaoManagementForm(forms.ModelForm):
	comentario = forms.CharField(
			label=_(u'Comentário'),
			widget=forms.Textarea,
		)
	def __init__(self, *args, **kwargs):
		super(InscricaoManagementForm, self).__init__(*args, **kwargs)
		self.fields['comprovante'].required = False
	class Meta:
		model = Inscricao
		fields = {'coffee', 'comprovante', 'numero_documento'}