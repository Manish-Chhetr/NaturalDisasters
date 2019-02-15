import json
import urllib2
import pandas as pd

def reverse_geocoding(lat, lon):

	'''
	This is used to get the location, Reverse GeoCoding
	Parameters : `lat` Latitude
							 `lon` Longitude
	Return : `Location name` `Bangalore, IN`
	'''

	key = '9d41bd4e5bffd04e03a6cb6832066559'
	url = 'http://api.openweathermap.org/data/2.5/weather?lat=' + str(lat) + '&lon=' + str(lon) + '&appid=' + str(key)

	open_url = urllib2.urlopen(url)
	details = json.load(open_url)

	if details['name'] == '': return 'Unknown'
	else:
		name = details['name']
		country = details['sys']['country']
		expected_name = name + ', ' + country
		return expected_name
