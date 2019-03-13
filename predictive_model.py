import warnings
warnings.filterwarnings("ignore")

import time
import datetime as dt
import numpy as np
import pandas as pd

from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn import linear_model
from sklearn.metrics import accuracy_score

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

def random_forest_regressor(train_X, train_y, test_X, test_y):
	reg = RandomForestRegressor()
	reg.fit(train_X, train_y)
	preds = reg.predict(test_X)
	accuracy = reg.score(test_X, test_y)
	return reg, preds, accuracy

def grid_search_cv(train_X, train_y, test_X, test_y):
	parameters = {'n_estimators' : [13, 18, 43, 77, 45, 450]}
	reg, _, _ = random_forest_regressor(train_X, train_y, test_X, test_y)
	gs = GridSearchCV(reg, parameters)
	grid_fit = gs.fit(train_X, train_y)
	best_fit = grid_fit.best_estimator_
	gs_preds = best_fit.predict(test_X)
	gs_accuracy = best_fit.score(test_X, test_y)
	return gs_preds, gs_accuracy

