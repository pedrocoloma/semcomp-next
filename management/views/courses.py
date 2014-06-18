from django.shortcuts import render, redirect, get_object_or_404

from website.models import Event, Course

from ..decorators import staff_required

from ..forms import CourseForm

@staff_required
def manage_courses(request):
	courses = Course.objects.all()
	return render(
		request,
		'management/courses.html',
		{
			'active_courses': True,
			'courses': courses
		}
	)

@staff_required
def courses_add(request):
	if request.method == 'POST':
		form = CourseForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('management_courses')
	else:
		form = CourseForm()
		form.fields['slots'].queryset = Event.objects.filter(type='minicurso')

	return render(
		request,
		'management/courses_change.html',
		{
			'form': form,
			'active_courses': True,
		}
	)

@staff_required
def courses_edit(request, course_pk):
	course = get_object_or_404(Course, pk=course_pk)

	if request.method == 'POST':
		form = CourseForm(request.POST, instance=course)
		if form.is_valid():
			form.save()
			return redirect('management_courses')
	else:
		form = CourseForm(instance=course)
		form.fields['slots'].queryset = Event.objects.filter(type='minicurso')

	context = {
		'form': form,
		'active_courses': True,
	}
	return render(request,'management/courses_change.html', context)

@staff_required
def courses_delete(request, course_pk):
	course = get_object_or_404(Course, pk=course_pk)

	course.delete()

	return redirect('management_courses')
