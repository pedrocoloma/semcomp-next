# coding: utf-8

import re
try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

from django.db.models import Count
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.utils.translation import ugettext as _

import xlsxwriter
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import ParagraphStyle, _baseFontNameB

from website.models import Event, SemcompUser
import stats

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

			attendance_data = []
			for att in json_data:
				if created:
					attendance_data.append({
						'badge': key,
						'user': unicode(value),
					})
			stats.add_event(
				'management-attendance',
				{
					'action': 'submit',
					'user': {
						'id': request.user.id,
						'name': request.user.full_name,
					},
					'attendances': attendance_data
				}
			)

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
def attendance_report(request, event_pk=None, report_type='pdf'):
	if report_type not in ['pdf', 'xls']:
		raise Http404

	if event_pk:
		event = get_object_or_404(Event, pk=event_pk)
		if event.type == 'minicurso' or not event.used_for_attendance:
			raise Http404
	else:
		event = None

	output = StringIO()
	headers, data = get_attendance_data(event)
	report = globals()['write_report_' + report_type](output, headers, data)

	content_types = {
		'pdf': 'application/pdf',
		'xls': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
	}

	if event:
		name = event.name()
		words = re.split(' |,', name)
		# três primeiras palavras, por mais bizarro que
		# possa ficar o nome do arquivo
		content_filename = u'relatorio-{}.'.format(
			slugify(u' '.join(words[:3]))
		)
	else:
		content_filename = _(u'relatorio-presenca-semcomp-17.')
	content_filename += u'xlsx' if report_type == 'xls' else u'pdf'
	content_disposition = u'attachment; filename={}'.format(content_filename)

	response = HttpResponse(
		output.getvalue(),
		content_type=content_types[report_type],
	)
	response['Content-Disposition'] = content_disposition

	return response


def get_attendance_data(event=None):
	if not event:
		total_events = Event.objects.exclude(
			type='minicurso'
		).filter(
			used_for_attendance=True
		).count()
	# Isso aqui assume que os dados que foram inseridos na base de dados são
	# todos corretos, i.e., nenhum usuário recebeu presença em um evento que na
	# verdade não deveria receber presença pelo site (como um minicurso)
	if event:
		users = SemcompUser.objects.registered().filter(
			attendance__event=event
		)
	else:
		users = SemcompUser.objects.registered().annotate(Count('attendance'))

	header_fields = [
		_(u'Nome'), _(u'Número USP'), _(u'ID Semcomp'),
		_(u'Crachá')
	]
	if not event:
		header_fields.append(_(u'Presença'))

	fields = ['full_name', 'id_usp', 'id', 'badge']

	data = []
	for user in users:
		user_data = [getattr(user, field) for field in fields]

		if not event:
			if total_events == 0:
				att = u'N/A'
			else:
				att = 100.0 * user.attendance__count / float(total_events)
				att = u'{}%'.format(int(att))
			att_string = u'{} ({}/{})'.format(
				att, user.attendance__count, total_events
			)

			user_data.append(att_string)

		data.append(user_data)

	return header_fields, data


def write_report_xls(output, headers, data):
	workbook = xlsxwriter.Workbook(output)

	bold = workbook.add_format({'bold': True})

	sheet = workbook.add_worksheet(_(u'Presenças Semcomp 17'))

	# escreve cabeçalho
	for index,field in enumerate(headers):
		sheet.write(0, index, field, bold)

	# largura mínima de 20 unidades
	column_widths = [20] * len(headers)
	for i,user_data in enumerate(data):
		for j,field in enumerate(user_data):
			field_length = len(unicode(field))
			if field_length > column_widths[j]:
				column_widths[j] = field_length
			sheet.write(i + 1, j, field)

	for i,width in enumerate(column_widths):
		sheet.set_column(i, i, width)

	workbook.close()


def write_report_pdf(output, headers, data):
	doc = SimpleDocTemplate(output, pagesize=A4)

	t = Table([headers] + data, repeatRows=1)
	t.setStyle(
		TableStyle([
			('FONTNAME', (0, 0), (-1, 0), _baseFontNameB),
			('GRID', (0, 0), (-1, -1), 0.5, (0, 0, 0)),
		])
	)
	doc.build([t])
