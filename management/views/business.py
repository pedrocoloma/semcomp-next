# coding: utf-8

from django.shortcuts import render, redirect, get_object_or_404

import stats
from website.models import BusinessLecture

from ..forms import BusinessLectureForm


def add_event(request, form, lecture, action):
	data = {
		'action': action,
		'user': {
			'id': request.user.id,
			'name': request.user.full_name,
			'email': request.user.email,
		},
		'lecture': {
			'id': lecture.pk,
		}
	}

	if action == 'change':
		data['lecture']['changed_fields'] = form.changed_data

	stats.add_event('management-business-lectures', data)


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
			lecture = form.save()
			add_event(request, form, lecture, 'add')
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
			lecture = form.save()
			add_event(request, form, lecture, 'change')
			return redirect('management_business_lectures')
	
	context = {
		'active_business_lectures': True,
		'form': form,
	}
	return render(request, 'management/business_change.html', context)

def business_lectures_delete(request, lecture_pk):
	lecture = get_object_or_404(BusinessLecture, pk=lecture_pk)

	add_event(request, None, lecture, 'delete')
	lecture.delete()

	return redirect('management_business_lectures')
