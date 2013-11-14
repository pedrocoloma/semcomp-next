from django.shortcuts import render, redirect, get_object_or_404

from ..decorators import staff_required

@staff_required
def manage_courses(request):
	return render(request, 'management/courses.html', {'active_courses': True})
