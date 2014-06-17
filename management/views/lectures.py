from django.shortcuts import render, redirect, get_object_or_404

from website.models import Event, Lecture

from ..decorators import staff_required

from ..forms import LectureForm

@staff_required
def manage_lectures(request):
	lectures = Lecture.objects.order_by('slot__start_date', 'slot__start_time')
	return render(
		request,
		'management/lectures.html',
		{
			'active_lectures': True,
			'lectures': lectures
		}
	)

@staff_required
def lectures_add(request):
	if request.method == 'POST':
		form = LectureForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('management_lectures')
	else:
		form = LectureForm()
		form.fields['slot'].queryset = Event.objects.unused('palestra')

	return render(
		request,
		'management/lectures_change.html',
		{
			'form': form,
			'active_lectures': True,
		}
	)

@staff_required
def lectures_edit(request, lecture_pk):
	lecture = get_object_or_404(Lecture, pk=lecture_pk)

	if request.method == 'POST':
		form = LectureForm(request.POST, instance=lecture)
		if form.is_valid():
			form.save()
			return redirect('management_lectures')
	else:
		form = LectureForm(instance=lecture)
		form.fields['slot'].queryset = Event.objects.unused('palestra', lecture.id)

	context = {
		'form': form,
		'active_lectures': True,
	}
	return render(request,'management/lectures_change.html', context)
