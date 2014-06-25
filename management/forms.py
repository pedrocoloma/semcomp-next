# coding: utf-8

from django import forms
from django.forms.models import inlineformset_factory

from website.models import Place, Event, Lecture, Course, Speaker, ContactInformation


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
		fields = ('type', 'start_date', 'start_time', 'end_date', 'end_time')

class LectureForm(forms.ModelForm):
	class Meta:
		model = Lecture
		fields = ('slot', 'title', 'description', 'place')

class CourseForm(forms.ModelForm):
	class Meta:
		model = Course
		fields = ('slots', 'title', 'track', 'description', 'requirements', 'place', 'speaker')
		widgets = {
			# esse "style" é feio mas é menos feio do que não conseguir ver as opções
			'slots': forms.SelectMultiple(attrs={'style': 'height:100px'})
		}

class SpeakerForm(forms.ModelForm):
	class Meta:
		model = Speaker
		fields = ('name', 'occupation', 'photo', 'bio')

ContactInformationFormset = inlineformset_factory(Speaker, ContactInformation)
