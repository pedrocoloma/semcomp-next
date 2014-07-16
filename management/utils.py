import math
import operator
import random
from StringIO import StringIO

from django.contrib.staticfiles.finders import find

from PIL import Image
import requests


def latlon_to_tiles(lat_deg, lon_deg, zoom):
	lat_rad = math.radians(lat_deg)
	n = 2.0 ** zoom
	xtile_float = (lon_deg + 180.0) / 360.0 * n
	ytile_float = (1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n

	return (xtile_float, ytile_float)

def ordered_offsets(x_frac, y_frac):
	x = 1 if x_frac > 0.5 else -1
	y = 1 if y_frac > 0.5 else -1

	offsets = [[0, 0], [x, y], [0, y], [x, 0]]
	return sorted(offsets, key=operator.itemgetter(0,1))

def get_neighboring_tiles(zoom, xtile_float, ytile_float):
	TILE_URL = 'http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

	x_frac, xtile = math.modf(xtile_float)
	y_frac, ytile = math.modf(ytile_float)

	xtile, ytile = map(int, (xtile, ytile))
	
	tiles = []
	for offset in ordered_offsets(x_frac, y_frac):
		x = xtile + offset[0]
		y = ytile + offset[1]

		url = TILE_URL.format(s=random.choice('abc'), z=zoom, x=x, y=y)
		response = requests.get(url)
		image = Image.open(StringIO(response.content))
		tiles.append(image)
	
	return tiles
		
def create_montage(tiles):
	montage = Image.new(mode='RGB', size=(256 * 2, 256 * 2))
	for i,offset in enumerate(ordered_offsets(1, 1)):
		montage.paste(tiles[i], (256 * offset[0], 256 * offset[1]))
	
	return montage

def crop_map_image(image, xtile_float, ytile_float):
	x_frac, xtile = math.modf(xtile_float)
	y_frac, ytile = math.modf(ytile_float)

	xtile, ytile = map(int, (xtile, ytile))

	x_center = x_frac + (0.0 if x_frac > 0.5 else 1.0)
	y_center = y_frac + (0.0 if y_frac > 0.5 else 1.0)

	x_center = int(x_center * 256.0)
	y_center = int(y_center * 256.0)

	return image.crop((
		x_center - 128,
		y_center - 128,
		x_center + 128,
		y_center + 128,
	))

def draw_marker(image, markerfile):
	marker = Image.open(markerfile)

	marker_width, marker_height = marker.size
	image_width, image_height = image.size

	x = (image_width / 2) - (marker_width / 2)
	y = (image_height / 2) - marker_height

	image.paste(marker, (x, y))

	return image

def get_static_map_image(lat, lon, zoom):
	xtile_float, ytile_float = latlon_to_tiles(lat, lon, zoom)
	tiles = get_neighboring_tiles(zoom, xtile_float, ytile_float)
	montage = create_montage(tiles)
	final_image = crop_map_image(montage, xtile_float, ytile_float)

	marker_path = find('img/maps/marker.png')

	return draw_marker(final_image, marker_path)

