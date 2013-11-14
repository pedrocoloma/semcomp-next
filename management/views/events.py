from django.shortcuts import render, redirect, get_object_or_404

from ..decorators import staff_required

@staff_required
def manage_events(request):
	return render(request, 'management/events.html', {'active_events': True})
