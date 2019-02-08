import csv
import pandas as pd
import geopandas as gpd
import dash_html_components as html

def seismic_reporting_data(occurence):
	'''
	Seismic Reporting Function
	Collects the additional features of the disaster like 'Tsunami Alerts', 'Danger Alerts'
	Depends on the occurence type that is being chosen

	Parameter : `occurence`
	Return : `pandas DataFrame`
	'''
	# geojson file reading
	eq_geojson = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' + str(occurence) +'.geojson'
	eq_geodata = gpd.read_file(eq_geojson)

	# conversion of geojson to pandas dataframe
	eq_geocsv = pd.DataFrame(eq_geodata)
	# take longitude geometric value
	longitude = eq_geodata['geometry'].x.tolist()
	# take latitude geometric value
	latitude = eq_geodata['geometry'].y.tolist()
	eq_geocsv['latitude'] = latitude
	eq_geocsv['longitude'] = longitude

	eq_geocsv.to_csv('additional_geojson.csv')
	data_quake = pd.read_csv('additional_geojson.csv', index_col=0)

	return data_quake

def get_all_felts(occurence, mag_value, region_name):
	'''
	Felt Reports
	Parameter : `occurence`, `mag_value`, `region_name`
	Return : `list - [ (), (), () ]`
	'''
	data_quakes = seismic_reporting_data(occurence)
	felt_specific = data_quakes[['title', 'mag', 'felt']]
	felt_specific = felt_specific[felt_specific['mag'] > mag_value]
	felt_specific.dropna(inplace=True)
	felt_specific = felt_specific.sort_values(by='felt', ascending=False)
	title_felt = list(zip(felt_specific['title'], felt_specific['felt']))
	region_felt = [regionf for regionf in title_felt if region_name in regionf[0]]
	if region_name == 'World Wide': return title_felt
	else: return region_felt

def get_all_alerts(occurence, mag_value, region_name):
	'''
	Alert Reports
	Parameter : `occurence`, `mag_value`, `region_name`
	Return : `list - [ (), (), () ]`
	'''
	data_quakes = seismic_reporting_data(occurence)
	alert_specific = data_quakes[['title', 'mag', 'alert']]
	alert_specific = alert_specific[alert_specific['mag'] > mag_value]
	alert_specific.dropna(inplace=True)
	alert_specific = alert_specific.sort_values(by='alert', ascending=False)
	title_alert = list(zip(alert_specific['title'], alert_specific['alert']))
	region_alert = [regiona for regiona in title_alert if region_name in regiona[0]]
	if region_name == 'World Wide': return title_alert
	else: return region_alert

def get_all_tsunamis(occurence, mag_value, region_name):
	'''
	Tsunami Reports
	Parameter : `occurence`, `mag_value`, `region_name`
	Return : `list - [ (), (), () ]`
	'''
	data_quakes = seismic_reporting_data(occurence)
	tsunami_specific = data_quakes[['title', 'mag', 'tsunami']]
	tsunami_specific = tsunami_specific[tsunami_specific['mag'] > mag_value]
	tsunami_event = tsunami_specific[tsunami_specific['tsunami'] > 0]
	tsunami_event = tsunami_event.sort_values(by='mag', ascending=False)
	title_tsunami = list(zip(tsunami_event['title'], tsunami_event['tsunami']))
	region_tsunami = [regiont for regiont in title_tsunami if region_name in regiont[0]]
	if region_name == 'World Wide': return title_tsunami
	else: return region_tsunami

def make_seismic_report(report_list, loc_color, report_color):
	'''
	Displaying Seismic Report (people felt and tsunami report)
	Parameter : `report_list` from any of the get_ functions
							`loc_color` location color
							`report_color` report color
	Return : `html.Div([])` list
	'''
	report_content = []
	for trs in report_list:
		report_content.append(
			html.Div([
				html.P('Location: ' + str(trs[0]), style={'color' : str(loc_color)}),
				html.P('Report found: ' + str(trs[1]), style={'color' : str(report_color)}),
				html.P('-'*25)
			])
		)

	if len(report_content) == 0:
		return html.Div([
			html.P('Everything seems clear...', 
				style={'textAlign' : 'center', 'margin-top' : 40, 'margin-bottom' : 40})
		])
	else:	return report_content

def make_alert_report(report_list):
	'''
	Displaying only Alert Color Report
	Parameter : `report_list` from any of the get_ functions
	Return : `html.Div([])` list
	'''
	alert_colors = {'green' : '#018014', 'yellow' : '#f1c40f', 'orange' : '#f39c12', 'red' : '#de1a0a'}
	report_content = []
	for colr in alert_colors:
		for trs in report_list:
			if trs[1] == colr:
				report_content.append(
					html.Div([
						html.P(str(trs[0]), style={'color' : alert_colors[colr]}),
						html.P('-'*25)
					])
				)

	if len(report_content) == 0:
		return html.Div([
			html.P('Everything seems clear...', 
				style={'textAlign' : 'center', 'margin-top' : 40, 'margin-bottom' : 40})
		])
	else:	return report_content


