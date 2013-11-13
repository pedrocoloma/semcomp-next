from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404

from website.forms import CompanyForm
from website.models import Company, Place

from .decorators import staff_required
from .forms import PlaceForm


@staff_required
def manage_overview(request):
	return render(request, 'management/overview.html', {'active_overview': True})

@staff_required
def manage_places(request):
	context = {
		'active_places': True,
		'places': Place.objects.all(),
	}
	return render(request, 'management/places.html', context)

@staff_required
def places_add(request):
	if request.method == 'POST':
		form = PlaceForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('management_places')
	else:
		form = PlaceForm()

	context = {
		'active_places': True,
		'form': form
	}

	return render(request, 'management/places_add.html', context)

@staff_required
def places_edit(request, place_pk):
	place = get_object_or_404(Place, pk=place_pk)

	if request.method == 'POST':
		form = PlaceForm(request.POST, instance=place)
		if form.is_valid():
			form.save()
			return redirect('management_places')
	else:
		form = PlaceForm(instance=place)

	context = {
		'active_places': True,
		'form': form
	}

	return render(request, 'management/places_add.html', context)

@staff_required
def places_delete(request, place_pk):
	place = get_object_or_404(Place, pk=place_pk)

	place.delete()

	return redirect('management_places')

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
