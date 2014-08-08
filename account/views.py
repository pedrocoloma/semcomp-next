# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from website.models import Inscricao
from django.core.exceptions import ObjectDoesNotExist
from forms import InscricoesForm
from website.models import Course
from website.models import Event
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
	slot1 = {'day': u'Terça'}
	slot1['tracks'] = []
	slot2 = {'day': u'Quinta'}
	slot2['tracks'] = []
	slots.append(slot1)
	slots.append(slot2)

	# pega os slots de minicurso
	events = Event.objects.filter(type='minicurso')
	# separa o primeiro e o ultimo dia dos minicursos
	first_day_slot = events[0]
	last_day_slot = events[len(events)-1]

	cA = first_day_slot.course_set.filter(track='A')
	cV = first_day_slot.course_set.filter(track='V')
	slot1['tracks'].append(cA)
	slot1['tracks'].append(cV)

	cA = last_day_slot.course_set.filter(track='A')
	cV = last_day_slot.course_set.filter(track='V')
	slot2['tracks'].append(cA)
	slot2['tracks'].append(cV)


	return render(request, 'account/courses.html', {'active_courses': True, 'slots': slots, 'inscricao': inscricao})

def account_logout(request):
	logout(request)
	return redirect('account_logout_view')

def account_logout_view(request):
	return render(request, 'account/logout.html')
