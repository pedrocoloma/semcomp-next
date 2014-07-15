from django.shortcuts import render, redirect, get_object_or_404

from website.models import Event, Lecture, Speaker

from ..decorators import staff_required

from ..forms import LectureForm, SpeakerForm, ContactInformationFormset

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
		lecture_form = LectureForm(request.POST, prefix='lecture')
		speaker_form = SpeakerForm(request.POST, request.FILES, prefix='speaker')
		contact_formset = ContactInformationFormset(request.POST, prefix='contact')

		if lecture_form.is_valid():
			lecture = lecture_form.save(commit=False)
			if speaker_form.has_changed():
				if speaker_form.is_valid() and contact_formset.is_valid():
					contact = contact_formset.save(commit=False)
					speaker = speaker_form.save()

					lecture.speaker = speaker

					for c in contact:
						c.speaker = speaker
						c.save()
					lecture.save()
					return redirect('management_lectures')
			else:
				lecture.save()
				return redirect('management_lectures')
	else:
		speaker_form = SpeakerForm(prefix='speaker')
		lecture_form = LectureForm(prefix='lecture')
		contact_formset = ContactInformationFormset(instance=Speaker(), prefix='contact')
		lecture_form.fields['slot'].queryset = Event.objects.unused('palestra')

	return render(
		request,
		'management/lectures_change.html',
		{
			'lecture_form': lecture_form,
			'speaker_form': speaker_form,
			'contact_formset': contact_formset,
			'active_lectures': True,
		}
	)

@staff_required
def lectures_edit(request, lecture_pk):
	lecture = get_object_or_404(Lecture, pk=lecture_pk)
	speaker = lecture.speaker
	contact = speaker.contactinformation_set if speaker else None

	if request.method == 'POST':
		lecture_form = LectureForm(request.POST, instance=lecture, prefix='lecture')
		speaker_form = SpeakerForm(request.POST, request.FILES, instance=speaker, prefix='speaker')
		contact_formset = ContactInformationFormset(request.POST, instance=speaker, prefix='contact')

		if lecture_form.is_valid():
			lecture = lecture_form.save(commit=False)
			if speaker_form.has_changed():
				if speaker_form.is_valid() and contact_formset.is_valid():
					contact = contact_formset.save(commit=False)
					speaker = speaker_form.save()

					lecture.speaker = speaker

					for c in contact:
						c.speaker = speaker
						c.save()
					lecture.save()
					return redirect('management_lectures')
			else:
				lecture.save()
				return redirect('management_lectures')
	else:
		lecture_form = LectureForm(instance=lecture, prefix='lecture')
		speaker_form = SpeakerForm(instance=speaker, prefix='speaker')
		contact_formset = ContactInformationFormset(instance=speaker, prefix='contact')
		lecture_form.fields['slot'].queryset = Event.objects.unused('palestra', lecture.slot.id)

	context = {
		'lecture_form': lecture_form,
		'speaker_form': speaker_form,
		'contact_formset': contact_formset,
		'active_lectures': True,
	}
	return render(request,'management/lectures_change.html', context)

@staff_required
def lectures_delete(request, lecture_pk):
	lecture = get_object_or_404(Lecture, pk=lecture_pk)
	speaker = lecture.speaker

	lecture.delete()

	if speaker:
		speaker.delete()

	return redirect('management_lectures')
