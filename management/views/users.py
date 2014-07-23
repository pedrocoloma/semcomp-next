from django.shortcuts import render, redirect, get_object_or_404
from website.models import SemcompUser, Inscricao
from ..decorators import staff_required
from ..forms import UserManagementForm, InscricaoManagementForm
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.template import loader
from django.conf import settings

def mail_user(aprovado, comentario, nome, email):
    data = {}
    data['subject'] = 'Contato Semcomp'
    data['message'] = loader.render_to_string('management/payment_notification.txt', {
    	'aprovado': aprovado,
    	'nome': nome,
    	'comentario': comentario,
    	})
    data['from_email'] = settings.DEFAULT_FROM_EMAIL
    data['recipient_list'] = [email]

    msg = EmailMultiAlternatives(subject=data['subject'], body=data['message'], from_email=data['from_email'], to=data['recipient_list'])

    msg.attach_alternative(loader.render_to_string('management/payment_notification.html', {
    	'aprovado': aprovado,
    	'nome': nome,
    	'comentario': comentario,
    	}), "text/html")
    msg.send(fail_silently=False)
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
		if 'is_admin' in user_form.changed_data or 'is_staff' in user_form.changed_data:
			return redirect('management_users')
		if(user_form.is_valid()):
			user_form.save()
			return redirect('management_users')
	user_form = UserManagementForm(instance=user)
	return render(request, 'management/users_change.html', {
		'active_users': True,
		'admin':request.user.is_admin,
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
				mail_user(True, inscricao_form.cleaned_data.get('comentario'), user.full_name, user.email)
			elif 'rejeitar' in request.POST:
				i.pagamento = False
				i.avaliado=True
				mail_user(False, inscricao_form.cleaned_data.get('comentario'), user.full_name, user.email)
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
