from django.shortcuts import render, redirect, get_object_or_404
from website.models import SemcompUser, Inscricao
from ..decorators import staff_required
from ..forms import UserManagementForm, InscricaoManagementForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist

def mail_user(aprovado, comentario, email):
	print aprovado
	send_mail('Pagamento', 'Seu pagamento foi aprovado', 'from@teste.com', [email], fail_silently=False)
@staff_required
def manage_users(request):
	usuarios = SemcompUser.objects.all()
	pendencias = SemcompUser.objects.filter(inscricao__pagamento=False, inscricao__avaliado=False).exclude(inscricao__comprovante__exact='')
	
	return render(request, 'management/users.html', {
		'active_users': True,
		'usuarios': usuarios,
		'pendencias': pendencias,
		'total_inscritos': usuarios.count(),
		'total_pagos':Inscricao.objects.filter(pagamento=True).count(),
		'total_coffee': Inscricao.objects.filter(pagamento=True, coffee=True).count(),
		'total_sem_coffee': Inscricao.objects.filter(pagamento=True, coffee=False).count(),
		'total_pendentes': pendencias.count(),
		})

@staff_required
def users_edit(request, user_pk):
	user = get_object_or_404(SemcompUser, pk=user_pk)
	if request.method == 'POST':
		user_form = UserManagementForm(request.POST, instance=user)
		if(user_form.is_valid()):
			user_form.save()
			return redirect('management_users')
	user_form = UserManagementForm(instance=user)
	return render(request, 'management/users_change.html', {
		'active_users': True,
		'user': user,
		'user_form':user_form,
		})
@staff_required
def users_validate(request, user_pk):
	user = get_object_or_404(SemcompUser, pk=user_pk)
	inscricao = None
	if request.method == 'POST':
		try:
			inscricao = Inscricao.objects.get(user=user)
			inscricao_form = InscricaoManagementForm(request.POST, request.FILES, instance=inscricao)
		except ObjectDoesNotExist:
			inscricao = Inscricao(user=user)
			inscricao_form = InscricaoManagementForm(request.POST, request.FILES, instance=inscricao)
		if inscricao_form.is_valid():
			i = inscricao_form.save(commit=False)
			if 'aprovar' in request.POST:
				i.pagamento = True
				i.avaliado=True
				mail_user(True, "nada", user.email)
			elif 'rejeitar' in request.POST:
				i.pagamento = False
				i.avaliado=True
				mail_user(False, "nada", user.email)
			i.save()
			return redirect('management_users')
	else:
		try:
			inscricao = Inscricao.objects.get(user=user)
			inscricao_form = InscricaoManagementForm(instance=inscricao)
		except ObjectDoesNotExist:
			inscricao_form = InscricaoManagementForm()

	return render(request, 'management/users_validate.html', {
		'active_users': True,
		'user': user,
		'inscricao': inscricao,
		'inscricao_form': inscricao_form,
		})
