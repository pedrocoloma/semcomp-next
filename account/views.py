from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from website.models import Inscricao
from django.core.exceptions import ObjectDoesNotExist
@login_required
def account_overview(request):
	return render(request, 'account/index.html', {'active_overview': True})

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
def courses(request):
	return render(request, 'account/courses.html', {'active_courses': True})
