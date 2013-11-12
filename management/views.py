from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect

from website.forms import CompanyForm
from website.models import Company

from .decorators import staff_required


@staff_required
def manage_overview(request):
	return render(request, 'management/overview.html', {'active_overview': True})

@staff_required
def manage_events(request):
	return render(request, 'management/events.html', {'active_events': True})

@staff_required
def manage_lectures(request):
	return render(request, 'management/lectures.html', {'active_lectures': True})

@staff_required
def manage_courses(request):
	return render(request, 'management/courses.html', {'active_courses': True})

@staff_required
def manage_users(request):
	return render(request, 'management/users.html', {'active_users': True})

@staff_required
def manage_companies(request):
	context = {'active_companies': True}
	companies = Company.objects.all()
	context['companies'] = companies
	context['sponsorships'] = companies.filter(type='P')
	context['partnerships'] = companies.filter(type='A')

	return render(request, 'management/companies.html', context)

@staff_required
def companies_add(request):
	context = {'active_companies': True}

	if request.method == 'POST':
		form = CompanyForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect(reverse('management_companies'))
	else:
		form = CompanyForm()

	context['form'] = form

	return render(request, 'management/companies_add.html', context)
