import csv
import base64
import pandas as pd
import datetime as dt

from realtime_details import (extract_places_regions, radius_multiplier)

logo_image = 'cartoon-globe.png'
en_logo = base64.b64encode(open(logo_image, 'rb').read())

entire_month = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv')

def extract_month_values():

	'''
	Takes the entire data in a list -> [ [], [], [] ]
	Parameters : `None`
	Return : `list`
	'''

	all_month = entire_month.copy()
	time = pd.to_datetime(all_month['time'])
	all_month['time'] = time
	fields = [field for field in all_month]
	month_values = all_month.values
	return fields, month_values

def csv_feature_extraction(year, month, day):

	'''
	Considers the data which only meet the criteria, year, month, value
	Parameters : `year`, `month`, `day`
	Return : `list`
	'''

	fields, month_values = extract_month_values()
	extraction = [fields]
	for vals in month_values:
		if vals[0].year == year and vals[0].month == month and vals[0].day == day:
			if vals[4] >= 4.5: # magnitude > 1
				extraction.append(vals)
	return extraction

def day_wise_extraction(year, month, day):

	'''
	Writes the data which is selected as per the input into a CSV file.
	Parameters : `year`, `month`, `day`
	Return : `pandas DataFrame`
	'''
	
	extraction = csv_feature_extraction(year, month, day)
	with open('month_day.csv', 'w') as extract:
		writer = csv.writer(extract)
		writer.writerows(extraction)

def get_dates_sorted():

	'''
	Sort the dates
	Parameters : `None`
	Return : `list`
	'''

	_, month_values = extract_month_values()
	all_dates = []
	for each_date in month_values:
		all_dates.append(str(each_date[0].date()))
	timestamps = sorted(list(set(all_dates)))
	return timestamps

timestamps = get_dates_sorted()
date_start = dt.datetime.strptime(timestamps[0], '%Y-%m-%d')
date_end = dt.datetime.strptime(timestamps[len(timestamps)-1], '%Y-%m-%d')

def place_wise_extraction(place_name):

	'''
	This function is useful for plotting as per the place name chosen.
	Parameters : `place_name` --> Alaska, Japan ...
	Return : `pandas DataFrame`
	'''

	all_month = entire_month.copy()
	all_places = all_month['place'].tolist()
	u_regions, _, _ = extract_places_regions(all_places) # specific last name
	if place_name in u_regions:
		entire_place = all_month[all_month['place'].str.contains(place_name)]
		return entire_place
	else:
		entire_world = all_month[all_month['mag'] > 1]
		return entire_world

def history_eq(eq_some, zoom_value):

	'''
	This function basically reduces redundancy.
	Parameters : `eq_some`, `zoom_value`
	Return : `tuple`
	'''

	lats = eq_some['latitude'].tolist()
	lons = eq_some['longitude'].tolist()
	places = eq_some['place'].tolist()
	mags = ['Magnitude : ' + str(i) for i in eq_some['mag']]
	mag_size = [float(i) * radius_multiplier['outer'] for i in eq_some['mag']]
	depths = ['Depth : ' + str(i) for i in eq_some['depth']]
	info = [places[i] + '<br>' + mags[i] + '<br>' + depths[i] for i in range(len(places))]
	zooming = zoom_value
	return lats, lons, places, mags, mag_size, depths, info, zooming

