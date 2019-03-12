import csv
import pandas as pd

radius_multiplier = {'inner' : 1.5, 'outer' : 3}

def occurence_based(occurence):

	'''
	Parameters : `occurence`
	Return : `list`
	'''

	eq_quake = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' + str(occurence) + '.csv')
	only_mags = eq_quake['mag'].tolist()
	# min_mag = min(only_mags)
	max_mag = max(only_mags)
	mag_list = list(range(1, (int(max_mag) + 1)))
	return mag_list

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

def center_location(some_df, r_name):

	'''
	This is used to locate the highest magnitude earthquake at the center
	Parameters : `some_df` -> earthquake DataFrame
	Return : `c_lat` & `c_lon` -> `tuple`
	'''

	if r_name == 'Worldwide':
		max_mag = max(some_df['mag'])
		center_details = some_df[some_df['mag'] == max_mag]
		c_lat = center_details['latitude'].tolist()
		c_lon = center_details['longitude'].tolist()
		return c_lat[0], c_lon[0]
	else:
		r_df = some_df[some_df['place'].str.contains(str(r_name))]
		max_mag = max(r_df['mag'])
		center_details = r_df[r_df['mag'] == max_mag]
		c_lat = center_details['latitude'].tolist()
		c_lon = center_details['longitude'].tolist()
		return c_lat[0], c_lon[0]

