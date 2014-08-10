# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from website.models import Inscricao
from django.core.exceptions import ObjectDoesNotExist
from forms import InscricoesForm
from website.models import Course,Event
from account.models import CourseRegistration
from django.db.models import Max, Min
from django.core.exceptions import SuspiciousOperation
from django.db import transaction

@login_required
def account_overview(request):
	try:
		inscricao = Inscricao.objects.get(user=request.user)
	except ObjectDoesNotExist:
		inscricao = None
	return render(request, 'account/index.html', {'active_overview': True, 'inscricao':inscricao})

@login_required
def payment_overview(request):
	try:
		inscricao = Inscricao.objects.get(user=request.user)
	except ObjectDoesNotExist:
		inscricao = None
	return render(request, 'account/payment_overview.html', 
			{
			'active_payment': True,
			'inscricao': inscricao
			}
		)
@login_required
def payment_send(request):
	inscricao = None
	if request.method == 'POST':
		coffee = 'com_coffee' in request.POST
		try:
			inscricao = Inscricao.objects.get(user=request.user)
			inscricao_form = InscricoesForm(request.POST, request.FILES, instance=inscricao)
		except ObjectDoesNotExist:
			inscricao_form = InscricoesForm(request.POST, request.FILES)
		if inscricao_form.is_valid():
			inscricao = inscricao_form.save(commit=False)
			inscricao.coffee = coffee
			inscricao.user = request.user
			inscricao.avaliado=False;
			inscricao.save()
			return redirect('account_payment')
	else:
		try:
			inscricao = Inscricao.objects.get(user=request.user)
			inscricao_form = InscricoesForm(instance=inscricao)
		except ObjectDoesNotExist:
			inscricao_form = InscricoesForm()
	return render(request, 'account/payment_send.html', 
			{
			'active_payment': True,
			'inscricao': inscricao,
			'form':inscricao_form,
			}
		)

@login_required
def courses(request):
	try:
		inscricao = Inscricao.objects.get(user=request.user)
	except ObjectDoesNotExist:
		inscricao = None

	slots = courses_slots()

	user_courses = get_user_courses(request.user)


	return render(request, 'account/courses.html', {'active_courses': True, 'slots': slots, 'inscricao': inscricao, 'user_courses': user_courses})

@login_required
def course_register(request):

	try:
		inscricao = Inscricao.objects.get(user=request.user)
	except ObjectDoesNotExist:
		#não deixa tentar se inscrever sem ter feito pagamento
		raise SuspiciousOperation(u"Inscrição em minicurso sem realizar o pagamento: '%s'" % request.user.full_name)

	if not inscricao.pagamento:
		raise SuspiciousOperation(u"Inscrição em minicurso sem realizar o pagamento: '%s'" % request.user.full_name)

	if request.method == 'POST':
		# pega os slots de minicurso
		events = Event.objects.filter(type='minicurso')
		# separa o primeiro e o ultimo dia dos minicursos
		first_day_slot = events[0]
		last_day_slot = events[len(events)-1]

		user_courses = get_user_courses(request.user)

		minicurso1 = request.POST['minicurso-1']
		minicurso2 = request.POST['minicurso-2']

		minicurso_terca_novo = False
		minicurso_quinta_novo = False

		if minicurso1 != '-1':
			minicurso_terca_novo = Course.objects.get(pk=minicurso1)

		if minicurso2 != '-1':
			minicurso_quinta_novo = Course.objects.get(pk=minicurso2)

		error = 0
		if (minicurso_terca_novo and minicurso_quinta_novo and minicurso_terca_novo.track == minicurso_quinta_novo.track) or (not minicurso_terca_novo or not minicurso_quinta_novo):
			minicurso_terca_atual = False
			minicurso_quinta_atual = False

			for reg in user_courses:
				if reg.course.start_date == first_day_slot.start_date:
					minicurso_terca_atual = reg
				elif reg.course.start_date == last_day_slot.start_date:
					minicurso_quinta_atual = reg

			sucesso = register_in_course(request.user, minicurso_terca_atual, minicurso_terca_novo)
			if not sucesso:
				error = 2
			sucesso = register_in_course(request.user, minicurso_quinta_atual, minicurso_quinta_novo)
			if not sucesso:
				error = 2


			#if minicurso_quinta_atual:
			#	print "minicurso_quinta_atual quinta"
			#	print minicurso_quinta_atual.course.title

			#print "request:"
			#print request.POST['minicurso-1']
			#print request.POST['minicurso-2']
		else:
			error = 1 # minicursos de pacotes diferentes



	slots = courses_slots()
	user_courses = get_user_courses(request.user)

	return render(request, 'account/courses.html', {'active_courses': True, 'slots': slots, 'inscricao': inscricao, 'user_courses': user_courses, 'error':error})

@transaction.atomic
def register_in_course(user,old,new):
	tem_vagas = False
	# se selecionou um minicurso
	if new:
		tem_vagas = new.get_remaining_vacancies() > 0
	# se é o mesmo minicurso de antes, nada a fazer
	if old and new and old.course == new:
		return True
	# se nao tem vagas
	if new and not tem_vagas:
		return False
	# se o novo minicurso deve sobrescrever um minicurso antigo e o novo tem vagas, apaga a inscrição antiga e faz a nova
	if old and new and old.course != new and tem_vagas:
		print "minicurso terca old"
		print old.course.title
		old.delete()
		cr = CourseRegistration(user=user,course=new)
		cr.save()
	# se tinha um minicurso mas selecionou 'nenhum' então apaga a inscrição antiga
	elif old and not new:
		old.delete()
	# se não tinha uma inscrição e esta fazendo uma nova e tem vagas
	elif not old and new and tem_vagas:
		cr = CourseRegistration(user=user,course=new)
		cr.save()

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
	events = Event.objects.filter(type='minicurso')
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
	logout(request)
	return redirect('account_logout_view')

def account_logout_view(request):
	return render(request, 'account/logout.html')
