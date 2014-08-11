# coding: utf-8

from django.conf import settings
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import SuspiciousOperation
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models import Max, Min
from django.shortcuts import render, redirect
from django.template import loader

from account.forms import InscricoesForm
from account.models import CourseRegistration
from website.models import Course, Event, Inscricao
import stats


@login_required
def account_overview(request):
	try:
		inscricao = Inscricao.objects.get(user=request.user)
	except Inscricao.DoesNotExist:
		inscricao = None

	context = {
		'active_overview': True,
		'inscricao': inscricao,
	}

	return render(request, 'account/index.html', context)


@login_required
def payment_overview(request):
	try:
		inscricao = Inscricao.objects.get(user=request.user)
	except Inscricao.DoesNotExist:
		inscricao = None

	context = {
		'active_payment': True,
		'inscricao': inscricao,
	}

	return render(request, 'account/payment_overview.html', context)


@login_required
def payment_send(request):
	inscricao = None
	if request.method == 'POST':
		coffee = 'com_coffee' in request.POST

		try:
			inscricao = Inscricao.objects.get(user=request.user)
			inscricao_form = InscricoesForm(
				request.POST,
				request.FILES,
				instance=inscricao
			)
		except Inscricao.DoesNotExist:
			inscricao_form = InscricoesForm(request.POST, request.FILES)

		if inscricao_form.is_valid():
			inscricao = inscricao_form.save(commit=False)
			inscricao.coffee = coffee
			inscricao.user = request.user
			inscricao.avaliado=False;
			inscricao.save()

			stats.add_event(
				'account-payment',
				{
					'action': 'send',
					'payment': {
						'coffee': coffee,
						'user': {
							'id': request.user.pk,
							'name': request.user.full_name,
							'cpf': inscricao.CPF,
						},
					},
				}
			)

			return redirect('account_payment')
	else:
		try:
			inscricao = Inscricao.objects.get(user=request.user)
			inscricao_form = InscricoesForm(instance=inscricao)
		except Inscricao.DoesNotExist:
			inscricao_form = InscricoesForm()

	context = {
		'active_payment': True,
		'inscricao': inscricao,
		'form': inscricao_form
	}

	return render(request, 'account/payment_send.html', context)


@login_required
def courses(request):
	try:
		inscricao = Inscricao.objects.get(user=request.user)
	except Inscricao.DoesNotExist:
		inscricao = None

	slots = courses_slots()

	user_courses = get_user_courses(request.user)

	context = {
		'active_courses': True,
		'slots': slots,
		'inscricao': inscricao,
		'user_courses': user_courses,
	}

	return render(request, 'account/courses.html', context)


@login_required
def course_register(request):
	try:
		inscricao = Inscricao.objects.get(user=request.user)
		if not inscricao.pagamento:
			raise
	except:
		#não deixa tentar se inscrever sem ter feito pagamento
		msg = u"Inscrição em minicurso sem realizar o pagamento: '%s'"
		raise SuspiciousOperation(msg % request.user.full_name)

	minicursos_sucesso = []
	minicursos_lotados = []
	error = 0

	if request.method == 'POST':
		# pega os slots de minicurso
		events = Event.objects.filter(type='minicurso')
		# separa o primeiro e o ultimo dia dos minicursos
		first_day_slot = events[0]
		last_day_slot = events[len(events)-1]

		user_courses = get_user_courses(request.user)

		minicurso1 = request.POST['minicurso-0']
		minicurso2 = request.POST['minicurso-1']

		minicurso_terca_novo = False
		minicurso_quinta_novo = False

		try:
			if minicurso1 != '-1':
				minicurso_terca_novo = Course.objects.get(pk=minicurso1)

			if minicurso2 != '-1':
				minicurso_quinta_novo = Course.objects.get(pk=minicurso2)
		except Course.DoesNotExist:
			raise SuspiciousOperation(u'Minicurso não existe!')

		minicurso_novo = minicurso_terca_novo and minicurso_quinta_novo
		mesmo_pacote = lambda: minicurso_terca_novo.track == minicurso_quinta_novo.track

		if (minicurso_novo and mesmo_pacote()) or not minicurso_novo:
			minicurso_terca_atual = False
			minicurso_quinta_atual = False

			for reg in user_courses:
				if reg.course.start_date == first_day_slot.start_date:
					minicurso_terca_atual = reg
				elif reg.course.start_date == last_day_slot.start_date:
					minicurso_quinta_atual = reg

			sucesso = register_in_course(
				request.user,
				minicurso_terca_atual,
				minicurso_terca_novo
			)
			if sucesso:
				minicursos_sucesso.append(minicurso_terca_novo)
			else:
				minicursos_lotados.append(minicurso_terca_novo)
				error = 2

			sucesso = register_in_course(
				request.user,
				minicurso_quinta_atual,
				minicurso_quinta_novo
			)
			if sucesso:
				minicursos_sucesso.append(minicurso_quinta_novo)
			else:
				minicursos_lotados.append(minicurso_quinta_novo)
				error = 2
		else:
			error = 1 # minicursos de pacotes diferentes

	slots = courses_slots()
	user_courses = get_user_courses(request.user)

	context = {
		'active_courses': True,
		'slots': slots,
		'inscricao': inscricao,
		'user_courses': user_courses,
		'error':error,
		'minicursos_sucesso': minicursos_sucesso,
		'minicursos_lotados': minicursos_lotados,
		'user': request.user,
	}

	return render(request, 'account/courses.html', context)


def email_course(request, user, course):
	course_date_time = course.slots.aggregate(
		Min('start_time'), Max('end_time'),
		Min('start_date'), Max('end_date')
	)
	# annotate manually
	course.start_time = course_date_time['start_time__min']
	course.end_time = course_date_time['end_time__max']
	course.start_date = course_date_time['start_date__min']
	course.end_date = course_date_time['end_date__max']

	msg_context = {
		'user': user,
		'course': course,
		'absolute_uri': request.get_absolute_uri('/'),
	}

	data = {}
	data['subject'] = u'[Semcomp 17] Inscrição em minicurso'
	data['message'] = loader.render_to_string(
		'account/inscricao_minicurso.txt', msg_context
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
			'account/inscricao_minicurso.html', msg_context
		),
		"text/html"
	)
	msg.send(fail_silently=False)


@transaction.atomic
def register_in_course(user, old, new):
	tem_vagas = False

	stats_data = {
		'action': 'register',
		'user': {
			'id': user.pk,
			'name': user.full_name,
		},
	}

	# se selecionou um minicurso
	if new:
		tem_vagas = new.get_remaining_vacancies() > 0

	# se é o mesmo minicurso de antes, nada a fazer
	if old and new and old.course == new:
		return True

	# se nao tem vagas
	if new and not tem_vagas:
		return False

	# se o novo minicurso deve sobrescrever um minicurso antigo e o novo tem
	# vagas, apaga a inscrição antiga e faz a nova
	if old and new and old.course != new and tem_vagas:
		stats_data['action'] = 'change'
		stats_data['course'] = {
			'id': new.pk,
			'title': new.title,
			'vacancies': new.get_remaining_vacancies() - 1,
		}
		stats_data['old_course'] = {
			'id': old.course.pk,
			'title': old.course.title,
			'vacancies': old.course.get_remaining_vacancies() + 1,
		}

		old.delete()
		cr = CourseRegistration(user=user,course=new)
		cr.save()
	elif old and not new:
		# se tinha um minicurso mas selecionou 'nenhum' então apaga a
		# inscrição antiga
		stats_data['action'] = 'remove'
		stats_data['course'] = {
			'id': old.course.pk,
			'title': old.course.title,
			'vacancies': old.course.get_remaining_vacancies() + 1,
		}

		old.delete()
	elif not old and new and tem_vagas:
		# se não tinha uma inscrição e esta fazendo uma nova e tem vagas
		stats_data['action'] = 'register'
		stats_data['course'] = {
			'id': new.pk,
			'title': new.title,
			'vacancies': new.get_remaining_vacancies() - 1,
		}

		cr = CourseRegistration(user=user,course=new)
		cr.save()

	stats.add_event('account-courses', stats_data)

	return True


def courses_slots():
	slots = []
	slot1 = {}
	slot1['tracks'] = []
	slot2 = {}
	slot2['tracks'] = []
	slots.append(slot1)
	slots.append(slot2)

	# pega os slots de minicurso
	events = Event.objects.filter(type='minicurso').order_by('start_date')
	# separa o primeiro e o ultimo dia dos minicursos
	first_day_slot = events[0]
	last_day_slot = events[len(events)-1]

	slot1['day'] = first_day_slot.start_date
	slot2['day'] = last_day_slot.start_date

	cA = first_day_slot.course_set.filter(track='A')
	cV = first_day_slot.course_set.filter(track='V')
	slot1['tracks'].append(cA)
	slot1['tracks'].append(cV)

	cA = last_day_slot.course_set.filter(track='A')
	cV = last_day_slot.course_set.filter(track='V')
	slot2['tracks'].append(cA)
	slot2['tracks'].append(cV)

	return slots


def get_user_courses(user):
	user_courses = CourseRegistration.objects.filter(user=user)

	for reg in user_courses:
		course = reg.course
		course_date_time = course.slots.aggregate(
			Min('start_time'), Max('end_time'),
			Min('start_date'), Max('end_date')
		)
		# annotate manually
		course.start_time = course_date_time['start_time__min']
		course.end_time = course_date_time['end_time__max']
		course.start_date = course_date_time['start_date__min']
		course.end_date = course_date_time['end_date__max']

	return user_courses


def account_logout(request):
	def get_client_ip(request):
		x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
		if x_forwarded_for:
			ip = x_forwarded_for.split(',')[0]
		else:
			ip = request.META.get('REMOTE_ADDR')
		return ip

	stats.add_event(
		'account-users',
		{
			'action': 'logout',
			'user': {
				'id': request.user.pk,
				'name': request.user.full_name,
			},
			'client_ip': get_client_ip(request),
		}
	)

	logout(request)
	return redirect('account_logout_view')

def account_logout_view(request):
	return render(request, 'account/logout.html')
