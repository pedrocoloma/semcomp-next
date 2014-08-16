from django.utils.timezone import now

from website.models import SemcompConfig

def signup_allowed():
	registration_config = SemcompConfig.objects.get(
		title='REGISTRATION_DATE'
	)

	return now() > registration_config.get_value()

def course_registration_open():
	course_registration_config = SemcompConfig.objects.get(
		title='COURSE_REGISTRATION_DATE'
	)

	return now() > course_registration_config.get_value()

def course_registration_change_close():
	course_registration_change_close_config = SemcompConfig.objects.get(
		title='COURSE_CHANGE_DATE_LIMIT'
	)

	return now() > course_registration_change_close_config.get_value()

def payment_open():
	payment_config = SemcompConfig.objects.get(
		title='PAYMENT_DATE'
	)

	return now() > payment_config.get_value()

def create_semcomp_config():
	from website.models import SemcompConfig
	from django.conf import settings

	for title, data in settings.SEMCOMP_CONFIG.items():
		if not SemcompConfig.objects.filter(title=title).exists():
			config = SemcompConfig.objects.create(
				title=title,
				name=data[0],
				type=data[1]
			)
			config.set_value(data[2])
			config.save()

