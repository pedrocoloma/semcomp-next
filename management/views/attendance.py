# coding: utf-8

import re

from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404

from website.models import Event

from ..decorators import staff_required
from ..models import Attendance
from ..utils import render_json_response


@staff_required
def manage_attendance(request):
	events = Event.objects.exclude(
		type='minicurso'
	).filter(
		used_for_attendance=True
	)

	context = {
		'active_attendance': True,
		'events': events
	}
	return render(request, 'management/attendance.html', context)


@staff_required
def attendance_submit(request, event_pk):
	event = get_object_or_404(Event, pk=event_pk)
	if event.type == 'minicurso' or not event.used_for_attendance:
		raise Http404

	if request.method == 'POST':
		if request.is_ajax():
			badge_list = request.POST.getlist('badge-list[]')

			attendance_list = []
			regex = re.compile(r'^[0-9]+$')
			for badge in badge_list:
				if not badge:
					continue
				if not regex.match(badge):
					# aqui eu deveria passar alguma info de volta pro
					# javascript pra saber que esse cara aqui foi recusado. do
					# jeito que tá, vai sobrar uma chave no storage do cliente
					# que vai ser enviado toda vez (e o spinner nunca vai parar
					# de rodar)
					continue
				att, created = Attendance.objects.get_or_create_from_badge(
					event, badge
				)
				attendance_list.append((att, created))

			json_data = []
			for att,created in attendance_list:
				user = att.user
				if user.full_name:
					key = user.id
					value = user.full_name
					new_user = False
				else:
					key = user.id_usp
					value = user.id_usp
					new_user = True
				json_data.append({
					'key': unicode(key),
					'value': unicode(value),
					'created': created,
					'new_user': new_user
				})

			return render_json_response(json_data)
		else:
			badge = request.POST.get('badge-number', None)
			Attendance.objects.create_from_badge(event, badge)
			return redirect('management_attendance_submit', args=[event.pk])

	context = {
		'active_attendance': True,
		'event': event,
	}

	return render(request, 'management/attendance_submit.html', context)
