import warnings
warnings.filterwarnings("ignore")

import time
import datetime as dt
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.cluster import KMeans
from sklearn import datasets

eq_df = pd.read_csv('eq_database_place.csv')
dummy_eq = eq_df.copy()
dummy_pl = dummy_eq[dummy_eq['Place'].str.contains('IN')]
dummy_df = dummy_pl.copy()

def nan_helper(y):    
	return np.isnan(y), lambda z: z.nonzero()[0]

def label_integer_encoder(my_df, series_name):
	arr_name = np.array(list(my_df[str(series_name)]))
	label_arr_encoder = LabelEncoder()
	integer_arr_encoded = label_arr_encoder.fit_transform(arr_name)
	return integer_arr_encoded

def get_interpolation(my_df, nan_series):
	arr_series = np.array(my_df[str(nan_series)])
	nans, x = nan_helper(arr_series)
	arr_series[nans] = np.interp(x(nans), x(~nans), arr_series[~nans])
	return arr_series.round(2)

# dummy_df['Depth Error'] = get_interpolation(dummy_df, 'Depth Error')
# dummy_df['Depth Seismic Stations'] = get_interpolation(dummy_df, 'Depth Seismic Stations')
# dummy_df['Magnitude Error'] = get_interpolation(dummy_df, 'Magnitude Error')
# dummy_df['Magnitude Seismic Stations'] = get_interpolation(dummy_df, 'Magnitude Seismic Stations')
# dummy_df['Azimuthal Gap'] = get_interpolation(dummy_df, 'Azimuthal Gap')
# dummy_df['Horizontal Distance'] = get_interpolation(dummy_df, 'Horizontal Distance')
# dummy_df['Horizontal Error'] = get_interpolation(dummy_df, 'Horizontal Error')
# dummy_df['Root Mean Square'] = get_interpolation(dummy_df, 'Root Mean Square')

# dummy_df['Type'] = label_integer_encoder(dummy_df, 'Type')
# dummy_df['Magnitude Type'] = label_integer_encoder(dummy_df, 'Magnitude Type')
# dummy_df['Place'] = label_integer_encoder(dummy_df, 'Place')
# dummy_df['Status'] = label_integer_encoder(dummy_df, 'Status')

# dummy_df = dummy_df.drop(['ID', 'Source', 'Location Source', 'Magnitude Source'], axis=1)

# timestamp = []
# for d, t in zip(dummy_df['Date'], dummy_df['Time']):
# 	try:
# 		ts = dt.datetime.strptime(d + ' ' + t, '%m/%d/%Y %H:%M:%S')
# 		timestamp.append(time.mktime(ts.timetuple())) # inverse funtion of localtime
# 	except ValueError as e:
# 		timestamp.append('ValueError')
# time_s = pd.Series(timestamp)
# dummy_df['TimeStamp'] = time_s.values
# dummy_df = dummy_df.drop(['Date', 'Time'], axis=1)

def get_data_clusters(loc_df, num_clusters):
	clf_km = KMeans(n_clusters=num_clusters).fit(loc_df)
	unique_clusters = {i: np.where(clf_km.labels_ == i)[0] for i in range(clf_km.n_clusters)}
	return unique_clusters

def get_info_index(loc_df, main_df, num_clusters):
	quake_zones = get_data_clusters(loc_df, num_clusters)
	q_vals = main_df.values
	q_z = {}
	for i, j in quake_zones.items():
		z_lls = []
		for v in list(j):
			s_ll = (q_vals[v][0], q_vals[v][2], q_vals[v][3], q_vals[v][21], q_vals[v][8], q_vals[v][5])
			z_lls.append(s_ll)
		q_z[i] = z_lls
	return q_z

def segregation_llmd(r_list):
	daty = []; laty = []; lony = []; placy = []; magy = []; depthy = []
	for llmd in r_list:
		daty.append(llmd[0])
		laty.append(llmd[1])
		lony.append(llmd[2])
		placy.append(llmd[3])
		magy.append(llmd[4])
		depthy.append(llmd[5])
	return daty, laty, lony, placy, magy, depthy

def inside_place_wise(place_in):
	aplace_in = []
	for pi in place_in:
		fpi = pi.split(', ')
		aplace_in.append(fpi[0])

	cplace_in = {}
	uplace_in = list(set(aplace_in))
	for pi in uplace_in:
		cplace_in[pi] = aplace_in.count(pi)

	reverse_p = sorted(cplace_in.items(), key=lambda x : x[1], reverse=True)
	in_places = [str(pi[0]) + ' -- ' + str(pi[1]) for pi in reverse_p]
	in_places.insert(0, 'All')
	return in_places
