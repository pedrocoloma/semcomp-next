from django import forms

from website.models import Place, Event, Lecture


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
		fields = ('slot', 'title', 'description', 'place', 'speaker')

