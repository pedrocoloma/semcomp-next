# coding: utf-8

from django.shortcuts import render, redirect, get_object_or_404

from website.models import BusinessLecture

from ..forms import BusinessLectureForm

def manage_business_lectures(request):
	context = {
		'active_business_lectures': True,
		'lectures': BusinessLecture.objects.order_by('start_datetime'),
	}

	return render(request, 'management/business.html', context)

def business_lectures_add(request):
	form = BusinessLectureForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('management_business_lectures')
	
	context = {
		'active_business_lectures': True,
		'form': form
	}

	return render(request, 'management/business_change.html', context)

def business_lectures_edit(request, lecture_pk):
	lecture = get_object_or_404(BusinessLecture, pk=lecture_pk)
	form = BusinessLectureForm(request.POST or None, instance=lecture)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('management_business_lectures')
	
	context = {
		'active_business_lectures': True,
		'form': form,
	}
	return render(request, 'management/business_change.html', context)

def business_lectures_delete(request, lecture_pk):
	lecture = get_object_or_404(BusinessLecture, pk=lecture_pk)
	lecture.delete()

	return redirect('management_business_lectures')
