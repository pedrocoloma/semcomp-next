# coding: utf-8

from datetime import datetime, time, timedelta, date

from django.db.models import Q
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings

from website.models import Event

from ..decorators import staff_required
from ..forms import EventForm

def time_range(start, end, step):
	while start < end:
		yield start
		dt = datetime.combine(date.today(), start) + step
		start = dt.time()

def date_range(start, end, step):
	while start <= end:
		yield start
		start = start + step

@staff_required
def manage_events(request):
	first_day = settings.SEMCOMP_START_DATE
	last_day = settings.SEMCOMP_END_DATE
	day_count = (last_day - first_day).days

	events = Event.objects.filter(
		start_date__gte=first_day,
		start_date__lte=last_day,
		in_schedule=True,
	)

	time_start = time(8, 0)
	time_end = time(23, 0)
	time_delta = timedelta(minutes=30)
	one_day = timedelta(days=1)

	events_off_semcomp = Event.objects.filter(
		Q(start_date__lte=first_day) | Q(start_date__gte=last_day)
	)

	days = []
	for day in date_range(first_day, last_day, one_day):
		day_events = events.filter(start_date=day)
		day_start = datetime.combine(day, time_start)

		day_data = []
		for e in day_events:
			event_start = datetime.combine(e.start_date, e.start_time)
			dt = event_start - day_start

			day_data.append({
				'name': e.name,
				'type': e.type,
				'obj': e,
				'slots': e.duration().seconds / time_delta.seconds,
				'start_slot': dt.seconds / time_delta.seconds,
			})

		days.append(day_data)

	timeslots = time_range(time_start, time_end, time_delta)

	context = {
		'active_events': True,
		'days': days,
		'timeslots': timeslots
	}

	return render(request, 'management/events.html', context)

@staff_required
def events_add(request):
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('management_events')
	else:
		form = EventForm()
	
	first_day = settings.SEMCOMP_START_DATE
	last_day = settings.SEMCOMP_END_DATE

	context = {
		'active_events': True,
		'form': form,
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
			form.save()
			return redirect('management_events')
	else:
		form = EventForm(instance=event)

	first_day = settings.SEMCOMP_START_DATE
	last_day = settings.SEMCOMP_END_DATE

	context = {
		'active_events': True,
		'form': form,
		'first_day': first_day,
		'last_day': last_day
	}

	return render(request, 'management/events_change.html', context)

@staff_required
def events_delete(request, event_pk):
	event = get_object_or_404(Event, pk=event_pk)

	event.delete()

	return redirect('management_events')
