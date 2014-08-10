from datetime import datetime

from django.shortcuts import render, redirect

import stats
from website.models import SemcompConfig

from ..forms import SemcompConfigForm
from ..decorators import staff_required, admin_required

@admin_required
def manage_config(request):
	form_fields = SemcompConfig.objects.filter(type='datetime').order_by('name')
	
	form = SemcompConfigForm(request.POST or None, form_fields=form_fields)
	
	if request.method == 'POST':
		if form.is_valid():
			form.save()

			stats_data = {
				'action': 'change',
				'user': {
					'id': request.user.pk,
					'name': request.user.full_name,
				},
				'new_data': [],
			}

			for field in form.new_config:
				value = field.get_value()
				if isinstance(value, datetime):
					value = value.isoformat()

				stats_data['new_data'].append({
					'name': field.name,
					'value': value
				})

			stats.add_event('management-config', stats_data)

			return redirect('management_config')

	context = {
		'active_config': True,
		'form': form,
	}

	return render(request, 'management/config.html', context)
