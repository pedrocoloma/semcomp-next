from django.shortcuts import render, redirect, get_object_or_404

from management.forms import CompanyForm
from website.models import Company

import stats

from ..decorators import staff_required

def add_event(request, form, company, action):
	data = {
		'action': action,
		'user': {
			'id': request.user.id,
			'name': request.user.full_name,
			'email': request.user.email,
		},
		'company': {
			'id': company.pk,
			'name': company.name,
		}
	}

	if action == 'change':
		data['company']['changed_fields'] = form.changed_data

	stats.add_event('management-company', data)


@staff_required
def manage_companies(request):
	context = {'active_companies': True}
	companies = Company.objects.all()
	context['companies'] = companies.order_by('name')
	context['sponsorships'] = companies.exclude(type='Z')
	context['partnerships'] = companies.filter(type='Z')

	return render(request, 'management/companies.html', context)

@staff_required
def companies_add(request):
	context = {'active_companies': True}

	if request.method == 'POST':
		form = CompanyForm(request.POST, request.FILES)
		if form.is_valid():
			company = form.save()
			add_event(request, form, company, 'add')
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
			company = form.save()
			add_event(request, form, company, 'change')
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

	# fazer log antes de apagar pra pegar o ID
	add_event(request, None, company, 'delete')

	company.delete()

	return redirect('management_companies')
