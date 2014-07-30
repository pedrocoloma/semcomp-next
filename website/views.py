# coding: utf-8

from django.db.models import Max, Min
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist

from website.models import Event, Course, Company, BusinessLecture, RecruitmentProcess

def event_details(request, event_id, slug=None):
	event = get_object_or_404(Event, pk=event_id)
	if not event.needs_custom_page():
		raise Http404()

	absolute_url = event.get_absolute_url()
	if request.get_full_path() != absolute_url:
		return redirect(absolute_url)

	template_name = {
		"palestra": "website/lecture_details_include.html",
		"minicurso": "website/courses_details_include.html",
	}.get(
		event.type,
		'website/event_details_include.html',
	)

	if request.is_ajax():
		template = template_name
	else:
		template = 'website/event_details.html'

	context = {
		"event": event,
		"template_name": template_name
	}

	return render(request, template, context)

def course_details(request, course_id, slug=None):
	course = get_object_or_404(Course, pk=course_id)

	absolute_url = course.get_absolute_url()
	if request.get_full_path() != absolute_url:
		return redirect(absolute_url)

	detail_template = 'website/course_details_include.html'
	main_template = 'website/event_details.html'

	context = {
		'course': course,
	}

	if request.is_ajax():
		template = detail_template
	else:
		template = main_template
		context['template_name'] = detail_template

	course_date_time = course.slots.aggregate(
		Min('start_time'), Max('end_time'),
		Min('start_date'), Max('end_date')
	)
	# annotate manually
	course.start_time = course_date_time['start_time__min']
	course.end_time = course_date_time['end_time__max']
	course.start_date = course_date_time['start_date__min']
	course.end_date = course_date_time['end_date__max']

	return render(request, template, context)

def company_details(request, company_id, slug=None):
	company = get_object_or_404(Company, pk=company_id)

	absolute_url = company.get_absolute_url()
	if request.get_full_path() != absolute_url:
		return redirect(absolute_url)

	detail_template = 'website/company_details_include.html'
	main_template = 'website/event_details.html'

	try:
		lecture = BusinessLecture.objects.get(company=company)
	except ObjectDoesNotExist:
		lecture = None

	try:
		recruitment = RecruitmentProcess.objects.get(company=company)
	except ObjectDoesNotExist:
		recruitment = None

	context = {
		'company': company,
		'lecture': lecture,
		'recruitment': recruitment,
	}
	if request.is_ajax():
		template = detail_template
	else:
		template = main_template
		context['template_name'] = detail_template
	return render(request, template, context)