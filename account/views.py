from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import logout

@login_required
def account_overview(request):
	return render(request, 'account/index.html', {'active_overview': True})

@login_required
def payment(request):
	return render(request, 'account/payment.html', {'active_payment': True})

@login_required
def courses(request):
	return render(request, 'account/courses.html', {'active_courses': True})

def account_logout(request):
	logout(request)
	return redirect('account_logout_view')

def account_logout_view(request):
	return render(request, 'account/logout.html')