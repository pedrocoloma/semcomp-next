from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def manage_overview(request):
	return render(request, 'management/overview.html', {'active_overview': True})

@login_required
def manage_lectures(request):
	return render(request, 'management/lectures.html', {'active_lectures': True})

#aqui tudo era pra ser staff_required
@login_required
def manage_courses(request):
	return render(request, 'management/courses.html', {'active_courses': True})
