import math
from itertools import izip_longest

from django import template

from website.models import Company

register = template.Library()

@register.inclusion_tag('website/templatetags/render_sponsors.html')
def render_sponsors():
	return {
		'sponsors': Company.objects.filter(type='P'),
		'partners': Company.objects.filter(type='A'),
	}

@register.inclusion_tag('website/templatetags/render_user_bar.html', takes_context=True)
def render_user_bar(context):
	user = context['user']
	return {
		 'user': user,
	}

@register.assignment_tag
def split_list_n(variable, parts):
	def grouper(iterable, n, fillvalue=None):
		args = [iter(iterable)] * n
		return izip_longest(fillvalue=fillvalue, *args)

	return grouper(
		variable,
		int(math.ceil(len(variable) / float(parts)))
	)

