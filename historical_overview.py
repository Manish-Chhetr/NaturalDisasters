import pandas as pd
import csv
import datetime as dt
import plotly.graph_objs as go

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

d_eq_df = eq_data_df.copy()
d_eq_df['Date'] = pd.to_datetime(d_eq_df['Date'])

def get_years_based_r(e_region):

	'''
	Parameter : `e_region` --> `str`
	Return : `list`
	'''

	r_data = d_eq_df[d_eq_df['Place'].str.contains(str(e_region))]
	u_r_years = list(set([date.year for date in r_data['Date']]))
	u_r_years.reverse()
	u_r_years.insert(0, 'All')
	return u_r_years

def data_y_r_based(e_region, e_year):

	'''
	Parameter : `e_region` --> `str`
							`e_year` --> `int`
	Return : `pandas DataFrame`
	'''

	r_data = d_eq_df[d_eq_df['Place'].str.contains(str(e_region))]
	r_d_vals = r_data.values

	y_r_data = [list(r_data.columns)]
	for row in r_d_vals:
		if row[0].year == e_year:
			y_r_data.append(list(row))

	with open('region_year_history.csv', 'w') as ryh:
		writer = csv.writer(ryh)
		writer.writerows(y_r_data)

	yrdata = pd.read_csv('region_year_history.csv')
	return yrdata

def show_histogram():

	'''
	Parameter : `None`
	Return : `Dictionary`
	'''

	mags = d_eq_df['Magnitude'].tolist()
	data = [go.Histogram(x=mags, nbinsx=10)]
	layout = go.Layout(
		xaxis=dict(title='Magnitude'),
		yaxis=dict(title='Count'),
		height=600
	)
	return {'data' : data, 'layout' : layout}

def show_boxplot():

	'''
	Parameter : `None`
	Return : `Dictionary`
	'''

	mags = d_eq_df['Magnitude'].tolist()
	data = [go.Box(y=mags, name='Magnitude')]
	layout = go.Layout(height=600)
	return {'data' : data, 'layout' : layout}

def year_wise_frequency():

	'''
	Parameter : `None`
	Return : `Dictionary`
	'''

	d_eq_df['Year'] = d_eq_df['Date'].dt.year
	year_occurence = d_eq_df.groupby('Year').groups
	years = [i for i in range(1965, 2017)]

	occurence = []
	for i in range(len(years)):
		val = year_occurence[years[i]]
		occurence.append(len(val))

	traces = []
	traces.append(
		go.Scatter(
			x=years,
			y=occurence,
			mode='lines+markers'
		)
	)
	layout = go.Layout(
		xaxis=dict(title='Year'),
		yaxis=dict(title='Frequency'),
		height=600
	)
	return {'data' : traces, 'layout' : layout}

#################################################################################
