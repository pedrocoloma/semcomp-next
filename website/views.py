# coding: utf-8

from django.db.models import Max, Min
from django.shortcuts import render, get_object_or_404
from django.http import Http404

from website.models import Event, Course

def event_details(request, event_id):
	event = get_object_or_404(Event, pk=event_id)
	if not event.needs_custom_page():
		raise Http404()

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

def course_details(request, course_id):
	course = get_object_or_404(Course, pk=course_id)

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
