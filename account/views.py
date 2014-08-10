# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from website.models import Inscricao
from django.core.exceptions import ObjectDoesNotExist
from forms import InscricoesForm
from website.models import Course,Event,CourseRegistration
from django.db.models import Max, Min

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

	user_courses = CourseRegistration.objects.filter(user=request.user)

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


	return render(request, 'account/courses.html', {'active_courses': True, 'slots': slots, 'inscricao': inscricao, 'user_courses': user_courses})

@login_required
def course_register(request):
	try:
		inscricao = Inscricao.objects.get(user=request.user)
	except ObjectDoesNotExist:
		inscricao = None

	return redirect('account_courses')

def account_logout(request):
	logout(request)
	return redirect('account_logout_view')

def account_logout_view(request):
	return render(request, 'account/logout.html')
