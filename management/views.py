from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .decorators import staff_required
from website.forms import CompanyForm

@staff_required
def manage_overview(request):
	return render(request, 'management/overview.html', {'active_overview': True})

@staff_required
def manage_lectures(request):
	return render(request, 'management/lectures.html', {'active_lectures': True})

@staff_required
def manage_courses(request):
	return render(request, 'management/courses.html', {'active_courses': True})

@staff_required
def manage_companies(request):
	return render(request, 'management/companies.html', {'active_companies': True})

@staff_required
def companies_add(request):
	context = {'active_companies': True}

	if request.method == 'POST':
		form = CompanyForm(request.POST, request.FILES)
		if form.is_valid():
			form.save()
	else:
		form = CompanyForm()

	context['form'] = form

	return render(request, 'management/companies_add.html', context)
