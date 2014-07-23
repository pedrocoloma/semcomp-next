from datetime import datetime, time, timedelta, date
from itertools import izip_longest
import math

from django import template
from django.conf import settings
from django.db.models import Q
from cms.models import Page

from website.models import Company, Event, Place, RecruitmentProcess

register = template.Library()

@register.inclusion_tag('website/templatetags/render_sponsors.html')
def render_sponsors():
	return {
		'adamantium_sponsors': Company.objects.filter(type='A',).exclude(logo='').order_by('?'),
		'diamond_sponsors': Company.objects.filter(type='B').exclude(logo='').order_by('?'), 
		'sponsors': Company.objects.exclude(type__in = ['A','B','F','Z']).exclude(logo='').order_by('type','?'),
		'partners': Company.objects.filter(type='Z').exclude(logo='').order_by('?'),
	}

@register.inclusion_tag('website/templatetags/render_sponsors_detailed.html')
def render_sponsors_detailed():
	return {
		'sponsors': Company.objects.exclude(type='Z').exclude(logo='').order_by('type','?'),
		'partners': Company.objects.filter(type='Z').exclude(logo='').order_by('?'),
	}

@register.assignment_tag
def get_mapa():
	return {
		'links': [x for x in Page.objects.public() if x.get_slug('pt-br') != 'administracao' ]
	}

@register.inclusion_tag('website/templatetags/render_user_bar.html', takes_context=True)
def render_user_bar(context):
	user = context['user']
	return {
		 'user': user,
	}

# https://github.com/Compass/compass/blob/5247e8668020ca90635786a461605069fc5c5fa4/frameworks/compass/stylesheets/compass/utilities/color/_contrast.scss
@register.simple_tag
def contrast_color(color, dark='#000000', light='#ffffff', threshold=0.4):
	c = color[1:]
	r,g,b = c[0:2], c[2:4], c[4:6]
	r,g,b = map(lambda x: int(x, 16), (r,g,b))
	r,g,b = map(lambda x: x / 255.0, (r,g,b))

	lightness = 0.30 * r + 0.59 * g + 0.11 * b

	if lightness < threshold:
		return light
	else:
		return dark


@register.inclusion_tag('website/templatetags/render_schedule.html')
def render_schedule(render_type="user"):
	first_day = settings.SEMCOMP_START_DATE
	last_day = settings.SEMCOMP_END_DATE
	day_count = (last_day - first_day).days

	events = Event.objects.filter(
		start_date__gte=first_day,
		start_date__lte=last_day,
	)

	time_start = time(8, 0)
	time_end = time(23, 0)
	time_delta = timedelta(minutes=30)
	one_day = timedelta(days=1)

	events_off_semcomp = Event.objects.filter(
		Q(start_date__lte=first_day) | Q(start_date__gte=last_day)
	)

	days = []
	for day in date_range(first_day, last_day, one_day):
		day_events = events.filter(start_date=day)
		day_start = datetime.combine(day, time_start)

		day_data = []
		for e in day_events:
			event_start = datetime.combine(e.start_date, e.start_time)
			dt = event_start - day_start

			day_data.append({
				'type': e.type,
				'type_display': e.get_type_display(),
				'obj': e,
				'slots': e.duration().seconds / time_delta.seconds,
				'start_slot': dt.seconds / time_delta.seconds,
			})

		days.append(day_data)

	timeslots = time_range(time_start, time_end, time_delta)

	context = {
		'active_events': True,
		'days': days,
		'timeslots': timeslots,
		'is_management': render_type == 'management',
	}

	return context


@register.inclusion_tag('website/templatetags/render_recruitment_processes.html')
def render_recruitment_processes():
	processes = RecruitmentProcess.objects.exclude(company=None)
	context = {
		'processes': processes,
	}
	return context


@register.simple_tag
def render_place(place):
	assert isinstance(place, Place)

	if place.static_map:
		html = '<img src="{0}">'
		return html.format(place.static_map.url)
	else:
		return ''


@register.assignment_tag
def split_list_n(variable, parts):
	def grouper(iterable, n, fillvalue=None):
		args = [iter(iterable)] * n
		return izip_longest(fillvalue=fillvalue, *args)

	return grouper(
		variable,
		int(math.ceil(len(variable) / float(parts)))
	)

################### helper functions ####################

def time_range(start, end, step):
	while start < end:
		yield start
		dt = datetime.combine(date.today(), start) + step
		start = dt.time()

def date_range(start, end, step):
	while start <= end:
		yield start
		start = start + step
