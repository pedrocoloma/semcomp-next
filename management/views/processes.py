# coding: utf-8

from django.shortcuts import render, redirect, get_object_or_404

from website.models import RecruitmentProcess

from ..forms import RecruitmentProcessForm

def manage_processes(request):
	context = {
		'active_processes': True,
		'processes': RecruitmentProcess.objects.order_by('start_datetime'),
	}

	return render(request, 'management/processes.html', context)

def processes_add(request):
	form = RecruitmentProcessForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('management_processes')

	context = {
		'active_processes': True,
		'form': form,
	}
	return render(request, 'management/processes_change.html', context)

def processes_edit(request, process_pk):
	process = get_object_or_404(RecruitmentProcess, pk=process_pk)
	form = RecruitmentProcessForm(request.POST or None, instance=process)
	if request.method == 'POST':
		if form.is_valid():
			form.save()
			return redirect('management_processes')
	
	context = {
		'active_processes': True,
		'form': form,
	}
	return render(request, 'management/processes_change.html', context)

def processes_delete(request, process_pk):
	process = get_object_or_404(RecruitmentProcess, pk=process_pk)
	process.delete()

	return redirect('management_processes')
