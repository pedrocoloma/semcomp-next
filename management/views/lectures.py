from django.shortcuts import render, redirect, get_object_or_404

from ..decorators import staff_required

@staff_required
def manage_lectures(request):
	return render(request, 'management/lectures.html', {'active_lectures': True})
