# coding: utf-8

from website.models import SemcompConfig
from website.utils import signup_allowed, course_registration_open, course_registration_change_close

def semcomp(request):
	# Isso é uma função pra que só vá na base de dados caso realmente precise
	def course_registration_date():
		return SemcompConfig.objects.get(title='COURSE_REGISTRATION_DATE').get_value()
	def payment_date():
		return SemcompConfig.objects.get(title='PAYMENT_DATE').get_value()

	return {
		'signup_allowed': signup_allowed,
		'course_registration_open': course_registration_open,
		'course_registration_date': course_registration_date,
		'course_registration_change_close': course_registration_change_close,
		'payment_date': payment_date
	}
