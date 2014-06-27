import math
from itertools import izip_longest

from django import template
from cms.models import Page
from website.models import Company

register = template.Library()

@register.inclusion_tag('website/templatetags/render_sponsors.html')
def render_sponsors():
	return {
		'adamantium_sponsors': Company.objects.filter(type='A',).exclude(logo=''),
		'diamond_sponsors': Company.objects.filter(type='B').exclude(logo=''), 
		'sponsors': Company.objects.exclude(type__in = ['A','B','Z']).exclude(logo=''),
		'partners': Company.objects.filter(type='Z').exclude(logo=''),
	}

@register.inclusion_tag('website/templatetags/render_sponsors_detailed.html')
def render_sponsors_detailed():
	return {
		'sponsors': Company.objects.exclude(type__in = ['A','B','Z']).exclude(logo='').order_by('type','?'),
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

@register.assignment_tag
def split_list_n(variable, parts):
	def grouper(iterable, n, fillvalue=None):
		args = [iter(iterable)] * n
		return izip_longest(fillvalue=fillvalue, *args)

	return grouper(
		variable,
		int(math.ceil(len(variable) / float(parts)))
	)

