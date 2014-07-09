# coding: utf-8

from datetime import datetime, time, timedelta, date

from django.db.models import Q
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from website.models import Event

from ..decorators import staff_required
from ..forms import EventForm, EventDataFormset

def time_range(start, end, step):
	while start < end:
		yield start
		dt = datetime.combine(date.today(), start) + step
		start = dt.time()

def date_range(start, end, step):
	while start <= end:
		yield start
		start = start + step

def should_use_extra_data(event):
	return event.type not in ['palestra', 'minicurso', 'coffee']

@staff_required
def manage_events(request):
	context = {
		'active_events': True,
	}

	return render(request, 'management/events.html', context)

@staff_required
def events_add(request):
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			event = form.save(commit=False)
			formset = EventDataFormset(request.POST, instance=event)
			if formset.is_valid():
				event.save()
				if should_use_extra_data(event):
					formset.save()
				else:
					event.eventdata_set.all().delete()
				return redirect('management_events')
	else:
		form = EventForm()
		formset = EventDataFormset(instance=Event())
	
	first_day = settings.SEMCOMP_START_DATE
	last_day = settings.SEMCOMP_END_DATE

	context = {
		'active_events': True,
		'form': form,
		'formset': formset,
		'first_day': first_day,
		'last_day': last_day
	}

	return render(request, 'management/events_change.html', context)

@staff_required
def events_edit(request, event_pk):
	event = get_object_or_404(Event, pk=event_pk)

	if request.method == 'POST':
		form = EventForm(request.POST, instance=event)
		if form.is_valid():
			formset = EventDataFormset(request.POST, instance=event)
			if formset.is_valid():
				event = form.save()
				if should_use_extra_data(event):
					formset.save()
				else:
					event.eventdata_set.all().delete()
			return redirect('management_events')
	else:
		form = EventForm(instance=event)
		formset = EventDataFormset(instance=event)

	first_day = settings.SEMCOMP_START_DATE
	last_day = settings.SEMCOMP_END_DATE

	context = {
		'active_events': True,
		'form': form,
		'formset': formset,
		'first_day': first_day,
		'last_day': last_day
	}

	return render(request, 'management/events_change.html', context)

@staff_required
def events_delete(request, event_pk):
	event = get_object_or_404(Event, pk=event_pk)

	event.delete()

	return redirect('management_events')
