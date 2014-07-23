from django.shortcuts import render, redirect

from website.models import SemcompConfig

from ..forms import SemcompConfigForm

def manage_config(request):
	form_fields = SemcompConfig.objects.filter(type='datetime')
	
	form = SemcompConfigForm(request.POST or None, form_fields=form_fields)
	
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('management_config')

	context = {
		'active_config': True,
		'form': form,
	}

	return render(request, 'management/config.html', context)
