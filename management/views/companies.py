from django.shortcuts import render, redirect, get_object_or_404

from website.forms import CompanyForm
from website.models import Company

from ..decorators import staff_required

@staff_required
def manage_companies(request):
	context = {'active_companies': True}
	companies = Company.objects.all()
	context['companies'] = companies
	context['sponsorships'] = companies.exclude(type='Z')
	context['partnerships'] = companies.filter(type='Z')

	return render(request, 'management/companies.html', context)

@staff_required
def companies_add(request):
	context = {'active_companies': True}

	if request.method == 'POST':
		form = CompanyForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
			return redirect('management_companies')
	else:
		form = CompanyForm()

	context['form'] = form

	return render(request, 'management/companies_change.html', context)

@staff_required
def companies_edit(request, company_pk):
	company = get_object_or_404(Company, pk=company_pk)

	if request.method == 'POST':
		form = CompanyForm(request.POST, request.FILES, instance=company)
		if form.is_valid():
			form.save()
			return redirect('management_companies')
	else:
		form = CompanyForm(instance=company)

	context = {
		'company': company,
		'form': form
	}

	return render(request, 'management/companies_change.html', context)

@staff_required
def companies_delete(request, company_pk):
	company = get_object_or_404(Company, pk=company_pk)

	company.delete()

	return redirect('management_companies')
