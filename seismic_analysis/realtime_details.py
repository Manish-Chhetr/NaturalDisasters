import csv
import pandas as pd

measuring_mags = [1.0, 2.0, 3.0, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 8.0]
radius_multiplier = {'inner' : 1.5, 'outer' : 3}

def grab_appropriate_data(occurence, mag_value):

	'''
	Grab the appropriate data as per the `occurence` and `mag above` selected.
	Parameters : `occurence`, `mag_value`
	Return : `pandas DataFrame`
	'''

	quake_data = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' + str(occurence) + '.csv')
	appropriate_data = quake_data[quake_data['mag'] > mag_value]
	return appropriate_data

def extract_places_regions(eq_places):

	'''
	This extracts only the region -> "New Zealand" name from the place name -> "172km ESE of Raoul Island, New Zealand".
	Parameters : `eq_places` -> a list
	Return : `tuple`
	'''

	# taking only last name from each place
	end_names = []
	for p in eq_places:
		fplp = p.split(', ')
		if len(fplp) == 2:
			end_names.append(fplp[1])
		if len(fplp) == 1:
			end_names.append(fplp[0])

	counter_places = {}
	splaces = list(set(end_names))
	for entry in splaces:
		counter_places[entry] = end_names.count(entry)

	regions = list(counter_places.keys())
	region_counts = list(counter_places.values())

	return splaces, regions, region_counts
