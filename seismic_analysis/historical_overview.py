import pandas as pd
import csv
import datetime as dt
from countries_list import earth_countries

def collect_country_wise(earth_quake_df, country_code):

	'''
	This segregates the data based on the place country name
	Parameters : `earth_quake_df` pandas DataFrame
							 `country_code` --> `US`, `JP` ...
	Return : `pandas DataFrame`
	'''

	fields = list(earth_quake_df.columns)
	country_wise = [fields]
	earth_vals = earth_quake_df.values

	for each in range(len(earth_quake_df)):
		unique_place = earth_quake_df['Place'][each].split(', ')
		if len(unique_place) == 2:
			if country_code == unique_place[1]:
				country_wise.append(list(earth_vals[each]))

	with open(str(country_code) + '.csv', 'w') as ccode:
		writer = csv.writer(ccode)
		writer.writerows(country_wise)

	country_data = pd.read_csv(str(country_code) + '.csv')
	return country_data

def get_unique_region_code(earth_quake_df):

	'''
	Only gets the region code
	Paramters : `earth_quake_df` pandas DataFrame
	Return : `list`
	'''

	place = earth_quake_df['Place'].tolist()
	# print(len(place)) # 23412
	specific_place = list(set(place))
	# print(len(specific_place)) # 3068
	regions_code = []
	for nc in specific_place:
		naco = nc.split(', ')
		if len(naco) == 2:
			regions_code.append(naco[1])

	specific_regions_code = list(set(regions_code))
	return specific_regions_code

def get_country_name(earth_quake_df):
	
	'''
	Gets the country name given the region code `JP` ...
	Parameters : `earth_quake_df` pandas DataFrame
	Return : `Dictionary`
	'''

	prone_countries = {}
	prone_regions = get_unique_region_code(earth_quake_df)

	for rc in prone_regions:
		for i, j in earth_countries.items():
			if j == rc:
				prone_countries[i] = rc

	return prone_countries

eq_data_df = pd.read_csv('eq_database_place.csv')
select_countries = get_country_name(eq_data_df)

# import numpy as np
# import math
# japan = eq_data_df[eq_data_df['Place'].str.contains('JP')]
# japan.dropna(1)

# jp_seismic = japan[['Date', 'Time', 'Latitude', 'Longitude', 'Place', 'Type', 'Depth', 'Magnitude', 'Magnitude Type', 'Root Mean Square']]

# rms = japan['Root Mean Square'].tolist()
# non_nan_rms = [i for i in rms if math.isnan(i) == False]
# print(len(jp_seismic))