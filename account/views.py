from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from website.models import Inscricao
from django.core.exceptions import ObjectDoesNotExist
from forms import InscricoesForm
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
	return render(request, 'account/courses.html', {'active_courses': True})

def account_logout(request):
	logout(request)
	return redirect('account_logout_view')

def account_logout_view(request):
	return render(request, 'account/logout.html')
