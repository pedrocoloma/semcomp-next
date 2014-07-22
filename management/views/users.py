from django.shortcuts import render, redirect, get_object_or_404
from website.models import SemcompUser, Inscricao
from ..decorators import staff_required
from ..forms import UserManagementForm

@staff_required
def manage_users(request):
	usuarios = SemcompUser.objects.all()
	pendencias = SemcompUser.objects.filter(inscricao__pagamento=False, inscricao__avaliado=False,inscricao__comprovante__isnull=False)
	
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
