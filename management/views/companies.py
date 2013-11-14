from django.shortcuts import render, redirect, get_object_or_404

from website.forms import CompanyForm
from website.models import Company

from ..decorators import staff_required

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
