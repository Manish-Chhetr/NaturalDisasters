import time
import pandas as pd
import datetime as dt
import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as  html
import plotly.graph_objs as go
from dash.dependencies import (Input, Output, Event)

from earthquakes_mapping import (MapScatter, MapLayout)

from design_layout import (index_page, realtime_tracking_layout, earth_history_layout, colors_useful)
from realtime_details import (occurence_based, grab_appropriate_data, extract_places_regions, radius_multiplier, center_location)
from report_alerts import (seismic_reporting_data, get_all_felts, get_all_tsunamis, get_all_alerts, make_seismic_report, make_alert_report)
from historical_overview import (get_years_based_r, data_y_r_based)
from quake_means import (get_info_index, segregation_llmd, inside_place_wise)

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True

cs_mag = [
	[0, '#a303b9'],	[0.25, '#ea6402'],[0.5, '#fa73a0'],	
	[0.75, '#f03b20'], [1, '#bd0026'],
]

app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content')
])

################################# realtime tracking callbacks ############################
############# update magnitude options ###########
@app.callback(Output('magnitude-drop', 'options'), [Input('occurence_type', 'value')],
	events=[Event('live-update', 'interval')])
def show_mag_options(occurence_type):
	mag_list = occurence_based(occurence_type)
	mag_list.reverse()
	return [{'label' : m, 'value' : m} for m in mag_list]
##################################################

######## update the state regions options ########
@app.callback(
	Output('region-options', 'options'),
	[Input('occurence_type', 'value'),	Input('magnitude-drop', 'value')],
	events=[Event('live-update', 'interval')]
)
def grab_region_options(occurence_type, mag_value):
	eq = grab_appropriate_data(occurence_type, mag_value)
	places = eq['place'].tolist()
	_, regions, _ = extract_places_regions(places)
	regions.insert(0, 'World Wide')
	return [{'label' : s, 'value' : s} for s in regions]
##################################################

############# plot earthquakes ###################
@app.callback(
	Output('map-output', 'children'),
	[Input('occurence_type', 'value'), Input('magnitude-drop', 'value'), 
		Input('region-options', 'value')],
	events=[Event('live-update', 'interval')]
)
def plot_earthquakes(occurence_type, mag_value, region_options):
	try:
		eq = grab_appropriate_data(occurence_type, mag_value)
		c_lat, c_lon = center_location(eq, region_options)

		latitudes = eq['latitude'].tolist()
		longitudes = eq['longitude'].tolist()
		places = eq['place'].tolist()
		mags = eq['mag'].tolist()
		depths = eq['depth'].tolist()

		mag_info = ['Magnitude: ' + str(i) for i in mags]
		mag_size = [float(i) * radius_multiplier['outer'] for i in mags]
		depth_info = ['Depth: ' + str(i) for i in depths]

		_, eplaces, _ = extract_places_regions(places)
		seperate = []
		for p in range(len(places)):
			# split into, first name and last name: "122km SSE Name, Iran" --> ["122km SSE Name", "Iran"]
			seperate.append([places[p].split(', '), latitudes[p], longitudes[p], 
				mag_info[p], mag_size[p], depth_info[p]])

		state_regions = {}
		for p in eplaces:
			regions = []	
			for sep in seperate:
				locr = sep[0]
				if len(locr) == 2:
					if locr[1] == p:
						regions.append([str(locr[0])+', '+str(p), sep[1], sep[2], 
							sep[3], sep[4], sep[5]])
				if len(locr) != 2:
					if locr[0] == p:
						regions.append([locr[0], sep[1], sep[2], 
							sep[3], sep[4], sep[5]])
			state_regions[p] = regions
		state_regions['World Wide'] = []

		mi = []; ms = []; di = []; lats = []; lons = []
		region_names = []
		for k, v in state_regions.items():
			if k == region_options:
				zoom_value = 3
				details = v
				for about in details:
					region_names.append(about[0])
					lats.append(about[1])
					lons.append(about[2])
					mi.append(about[3])
					ms.append(about[4])
					di.append(about[5])
		if region_options == 'World Wide':
			zoom_value = 1
			for k, v in state_regions.items():
				details = v
				for about in details:
					region_names.append(about[0])
					lats.append(about[1])
					lons.append(about[2])
					mi.append(about[3])
					ms.append(about[4])
					di.append(about[5])

		info = [region_names[i] + '<br>' + mi[i] + '<br>' + di[i] for i in range(len(region_names))]

		quakes = [MapScatter(lats, lons, ms, ms, cs_mag, info)]
		layout = MapLayout(700, 30, 10, 30, 40, c_lat, c_lon, zoom_value)

		map_deisgn = html.Div([
			dcc.Graph(
				id='map-earthquake',
				figure={'data' : quakes, 'layout' : layout},
				config={'displayModeBar' : False}
			)
		])
		return map_deisgn

	except Exception as e:
		return html.Div([
			html.H4('Could not load the map for the input selected.'),
			html.H3('Please select valid Magnitude / Region ...'),
			# html.P(str(e))
		], style={'margin-top' : 200, 'margin-bottom' : 200, 'textAlign' : 'center'})
##################################################

##### update region dropdown clicked on map ######
@app.callback(
	Output('region-options', 'value'), [Input('map-earthquake', 'clickData')]
)
def update_region_click(selection):
	if selection is not None:
		info_text = selection['points'][0]
		place_name = info_text['text'].split('<br>')
		split_place = place_name[0].split(', ')
		if len(split_place) == 2:
			region_n = split_place[1]
		elif len(split_place) != 2:
			region_n = split_place[0]
		return str(region_n)
##################################################

############# display seismic report #############
@app.callback(
	Output('people-reports', 'children'), 
	[Input('occurence_type', 'value'), Input('magnitude-drop', 'value'), 
		Input('region-options', 'value')],
	events=[Event('live-update', 'interval')]
)
def display_people_reports(occurence_type, mag_value, region_options):
	try:
		report_list = get_all_felts(occurence_type, mag_value, region_options)
		make_report = make_seismic_report(report_list, colors_useful['loc_color'], colors_useful['report_color'])
		return make_report
	except TypeError as e:
		return html.Div([
			html.P('Please select the region...', 
				style={'margin-top' : 40, 'margin-bottom' : 40, 'textAlign' : 'center'})
		])

@app.callback(
	Output('alert-reports', 'children'), 
	[Input('occurence_type', 'value'), Input('magnitude-drop', 'value'),
		Input('region-options', 'value')],
	events=[Event('live-update', 'interval')]
)
def display_alert_reports(occurence_type, mag_value, region_options):
	try:
		report_list = get_all_alerts(occurence_type, mag_value, region_options)
		make_report = make_alert_report(report_list)
		return make_report
	except TypeError as e:
		return html.Div([
			html.P('Please select the region...', 
				style={'margin-top' : 40, 'margin-bottom' : 40, 'textAlign' : 'center'})
		])

@app.callback(
	Output('tsunami-reports', 'children'), 
	[Input('occurence_type', 'value'), Input('magnitude-drop', 'value'), 
		Input('region-options', 'value')],
	events=[Event('live-update', 'interval')]
)
def display_tsunami_reports(occurence_type, mag_value, region_options):
	try:
		report_list = get_all_tsunamis(occurence_type, mag_value, region_options)
		make_report = make_seismic_report(report_list, colors_useful['tsunami_color'], colors_useful['tsunami_color'])
		return make_report
	except TypeError as e:
		return html.Div([
			html.P('Please select the region...', 
				style={'margin-top' : 40, 'margin-bottom' : 40, 'textAlign' : 'center'})
		])
##################################################

############# display the highest mag ############
@app.callback(
	Output('highest-mag', 'children'),
	[Input('occurence_type', 'value'), Input('magnitude-drop', 'value'),
		Input('region-options', 'value')],
	events=[Event('live-update', 'interval')]
)
def display_highest_mag(occurence_type, mag_value, region_options):
	eq = grab_appropriate_data(occurence_type, mag_value)
	threshold_mag = 5.0
	try:
		if region_options == 'World Wide':
			world_df = eq
			world_hm_mags = world_df['mag'].tolist()
			world_max_mag = max(world_hm_mags)
			world_places = world_df['place'].tolist()

			for wp in range(len(world_places)):
				if world_hm_mags[wp] == world_max_mag:
					world_hm_place = world_places[wp]

			if world_max_mag >= threshold_mag:
				wc_display = colors_useful['danger']
			else:
				wc_display = colors_useful['text_color']

			return html.Div([html.H2('M ' + str(world_max_mag) + ' -- ' + str((world_hm_place)))
			], style={'textAlign' : 'center', 'color' : wc_display, 'margin-left' : 30, 'margin-right' : 30})

		else:
			region_df = eq[eq['place'].str.contains(str(region_options))]
			region_hm_mags = region_df['mag'].tolist()
			region_max_mag = max(region_hm_mags)
			region_places = region_df['place'].tolist()

			for rp in range(len(region_places)):
				if region_hm_mags[rp] == region_max_mag:
					region_hm_place = region_places[rp]

			if region_max_mag >= threshold_mag:
				rc_display = colors_useful['danger']
			else:
				rc_display = colors_useful['text_color']

			return html.Div([html.H2('M ' + str(region_max_mag) + ' -- ' + str((region_hm_place)))
			], style={'textAlign' : 'center', 'color' : rc_display, 'margin-left' : 30, 'margin-right' : 30})
	except ValueError as e:
		return ''
##################################################

############# bar chart - update #################
def bar_chart_colouring(mags):
	min_mag = min(mags)
	threshold_mag = 5.0
	bar_highlight = []
	for m in mags:
		if m >= threshold_mag:
			bar_highlight.append(colors_useful['bar_max_val'])
		elif m == min_mag:
			bar_highlight.append(colors_useful['bar_min_val'])
		else:
			bar_highlight.append(colors_useful['bar_normal'])
	return bar_highlight

@app.callback(
	Output('mag-bar', 'children'),
	[Input('occurence_type', 'value'), Input('magnitude-drop' , 'value'), 
		Input('region-options', 'value')],
	events=[Event('live-update', 'interval')]
)
def mag_bar_diagram(occurence_type, mag_value, region_options):
	try:
		eq = grab_appropriate_data(occurence_type, mag_value)
		places = eq['place'].tolist()
		mags = eq['mag'].tolist()
		depths = eq['depth'].tolist()

		_, eplaces, _ = extract_places_regions(places)

		seperate = []
		for p in range(len(places)):
			seperate.append([places[p].split(', '), mags[p], depths[p]])

		state_regions = {}
		for p in eplaces:
			regions = []	
			for sep in seperate:
				locr = sep[0]
				if len(locr) == 2:
					if locr[1] == p:
						regions.append([str(locr[0])+', '+str(p), sep[1], sep[2]])
				if len(locr) != 2:
					if locr[0] == p:
						regions.append([locr[0], sep[1], sep[2]])
			state_regions[p] = regions
		state_regions['World Wide'] = []

		region_places = list(state_regions.keys())
		region_places.remove('World Wide')

		traces = []; bar_region = []
		bar_mag = []; bar_depth = []
		if region_options in region_places:
			for k, v in state_regions.items():
				if k == region_options:
					details = v
					for about in details:
						bar_region.append(about[0])
						bar_mag.append(about[1])
						bar_depth.append(about[2])
			traces.append(
				go.Histogram2dContour(
					x=bar_mag, y=bar_depth,
					name='Region Magnitude',
					colorscale='Viridis'
				)
			)
			layout = go.Layout(height=600, title=str(region_options))
			bar_state_region = html.Div([
				dcc.Graph(id='state-region-bar', figure={'data' : traces, 'layout' : layout})
			])
			return bar_state_region

		elif region_options == 'World Wide':
			for k, v in state_regions.items():
				details = v
				for about in details:
					bar_region.append(about[0])
					bar_mag.append(about[1])
			bar_highlight = bar_chart_colouring(bar_mag)
			traces.append(
				go.Bar(
					x=bar_region, y=bar_mag,
					name='Region Magnitude',
					marker=dict(color=bar_highlight)
				)
			)
			layout = go.Layout(title=str(region_options))
			bar_worldwide = html.Div([
				dcc.Graph(id='bar-worldwide', figure={'data' : traces, 'layout' : layout})
			])
			return bar_worldwide

	except Exception as e:
		return html.Div([
			html.H4('Network issues, try refreshing the page...')
		], style={'textAlign' : 'center', 'margin-top' : 150})

##################################################

########## mag depth relationship ################
@app.callback(
	Output('mag-depth-relation', 'children'),	[Input('occurence_type', 'value')]
)
def mag_depth_relation_line(occurence_type):
	eq = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' + str(occurence_type) + '.csv')
	mags = eq['mag'].tolist()
	depths = eq['depth'].tolist()
	# beta_, alpha_ = np.polyfit(mags, depths, 1)
	# fit_line = [((beta_ * d) + alpha_) for d in depths]
	traces = [
		go.Scatter(
			x=mags,
			y=depths,
			mode='markers'
		),
		# go.Scatter(x=mags, y=fit_line, mode='lines')
	]
	layout = go.Layout(
		xaxis=dict(title='Magnitude'),
		yaxis=dict(title='Depth')
	)
	relation = html.Div([
		dcc.Graph(id='relation-graph', figure={'data' : traces, 'layout' : layout})
	])
	return relation
##################################################

############# pie chart - update #################
@app.callback(
	Output('region-pie', 'children'),
	[Input('occurence_type' , 'value'), Input('magnitude-drop', 'value')],
	events=[Event('live-update', 'interval')]
)
def pie_region_diagram(occurence_type, mag_value):
	try:
		eq = grab_appropriate_data(occurence_type, mag_value)
		places = eq['place'].tolist()
		_, regions, region_counts = extract_places_regions(places)
		traces = []
		traces.append(
			go.Pie(labels=regions, values=region_counts, pull=.05)
		)
		layout = go.Layout(title='World Wide')
		pie_chart = html.Div([
			dcc.Graph(id='pie-graph',	figure={'data' : traces, 'layout' : layout})
		])
		return pie_chart

	except Exception as e:
		return html.Div([
			html.H4('Network issues, try refreshing the page...')
		], style={'textAlign' : 'center', 'margin-top' : 150})
##################################################
################################# realtime tracking callbacks ############################

################################# earthquake history ############################

earth_quake_df = pd.read_csv('eq_database_place.csv') # for earthquake_history

############## place year options ################
@app.callback(
	Output('history-year-dropdown', 'options'), [Input('countries-dropdown', 'value')]
)
def show_year_options(country_name):
	region_years = get_years_based_r(country_name)
	return [{'label' : y, 'value' : y} for y in region_years]

@app.callback(
	Output('history-year-dropdown', 'value'), [Input('history-year-dropdown', 'options')]
)
def choose_all(year_options):
	return year_options[0]['value']
##################################################

############## country wise map plot #############
@app.callback(
	Output('history-map', 'children'), 
	[Input('countries-dropdown', 'value'), Input('history-year-dropdown', 'value')]
)
def show_ancient_cw(country_name, occ_year):
	if occ_year == 'All':
		country_wise_df = earth_quake_df[earth_quake_df['Place'].str.contains(str(country_name))]
		zoom_value = 3
	else:	
		country_wise_df = data_y_r_based(country_name, occ_year)
		zoom_value = 3.5

	lats = country_wise_df['Latitude'].tolist()
	lons = country_wise_df['Longitude'].tolist()
	mags = country_wise_df['Magnitude'].tolist()
	deps = country_wise_df['Depth'].tolist()
	places = country_wise_df['Place'].tolist()
	dates = country_wise_df['Date'].tolist()
	ms = [float(i) * radius_multiplier['outer'] for i in mags]

	info = ['Date: ' + str(dates[i]) + '<br>' + 'Place: ' + places[i] + '<br>' + 'Magnitude: ' + str(mags[i]) + '<br>' + 'Depth: ' + str(deps[i]) for i in range(len(places))]

	quakes = [MapScatter(lats, lons, 10, ms, cs_mag, info)]
	layout = MapLayout(700, 10, 10, 20, 20, lats[0], lons[0], zoom_value)

	country_map = html.Div([
		dcc.Graph(
			id='country-result', 
			figure={'data' : quakes, 'layout' : layout},
			config={'displayModeBar' : False}
		)
	])
	return country_map
##################################################
################################# earthquake history ############################

################################# predictive model ##############################
############### update place inside ##############
@app.callback(
	Output('place-inside', 'options'), [Input('country-means', 'value')]
)
def update_inside_places(country_name):
	country_wise_df = earth_quake_df[earth_quake_df['Place'].str.contains(str(country_name))]
	cplaces = country_wise_df['Place'].tolist()
	place_inoptions = inside_place_wise(cplaces)
	return [{'label' : pi, 'value' : pi.split(' -- ')[0]} for pi in place_inoptions]

@app.callback(
	Output('place-inside', 'value'), [Input('place-inside', 'options')]
)
def choose_all_placein(placein_options):
	return placein_options[0]['value']
##################################################

############### k means clustering ###############
@app.callback(
	Output('quake-means-map', 'children'),
	[Input('country-means', 'value'), Input('place-inside', 'value')]
)
def cluster_qmeans_placein(country_name, placein_name):
	dummy_eq = earth_quake_df.copy()
	dummy_pl = dummy_eq[dummy_eq['Place'].str.contains(str(country_name))]
	dummy_df = dummy_pl.copy()
	dummy_df = dummy_df.drop(['ID', 'Source', 'Location Source', 'Magnitude Source'], axis=1)
	qmeans_pin = []; clat = 0; clon = 0

	try:
		if placein_name == 'All':
			clat = dummy_df['Latitude'].tolist()[0]
			clon = dummy_df['Longitude'].tolist()[0]
			zoom_value = 3
			location_df = dummy_df[['Latitude', 'Longitude']]
			q_zones = get_info_index(location_df, dummy_pl, 4)

			for i, j in q_zones.items():
				daty, laty, lony, placy, magy, depthy = segregation_llmd(j)
				cluster_info = ['Date: ' + str(daty[k]) + '<br>' + 'Place: ' + placy[k] + '<br>' + 'Magnitude: ' + str(magy[k]) + '<br>' + 'Depth: ' + str(depthy[k]) for k in range(len(placy))]
				qmeans_pin.append(MapScatter(laty, lony, 10, None, None, cluster_info))
		else:
			placein_df = dummy_df[dummy_df['Place'].str.contains(str(placein_name))]
			daty = placein_df['Date'].tolist()
			laty = placein_df['Latitude'].tolist()
			lony = placein_df['Longitude'].tolist()
			placy = placein_df['Place'].tolist()
			magy = placein_df['Magnitude'].tolist()
			depthy = placein_df['Depth'].tolist()
			clat = laty[0]; clon = lony[0]
			zoom_value = 5

			cluster_info = ['Date: ' + str(daty[k]) + '<br>' + 'Place: ' + placy[k] + '<br>' + 'Magnitude: ' + str(magy[k]) + '<br>' + 'Depth: ' + str(depthy[k]) for k in range(len(placy))]
			qmeans_pin.append(MapScatter(laty, lony, 10, magy, cs_mag, cluster_info))

		layout = MapLayout(700, 10, 10, 20, 20, clat, clon, zoom_value)
		
		cluster_qmap = html.Div([
			dcc.Graph(
				id='cluster-result',
				figure={'data' : qmeans_pin, 'layout' : layout},
				config={'displayModeBar' : False}
			)
		])
		return cluster_qmap
	except Exception as e:
		return html.Div([
			html.H4('Location Unavailable for this input -- Deprecated')
		], style={'textAlign' : 'center', 'margin-top' : 150, 'margin-bottom' : 150})
##################################################
################################# predictive model ##############################

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
	if pathname == '/realtime_tracking-page':
		return realtime_tracking_layout
	if pathname == '/earthquake_history-page':
		return earth_history_layout
	else:
		return index_page

external_css = 'https://codepen.io/chriddyp/pen/bWLwgP.css'
app.css.append_css({'external_url' : external_css})

external_js = 'https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js'
app.scripts.append_script({'external_url' : external_js})

if __name__ == '__main__':
	app.run_server(debug=True)

