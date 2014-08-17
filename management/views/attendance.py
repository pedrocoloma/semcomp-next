# coding: utf-8

import re
try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.translation import ugettext as _

import xlsxwriter

from website.models import Event, SemcompUser

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
				# guarda qual foi o número de crachá que usou pra dar presença
				attendance_list.append((att, badge, created))

			json_data = []
			for att,key,created in attendance_list:
				user = att.user
				if user.full_name:
					value = user.full_name
					new_user = False
				else:
					value = user.id_usp
					new_user = True
				json_data.append({
					'key': key,
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


@staff_required
def attendance_report(request, report_type):
	if report_type not in ['pdf', 'xls']:
		raise Http404

	output = StringIO()
	report = globals()['write_report_' + report_type](output)

	content_types = {
		'pdf': 'application/pdf',
		'xls': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
	}
	content_filename = _(u'relatorio-presenca-semcomp-17.')
	content_filename += u'xlsx' if report_type == 'xls' else u'pdf'
	content_disposition = u'attachment; filename={}'.format(content_filename)

	response = HttpResponse(
		output.read(),
		content_type=content_types[report_type],
	)
	response['Content-Disposition'] = content_disposition

	return response


def get_attendance_data():
	total_events = Event.objects.exclude(
		type='minicurso'
	).filter(
		used_for_attendance=True
	).count()
	# Isso aqui assume que os dados que foram inseridos na base de dados são
	# todos corretos, i.e., nenhum usuário recebeu presença em um evento que na
	# verdade não deveria receber presença pelo site (como um minicurso)
	users = SemcompUser.objects.registered().annotate(Count('attendance'))

	return total_events, users


def write_report_xls(output):
	workbook = xlsxwriter.Workbook(output)

	bold = workbook.add_format({'bold': True})

	sheet = workbook.add_worksheet(_(u'Presenças Semcomp 17'))

	total_events, attendance_data = get_attendance_data()

	# escreve cabeçalho
	header_fields = [
		_(u'Nome'), _(u'Número USP'), _(u'ID Semcomp'),
		_(u'Crachá'), _(u'Presença')
	]
	for index,header in enumerate(header_fields):
		sheet.write(0, index, header, bold)

	# escreve dados presença
	fields = ['full_name', 'id_usp', 'id', 'badge']
	# largura mínima de 20 unidades, o "+1" é pra coluna de presença
	column_widths = [20] * (len(fields) + 1)
	for i,user in enumerate(attendance_data):
		for j,field in enumerate(fields):
			data = getattr(user, field)
			data_length = len(unicode(data))
			if data_length > column_widths[j]:
				column_widths[j] = data_length
			sheet.write(i + 1, j, data)

		attendance = 100.0 * user.attendance__count / float(total_events)
		att_string = '{}% ({}/{})'.format(
			int(attendance), user.attendance__count, total_events
		)
		sheet.write(i + 1, len(fields), att_string)

	for i,width in enumerate(column_widths):
		sheet.set_column(i, i, width)

	workbook.close()

	output.seek(0)


def write_report_pdf():
	print 'report pdf'

