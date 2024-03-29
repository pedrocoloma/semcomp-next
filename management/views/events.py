# coding: utf-8

from datetime import datetime, time, timedelta, date

from django.db.models import Q
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

import stats
from website.models import Event

from ..decorators import staff_required
from ..forms import EventForm, EventDataFormset

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
				if event.needs_event_data():
					formset.save()
				elif hasattr(event, 'eventdata'):
					event.eventdata.delete()

				stats.add_event(
					'management-events',
					{
						'action': 'add',
						'event': {
							'id': event.id,
							'type': event.type,
						},
						'user': {
							'id': request.user.id,
							'name': request.user.full_name,
						},
					}
				)

				return redirect('management_events')
		else:
			formset = EventDataFormset(request.POST)
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
		formset = EventDataFormset(request.POST, instance=event)
		if form.is_valid():
			if formset.is_valid():
				event = form.save()
				if event.needs_event_data():
					formset.save()
				elif hasattr(event, 'eventdata'):
					event.eventdata.delete()

				stats.add_event(
					'management-events',
					{
						'action': 'change',
						'event': {
							'id': event.id,
							'type': event.type,
							'changed_fields': form.changed_data + map(lambda x: x.changed_data, formset)
						},
						'user': {
							'id': request.user.id,
							'name': request.user.full_name,
						},
					}
				)

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

	stats.add_event(
		'management-events',
		{
			'action': 'delete',
			'user': {
				'id': request.user.id,
				'name': request.user.full_name,
			},
			'event': {
				'id': event.id,
				'type': event.type,
			},
		}
	)

	event.delete()

	return redirect('management_events')
