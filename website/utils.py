from django.utils.timezone import now

from website.models import SemcompConfig

def signup_allowed():
	registration_config = SemcompConfig.objects.get(
		title='REGISTRATION_DATE'
	)

	return now() > registration_config.get_value()
