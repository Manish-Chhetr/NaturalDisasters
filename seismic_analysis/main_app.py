import time
import pandas as pd
import datetime as dt

import dash
import dash_core_components as dcc
import dash_html_components as  html
import plotly.graph_objs as go
from dash.dependencies import (Input, Output, Event)

from design_layout import (index_page, realtime_analysis_layout, earth_history_layout, colors_useful)
from realtime_details import (grab_appropriate_data, extract_places_regions, radius_multiplier, center_location)
from report_alerts import (seismic_reporting_data, get_all_felts, get_all_tsunamis, get_all_alerts, make_seismic_report, make_alert_report)

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True

cs_mag = [
	[0, '#a303b9'],	[0.25, '#ea6402'],[0.5, '#fa73a0'],	
	[0.75, '#f03b20'], [1, '#bd0026'],
]

with open('map_token.txt', 'r') as mk:
	map_token = mk.read()

app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content')
])

earth_quake_df = pd.read_csv('eq_database_place.csv') # for earthquake_history

################################# realtime analysis callbacks ############################
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
			# split into, first name and last name example : "122km SSE Name, Iran" --> ["122km SSE Name", "Iran"]
			seperate.append([places[p].split(', '), latitudes[p], longitudes[p], 
				mag_info[p], mag_size[p], depth_info[p]])

		state_regions = {}
		for p in eplaces:
			regions = []	
			for sep in seperate:
				locr = sep[0]
				if len(locr) == 2:
					if locr[1] == p:
						regions.append([locr[0], sep[1], sep[2], 
							sep[3], sep[4], sep[5]])
				if len(locr) != 2:
					if locr[0] == p:
						regions.append([locr[0], sep[1], sep[2], 
							sep[3], sep[4], sep[5]])
			state_regions[p] = regions
		state_regions['World Wide'] = []
		# print(state_regions)

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

		quakes = [
			go.Scattermapbox(
				lat=lats, lon=lons,	mode='markers',
				marker=dict(
					size=ms, color=ms, opacity=1,
					colorscale=cs_mag,
				),
				text=info, hoverinfo='text', showlegend=False
			)
		]
		layout = go.Layout(
			height=700, autosize=True, showlegend=False,
		  hovermode='closest',
		  geo=dict(
		  	projection=dict(type="equirectangular"),
		  ),
		  mapbox=dict(
		    accesstoken=map_token, bearing=1,
				center=dict(lat=c_lat, lon=c_lon),
				pitch=0, zoom=zoom_value, 
				style='mapbox://styles/chaotic-enigma/cjpbbmuzmadb12spjq5n07nd1'
			)
		)
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
			html.H4('Could not load the map for some reasons'),
			html.H2('Please select the input...'),
			# html.P(str(e))
		], style={'margin-top' : 200, 'margin-bottom' : 200, 'textAlign' : 'center'})
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
		make_report = make_seismic_report(report_list, '#d35400', '#8e44ad')
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
		make_report = make_seismic_report(report_list, '#0240da', '#0240da')
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
	[Input('occurence_type', 'value'), Input('magnitude-drop', 'value')],
	events=[Event('live-update', 'interval')]
)
def display_highest_mag(occurence_type, mag_value):
	eq = grab_appropriate_data(occurence_type, mag_value)
	hm_mags = eq['mag'].tolist()
	high_mag = max(hm_mags)
	places = eq['place'].tolist()

	for p in range(len(places)):
		if hm_mags[p] == high_mag:
			hm_place = places[p]

	return html.Div([html.H1('M ' + str(high_mag) + ' -- ' + str((hm_place)))
	], style={'textAlign' : 'center'})
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
		if occurence_type == 'all_hour' or occurence_type == 'all_day':
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
							regions.append([locr[0], sep[1], sep[2]])
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
				layout = go.Layout(
					height=600,
					title=str(region_options)
				)
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

		else:
			issue = html.Div([
				html.H4('Sorry, could not display the chart for the ' + str(occurence_type) + '...')
			], style={'textAlign' : 'center', 'margin-top' : 150})
			return issue

	except Exception as e:
		return html.Div([
			html.H4('Network issues, try refreshing the page...')
		], style={'textAlign' : 'center', 'margin-top' : 150})

##################################################

############# pie chart - update #################
@app.callback(
	Output('region-pie', 'children'),
	[Input('occurence_type' , 'value'), Input('magnitude-drop', 'value')],
	events=[Event('live-update', 'interval')]
)
def pie_region_diagram(occurence_type, mag_value):
	try:
		if occurence_type == 'all_hour' or occurence_type == 'all_day':
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

		else:
			issue = html.Div([
				html.H4('Sorry, could not display the chart for the ' + str(occurence_type) + '...')
			], style={'textAlign' : 'center', 'margin-top' : 150})
			return issue

	except Exception as e:
		return html.Div([
			html.H4('Network issues, try refreshing the page...')
		], style={'textAlign' : 'center', 'margin-top' : 150})
##################################################
################################# realtime analysis callbacks ############################

################################# earthquake history ############################
@app.callback(
	Output('history-map', 'children'), [Input('countries-dropdown', 'value')]
)
def show_ancient_cw(country_name):
	country_wise_df = earth_quake_df[earth_quake_df['Place'].str.contains(str(country_name))]

	lats = country_wise_df['Latitude'].tolist()
	lons = country_wise_df['Longitude'].tolist()
	mags = country_wise_df['Magnitude'].tolist()
	deps = country_wise_df['Depth'].tolist()
	places = country_wise_df['Place'].tolist()
	dates = country_wise_df['Date'].tolist()

	occ_dates = ['Date: ' + str(i) for i in dates]
	di = ['Depth: ' + str(i) for i in deps]
	mi = ['Magnitude: ' + str(i) for i in mags]
	ms = [float(i) * radius_multiplier['outer'] for i in mags]
	info = [occ_dates[i] + '<br>' + places[i] + '<br>' + mi[i] + '<br>' + di[i] for i in range(len(places))]

	quakes = [
		go.Scattermapbox(
			lat=lats, lon=lons,	mode='markers',
			marker=dict(
				size=10, color=ms, opacity=1,
				colorscale=cs_mag,
			),
			text=info, hoverinfo='text', showlegend=False
		)
	]
	layout = go.Layout(
		height=700, autosize=True, showlegend=False,
	  hovermode='closest',
	  geo=dict(
	  	projection=dict(type="equirectangular"),
	  ),
	  mapbox=dict(
	    accesstoken=map_token, bearing=1,
			center=dict(lat=lats[0], lon=lons[0]),
			pitch=0, zoom=3, 
			style='mapbox://styles/chaotic-enigma/cjpbbmuzmadb12spjq5n07nd1'
		)
	)

	country_map = html.Div([
		dcc.Graph(id='country-result', figure={'data' : quakes, 'layout' : layout})
	])
	return country_map
################################# earthquake history ############################

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
	if pathname == '/realtime_analysis-page':
		return realtime_analysis_layout
	if pathname == '/earthquake_history-page':
		return earth_history_layout
	else:
		return index_page

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
for css in external_css:
	app.css.append_css({'external_url' : css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
	app.scripts.append_script({'external_url' : js})

if __name__ == '__main__':
	app.run_server(debug=True)

