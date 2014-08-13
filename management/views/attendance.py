from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404

from website.models import Event

from ..decorators import staff_required
from ..models import Attendance


@staff_required
def manage_attendance(request):
	context = {
		'active_attendance': True,
		'events': Event.objects.all(),
	}
	return render(request, 'management/attendance.html', context)

@staff_required
def attendance_submit(request, event_pk):
	event = get_object_or_404(Event, pk=event_pk)

	if request.method == 'POST':
		badge = request.POST.get('badge-number', None)
		attendance = Attendance.objects.create_from_badge(event, badge)

	context = {
		'active_attendance': True,
		'event': event,
	}

	return render(request, 'management/attendance_submit.html', context)
