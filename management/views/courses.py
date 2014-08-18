# coding: utf-8

try:
	from cStringIO import StringIO
except ImportError:
	from StringIO import StringIO

from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.template.defaultfilters import date, time
from django.utils.translation import ugettext as _

from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import (
	ParagraphStyle,
	_baseFontNameB,
	getSampleStyleSheet
)
from reportlab.lib.units import mm, inch
from reportlab.platypus import (
	PageBreak,
	Paragraph,
	SimpleDocTemplate,
	Table,
	TableStyle,
)

from account.models import CourseRegistration
from website.models import Event, Course, Speaker, SemcompUser
import stats

from ..decorators import staff_required
from ..forms import (
	CourseForm,
	CourseMembersAddForm,
	CourseExpelForm,
	SpeakerForm,
	ContactInformationFormset
)


@staff_required
def manage_courses(request):
	courses = Course.objects.all()
	return render(
		request,
		'management/courses.html',
		{
			'active_courses': True,
			'courses': courses
		}
	)

@staff_required
def courses_add(request):
	if request.method == 'POST':
		course_form = CourseForm(request.POST, request.FILES, prefix='course')
		speaker_form = SpeakerForm(request.POST, request.FILES, prefix='speaker')
		contact_formset = ContactInformationFormset(request.POST, prefix='contact')

		if course_form.is_valid():
			course = course_form.save(commit=False)
			if speaker_form.has_changed():
				if speaker_form.is_valid() and contact_formset.is_valid():
					contact = contact_formset.save(commit=False)
					speaker = speaker_form.save()

					course.speaker = speaker

					for c in contact:
						c.speaker = speaker
						c.save()

					course.save()
					course_form.save_m2m()

					return redirect('management_courses')
			else:
					course.save()
					course_form.save_m2m()

					return redirect('management_courses')
	else:
		speaker_form = SpeakerForm(prefix='speaker')
		course_form = CourseForm(prefix='course')
		contact_formset = ContactInformationFormset(instance=Speaker(), prefix='contact')
		course_form.fields['slots'].queryset = Event.objects.filter(type='minicurso')

	return render(
		request,
		'management/courses_change.html',
		{
			'course_form': course_form,
			'speaker_form': speaker_form,
			'contact_formset': contact_formset,
			'active_courses': True,
		}
	)

@staff_required
def courses_edit(request, course_pk):
	course = get_object_or_404(Course, pk=course_pk)
	speaker = course.speaker
	contact = speaker.contactinformation_set if speaker else None

	if request.method == 'POST':
		course_form = CourseForm(request.POST, request.FILES, instance=course, prefix='course')
		speaker_form = SpeakerForm(request.POST, request.FILES, instance=speaker, prefix='speaker')
		contact_formset = ContactInformationFormset(request.POST, instance=speaker, prefix='contact')

		if course_form.is_valid():
			course = course_form.save(commit=False)
			if speaker_form.has_changed():
				if speaker_form.is_valid() and contact_formset.is_valid():
					contact = contact_formset.save(commit=False)
					speaker = speaker_form.save()

					course.speaker = speaker

					for c in contact:
						c.speaker = speaker
						c.save()

					course.save()
					course_form.save_m2m()

					return redirect('management_courses')
			else:
				course.speaker = speaker
				course.save()
				course_form.save_m2m()

				return redirect('management_courses')
	else:
		course_form = CourseForm(instance=course, prefix='course')
		speaker_form = SpeakerForm(instance=speaker, prefix='speaker')
		contact_formset = ContactInformationFormset(instance=speaker, prefix='contact')
		course_form.fields['slots'].queryset = Event.objects.filter(type='minicurso')

	context = {
		'course_form': course_form,
		'speaker_form': speaker_form,
		'contact_formset': contact_formset,
		'active_courses': True,
	}
	return render(request,'management/courses_change.html', context)

@staff_required
def courses_members(request, course_pk):
	course = get_object_or_404(Course, pk=course_pk)
	form = CourseMembersAddForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			try:
				reg = CourseRegistration(course=course, user=form.cleaned_data['member'])
				reg.save()
				messages.success(request, u'O usuário foi adicionado com sucesso')
				stats.add_event(
					'course-management',
					{
						'action': 'add-member',
						'user': {
							'id': request.user.pk,
							'name': request.user.full_name,
						},
						'registration' :{
							'member': {
								'id': form.cleaned_data['member'].pk,
								'name': form.cleaned_data['member'].full_name,
							},
							'course': {
								'id': course.pk,
								'title': course.title,
								'vacancies': course.get_remaining_vacancies()
							},
						},
					}
				)
				return redirect('management_courses_members', course.pk)
			except (CourseRegistration.PagamentoNaoRealizado,
				CourseRegistration.ConflitoDeHorario,
				CourseRegistration.PacotesDiferentes,
				CourseRegistration.VagasEsgotadas) as ex:
				messages.error(request, ex.msg)
			except IntegrityError:
				messages.error(request, u'O usuário já participa deste minicurso!')

	context = {
		'active_courses': True,
		'course': course,
		'users': course.get_registered_users(),
		'form': form
	}
	return render(request,'management/courses_members.html', context)


@staff_required
def courses_attendance(request, course_pk):
	course = get_object_or_404(Course, pk=course_pk)
	slots = course.slots.order_by('start_date', 'start_time')

	# pra ter estilos base decentes sem trabalho extra
	stylesheet = getSampleStyleSheet()

	# os dados que vão aparecer na tabela de verdade
	users = SemcompUser.objects.in_course(course).order_by('full_name')
	user_data = [
		[Paragraph(user.full_name, stylesheet['Normal']), user.badge, '']
		for user in users
	]
	header_fields = [_(u'Nome'), _(u'Crachá'), _(u'Assinatura')]

	# escreve o pdf num StringIO pra mandar na resposta
	output = StringIO()
	doc = SimpleDocTemplate(output, pagesize=A4)

	story = []
	subtitle_text = u'<para alignment="center" spaceafter="10">{}</para>'
	slot_format = u'{}, {} - {}'

	for slot in slots:
		# escreve cabeçalho, só vai aparecer na primeira página de cada slot
		story.append(Paragraph(course.title, stylesheet['Title']))
		story.append(Paragraph(
			subtitle_text.format(slot_format.format(
				date(slot.start_date, 'l'),
				time(slot.start_time, r'H\hi'),
				time(slot.end_time, r'H\hi'),
				course.place,
			)),
			stylesheet['Normal']
		))
		story.append(Paragraph(
			subtitle_text.format(course.place),
			stylesheet['Normal']
		))

		# aqui os dados de verdade. a tabela quebra páginas sozinha
		t = Table(
			[header_fields] + user_data,
			colWidths=(None, 30*mm, 50*mm),
			rowHeights=12*mm,
			repeatRows=1
		)
		t.setStyle(
			TableStyle([
				('FONTNAME', (0, 0), (-1, 0), _baseFontNameB),
				('LINEBELOW', (0, 0), (-1, 0), 0.5, (0, 0, 0)),
				('LINEBELOW', (2, 0), (2, -1), 0.5, (0, 0, 0)),
				('ALIGN', (1, 0), (-1, -1), 'CENTER'),
			])
		)
		story.append(t)

		# quebra a página pra poder ter listas de presença separadas pra cada
		# horário do minicurso
		story.append(PageBreak())

	# função legal que serve pra, junto do doc.build, colocar o número da
	# página. não coloco o número total de páginas porque achei desnecessário,
	# mas se alguém quiser fazer isso algum dia, parece que esse é o jeito
	# certo: http://code.activestate.com/recipes/576832/
	def add_page_number(canvas, doc):
		page_num = canvas.getPageNumber()
		text = u'Página {}'.format(page_num)

		canvas.drawRightString(
			doc.pagesize[0] - doc.rightMargin,
			doc.bottomMargin / 2.0,
			text
		)

	doc.build(story, onFirstPage=add_page_number, onLaterPages=add_page_number)

	response = HttpResponse(output.getvalue(), content_type='application/pdf')

	# faz o nome do arquivo ter parte do nome do minicurso
	content_filename = 'presenca-minicurso-{}.pdf'.format(course.slug(3))
	response['Content-Disposition'] = 'attachment; filename={}'.format(
		content_filename
	)
	return response


@staff_required
def courses_expel(request, course_pk, user_pk):
	course = get_object_or_404(Course, pk=course_pk)
	user = get_object_or_404(SemcompUser, pk=user_pk)
	if request.method == 'POST':
		form = CourseExpelForm(request.POST)
		if form.is_valid():
			try:
				registration = CourseRegistration.objects.get(user=user, course=course)
				registration.delete()
				msg = u'A inscrição do usuário {} foi cancelada para o minicurso {}'
				messages.success(
					request,
					msg.format(user.full_name, course.title)
				)
				stats.add_event(
					'course-management',
					{
						'action': 'expel-member',
						'user': {
							'id': request.user.pk,
							'name': request.user.full_name,
						},
						'registration': {
							'member': {
								'id': user.pk,
								'name': user.full_name,
							},
							'course': {
								'id': course.pk,
								'title': course.title,
								'vacancies': course.get_remaining_vacancies()
							},
						},
						'send_mail': form.cleaned_data['send_mail'],
						'comentario':form.cleaned_data['comentario'],
					}
				)
				if form.cleaned_data['send_mail']:
					email_expel(user, course, form.cleaned_data['comentario'])
			except CourseRegistration.DoesNotExist:
				pass
			return redirect('management_courses_members', course.pk)
	else:
		form = CourseExpelForm()
	context = {
		'form': form,
		'course_member': user,
		'course': course
	}
	return render(request,'management/courses_expel.html', context)

def email_expel(user, course, comentario):
	msg_context = {
		'user': user,
		'course': course,
		'comentario': comentario
	}

	data = {}
	data['subject'] = u'[Semcomp 17] Inscrição cancelada'
	data['message'] = loader.render_to_string(
		'management/courses_expel_message.txt', msg_context
	)
	data['from_email'] = settings.DEFAULT_FROM_EMAIL
	data['recipient_list'] = [user.email]

	msg = EmailMultiAlternatives(
		subject=data['subject'],
		body=data['message'],
		from_email=data['from_email'],
		to=data['recipient_list']
	)

	msg.attach_alternative(
		loader.render_to_string(
			'management/courses_expel_message.html', msg_context
		),
		"text/html"
	)
	msg.send(fail_silently=False)

@staff_required
def courses_delete(request, course_pk):
	course = get_object_or_404(Course, pk=course_pk)
	speaker = course.speaker

	course.delete()

	if speaker:
		speaker.delete()

	return redirect('management_courses')
