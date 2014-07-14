from django.shortcuts import render, redirect, get_object_or_404

from website.models import Event, Course, Speaker

from ..decorators import staff_required

from ..forms import CourseForm, SpeakerForm, ContactInformationFormset

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
		course_form = CourseForm(request.POST, prefix='course')
		speaker_form = SpeakerForm(request.POST, request.FILES, prefix='speaker')
		contact_formset = ContactInformationFormset(request.POST, prefix='contact')

		if course_form.is_valid():
			course = course_form.save(commit=False)
			if speaker_form.has_changed():
				if speaker_form.is_valid() and contact_formset.is_valid():
					contact = contact_formset.save(commit=False)
					speaker = speaker_form.save()

					course.speaker = speaker

					for c in contact:
						c.speaker = speaker
						c.save()

					course.save()
					course_form.save_m2m()

					return redirect('management_courses')
			else:
					course.save()
					course_form.save_m2m()

					return redirect('management_courses')
	else:
		speaker_form = SpeakerForm(prefix='speaker')
		course_form = CourseForm(prefix='course')
		contact_formset = ContactInformationFormset(instance=Speaker(), prefix='contact')
		course_form.fields['slots'].queryset = Event.objects.filter(type='minicurso')

	return render(
		request,
		'management/courses_change.html',
		{
			'course_form': course_form,
			'speaker_form': speaker_form,
			'contact_formset': contact_formset,
			'active_courses': True,
		}
	)

@staff_required
def courses_edit(request, course_pk):
	course = get_object_or_404(Course, pk=course_pk)
	speaker = course.speaker
	contact = speaker.contactinformation_set if speaker else None

	if request.method == 'POST':
		course_form = CourseForm(request.POST, instance=course, prefix='course')
		speaker_form = SpeakerForm(request.POST, request.FILES, instance=speaker, prefix='speaker')
		contact_formset = ContactInformationFormset(request.POST, instance=speaker, prefix='contact')

		if course_form.is_valid():
			course = course_form.save(commit=False)
			if speaker_form.has_changed():
				if speaker_form.is_valid() and contact_formset.is_valid():
					contact = contact_formset.save(commit=False)
					speaker = speaker_form.save()

					course.speaker = speaker

					for c in contact:
						c.speaker = speaker
						c.save()

					course.save()
					course_form.save_m2m()

					return redirect('management_courses')
			else:
				course.save()
				course_form.save_m2m()

				return redirect('management_courses')
	else:
		course_form = CourseForm(instance=course, prefix='course')
		speaker_form = SpeakerForm(instance=speaker, prefix='speaker')
		contact_formset = ContactInformationFormset(instance=speaker, prefix='contact')
		course_form.fields['slots'].queryset = Event.objects.filter(type='minicurso')

	context = {
		'course_form': course_form,
		'speaker_form': speaker_form,
		'contact_formset': contact_formset,
		'active_courses': True,
	}
	return render(request,'management/courses_change.html', context)

@staff_required
def courses_delete(request, course_pk):
	course = get_object_or_404(Course, pk=course_pk)
	speaker = course.speaker

	course.delete()

	if speaker:
		speaker.delete()

	return redirect('management_courses')
