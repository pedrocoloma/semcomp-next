from StringIO import StringIO

from django.shortcuts import render, redirect, get_object_or_404
from django.core.files import File

from website.models import Place

from ..decorators import staff_required
from ..forms import PlaceForm
from ..utils import get_static_map_image

def save_static_map(place):
	image = get_static_map_image(
		float(place.latitude),
		float(place.longitude),
		place.zoom
	)

	output_buffer = StringIO()
	image.save(output_buffer, 'png')
	output_buffer.seek(0)

	image_file = File(output_buffer)
	place.static_map.save('output-static-map.png', image_file)


@staff_required
def manage_places(request):
	context = {
		'active_places': True,
		'places': Place.objects.all(),
	}
	return render(request, 'management/places.html', context)

@staff_required
def places_add(request):
	if request.method == 'POST':
		form = PlaceForm(request.POST)
		if form.is_valid():
			place = form.save()
			save_static_map(place)

			return redirect('management_places')
	else:
		form = PlaceForm()

	context = {
		'active_places': True,
		'form': form,
	}

	return render(request, 'management/places_add.html', context)

@staff_required
def places_edit(request, place_pk):
	place = get_object_or_404(Place, pk=place_pk)

	if request.method == 'POST':
		form = PlaceForm(request.POST, instance=place)
		if form.is_valid():
			place = form.save()
			save_static_map(place)

			return redirect('management_places')
	else:
		form = PlaceForm(instance=place)

	context = {
		'active_places': True,
		'form': form,
	}

	return render(request, 'management/places_add.html', context)

@staff_required
def places_delete(request, place_pk):
	place = get_object_or_404(Place, pk=place_pk)

	place.delete()

	return redirect('management_places')
