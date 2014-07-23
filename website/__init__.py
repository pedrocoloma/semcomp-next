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

