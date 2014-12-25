from os import walk
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS
import math
import json

places = {
	'Kazan' 		: [55.798010, 49.105575],
 	'Yekaterinburg' : [56.836998, 60.604122],
 	'Czech'		    : [50.063763, 14.483625],
 	'Italy' 		: [44.415561, 12.186862]
}

colors = {
	'Kazan' 		: 'red',
 	'Yekaterinburg' : 'blue',
 	'Czech'		    : 'green',
 	'Italy' 		: 'azure'
}

def extract_image_data(file_name, storage):
	ret = {}

	i = Image.open(file_name)
	info = i._getexif()

	if (info != None):
		for tag,value in info.items():
			decoded = TAGS.get(tag, tag)
			ret[decoded] = value

		if ret.has_key('GPSInfo') and ret.has_key('DateTime'):
			Nsec = ret['GPSInfo'][2][2][0] / float(ret['GPSInfo'][2][2][1])
			Nmin = ret['GPSInfo'][2][1][0] / float(ret['GPSInfo'][2][1][1])
			Ndeg = ret['GPSInfo'][2][0][0] / float(ret['GPSInfo'][2][0][1])
			Wsec = ret['GPSInfo'][4][2][0] / float(ret['GPSInfo'][4][2][1])
			Wmin = ret['GPSInfo'][4][1][0] / float(ret['GPSInfo'][4][1][1])
			Wdeg = ret['GPSInfo'][4][0][0] / float(ret['GPSInfo'][4][0][1])

			if ret['GPSInfo'][1] == 'N':
				Nmult = 1
			else:
				Nmult = -1

			if ret['GPSInfo'][1] == 'E':
				Wmult = 1
			else:
				Wmult = -1

			Lat = Nmult * (Ndeg + (Nmin + Nsec/60.0)/60.0)
			Lng = Wmult * (Wdeg + (Wmin + Wsec/60.0)/60.0)

			storage[file_name] = {}
			storage[file_name]['coordinates'] = [Lat, Lng]
			storage[file_name]['date'] = ret['DateTime']
		else:
			print('Wrong file: ' + file_name)
	else:
		print('Wrong file: ' + file_name)

def distance(point1, point2):
	R = 6371

	dLat = ((point1[0] - point2[0]) * math.pi / 180)
	dLon = ((point1[1] - point2[1]) * math.pi / 180)

	a = math.sin(dLat/2) * math.sin(dLat/2) + math.cos(point2[0] * math.pi/180) * math.cos(point1[0] * math.pi/180) * math.sin(dLon/2) ** 2
	c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

	return c * R

def process():
	global places
	storage = {}

	for (dir_path, dir_names, file_names) in walk('.'):
	    for file_name in file_names:
			if file_name.lower().endswith('.jpg'):
				extract_image_data(file_name, storage)

	for image in storage.keys():
		coordinates = storage[image]['coordinates']
		storage[image]['color'] = colors['Kazan']

		min_distance = distance(coordinates, places['Kazan'])

		for place in places.keys():
			if (distance(coordinates, places[place]) < min_distance):
				storage[image]['color'] = colors[place]
				min_distance = distance(coordinates, places[place])

	return json.dumps(storage)
