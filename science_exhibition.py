import csv
import dash
import time
import base64
import pandas as pd
import datetime as dt
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, Event

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
	dcc.Location(id='url', refresh=False),
	html.Div(id='page-content')
])

##################### home page ##################
index_page = html.Div([
	html.Div([
		html.H1('Earthquakes - Seismic Analysis', style={'textAlign' : 'center'}),
		html.Div([
			html.H3('Earthquake is a sudden shaking surface of the earth creating seismic waves. They are measured in terms of magnitude that signifies the occurrence type, basically varies from those that are so weak that they cannot be felt to those that are tremendous enough to create a widespread havoc.'),
		], className='container', style={'backgroundColor' : '#1C2833'}
		),
	], style={'color' : '#fff'}),

	html.Hr(),

	html.Div([
		html.Div([html.H2('National Earthquake Report')], className='container'),
		html.Div([
			html.H4('NEIC (National Earthquake Information Center) reports that 12000 - 14000 earthquakes happen each year. Smaller earthquakes of magnitude 2 occur several hundred times a day world wide and Major earthquakes of magnitude greater than 7 happen more than a once per month.')
		], className='container', style={'backgroundColor' : '#1C2833'}),
		html.Div([html.H3('Major Earthquakes')], className='container'),
		html.Div([
			html.H5('The largest recorded earthquake was Great Chilean Earthquake of May 22, 1960 which had a magnitude of 9.5. The great earthquake in  2004 in Sumatra, Indonesia measuring magnitude 9.1 produced Tsunamis that caused widespread disaster in 14 countries. In 2011, earthquake of japan having magnitude 9.0 also caused Tsunamis.')
		], className='container', style={'backgroundColor' : '#1C2833'})
	], style={'color' : '#fff'}),

	html.Div([
		html.H4('What are the major causes of Earthquakes and how is it identified/measured?', className='nine columns',
			style={'textAlign' : 'center', 'backgroundColor' : '#1C2833'}),
		dcc.Link('Check this out', href='video-page', className='three columns', 
			style={'textAlign' : 'left', 'margin-top' : 30})
	], className='row container', style={'color' : '#fff'}),

	# html.Div([
	# 	dcc.Link('Real Time Analysis', href='/realtime_analysis-page'),
	# 	html.Br(),
	# 	dcc.Link('Earthquake History', href='/earthquake_history-page'),
	# ], className='container'),

	html.Div([
		html.H2('Explore the Seismic Analysis', className='eight columns', style={'color' : '#fff', 'textAlign' : 'right'}),
		dcc.Link('Here', href='/seismic_about-page', className='four columns', style={'margin-top' : 30, 'textAlign' : 'left'})
	], className='row container'),

], style={'background-image' : 'url(http://www.zouros.gr/wp-content/uploads/2016/10/world-map-background.jpg)', 
					'background-repeat' : 'no-repeat', 'background-size' : 'cover', 
					'background-position' : 'center'}
)
##################################################

################# video page #####################
video_layout = html.Div([
	html.H2('YouTube Tutorial', style={'color' : '#fff', 'textAlign' : 'center'}),
	html.Div([dcc.Link('Back to Home', href='/')], className='container'),
	html.Div([
		html.Iframe(src=f'https://www.youtube.com/embed/{"dx4OqT0PYnU"}', 
			style={'height' : 500, 'width' : 800, 'margin-top' : 30})
	], style={'textAlign' : 'center'}),
], style={'background-image' : 'url(http://www.zouros.gr/wp-content/uploads/2016/10/world-map-background.jpg)', 
					'background-repeat' : 'no-repeat', 'background-size' : 'cover', 
					'background-position' : 'center'}
)
##################################################

################# seismic about page #####################
seismic_layout = html.Div([
	html.H2('About the Project', style={'textAlign' : 'center'}),
	html.Div([dcc.Link('Back to Home', href='/')], className='container'),
	html.Div([
		html.H3('Real Time Analysis', className='five columns', style={'textAlign' : 'right'}),
		dcc.Link('Real Time Analysis', href='/realtime_analysis-page', className='seven columns', 
			style={'textAlign' : 'left', 'margin-top' : 25})
	], className='row container'),
	html.Div([
		html.H5('The Seismic data are renedred from the official USGS website and updated every 5 minutes. This makes the Data Management handy.'),
		html.H5("Magnitude is the best available estimate of earthquake's size. It is the measure of the size of an earthquake at its source. At the same distance from the earthquake, the amplitude of the seismic waves from which the magnitude is determined are approximately 10 times as large during a magnitude 5 earthquake as during a magnitude 4 earthquake.")
	], className='container', style={'backgroundColor' : '#1C2833'}),
	html.Div([
		html.H3('Earthquake History', className='five columns', style={'textAlign' : 'right'}),
		dcc.Link('Earthquake History', href='/earthquake_history-page', className='seven columns', 
			style={'textAlign' : 'left', 'margin-top' : 25})
	], className='row container'),
	html.Div([
		html.H5('Ih this, we have considered only last 30 days of seismic data due to some constraints. Even here, the data are being updated every 15 minutes.'),
		html.H5("Earthquakes are commonly complex events that release energy over a wide range of frequencies and at varying amounts as faulting or rupture process occurs. The various types of magnitude measure different aspects of the seismic radiation.")
	], className='container', style={'backgroundColor' : '#1C2833'}),
	html.Div([html.H4('Prediction -- Work in Progress...')], className='container')
], style={'color' : '#fff', 
					'background-image' : 'url(http://www.zouros.gr/wp-content/uploads/2016/10/world-map-background.jpg)',
					'background-repeat' : 'no-repeat', 'background-size' : 'cover', 
					'background-position' : 'center'}
)
#######################################################

measuring_mags = [1.0, 2.0, 3.0, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 8.0]
radius_multiplier = {'inner' : 1.5, 'outer' : 3}

with open('map_token.txt', 'r') as mk:
	map_token = mk.read()

colorscale_magnitude = [
	[0, '#a303b9'],	[0.25, '#ea6402'],[0.5, '#fa73a0'],	
	[0.75, '#f03b20'], [1, '#bd0026'],
]

def grab_appropriate_data(datatype, filter_mag):
	quake_data = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' + str(datatype) + '.csv')
	fields = [field for field in quake_data]
	quake_values = quake_data.values
	appropriate_data = [fields]

	for qvalue in quake_values:
		quaky = list(qvalue)
		if quaky[4] > filter_mag:
			appropriate_data.append(quaky)

	with open('filtered_mags.csv', 'w') as mag:
		writer = csv.writer(mag)
		writer.writerows(appropriate_data)

def extract_places_regions(eq_places):
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

##################### real time analysis ##################
realtime_analysis_layout = html.Div([

	html.Div([
		dcc.Link('Back to About', href='/seismic_about-page', className='six columns', style={'textAlign' : 'left'}),
		dcc.Link('Earthquake History', href='/earthquake_history-page', className='six columns', style={'textAlign' : 'right'})
	], className='container'),

	dcc.Interval(id='live-update', interval='300000'), # update every 5 min

	html.Div([html.H3('Earthquake Data Plotting', style={'textAlign' : 'center', 'margin-top' : 30, 'margin-bottom' : 30}),
		html.Div([
			html.Div([html.H5('Occurence')], className='three columns', style={'textAlign' : 'right'}),
			html.Div([
				dcc.Dropdown(
					id='datatype',
					options=[
						{'label' : 'This Hour', 'value' : 'all_hour'},
						{'label' : 'Today', 'value' : 'all_day'},
						{'label' : 'Last Week', 'value' : 'all_week'},
					],
					value='all_day',
				)
			], className='three columns', style={'textAlign' : 'left'}),
			html.Div([html.H5('Mag above')], className='two columns', style={'textAlign' : 'right'}),
			html.Div([
				dcc.Dropdown(
					id='magnitude-drop',
					options=[{'label' : s, 'value' : s} for s in measuring_mags],
					value=3
				)
			], className='two columns', style={'textAlign' : 'center'})
		], className='row', style={'textAlign' : 'center'}),
		html.Div([
			html.Div([html.H5('Select the State Region')], className='six columns',
				style={'textAlign' : 'right'}),
			html.Div([
				dcc.Dropdown(id='region-options')
			], className='three columns', style={'textAlign' : 'left'})
		], className='row', style={'margin-top' : 30}),
	], style={'borderBottom' : 'thin lightgrey solid', 
			'backgroundColor' : 'rgb(213, 245, 227)', 
			'padding': '10px 10px', 'margin-left' : 30, 
			'margin-right' : 30, 'margin-top' : 40
	}),

	html.Div([html.Div(id='map-output')]),

	html.Hr(),

	html.Div([
		html.Div(id='highest-mag'),
		html.Div([
			html.Div([
				html.H6('Total Earthquakes across the states',
						style={'textAlign' : 'center'}),
				html.Div(id='region-pie')
			], className='eight columns'),
			html.Div([
				html.H6('No: of earthquakes in a year', style={'textAlign' : 'center'}),
					html.Div([
						html.P("NEIC (National Earthquake Information Center) reports that 12000 - 14000 earthquakes happen each year. Smaller earthquakes of magnitude 2 occur several hundred times a day world wide and Major earthquakes of magnitude greater than 7 happen more than a once per month."),
						html.P("The largest recorded earthquake was Great Chilean Earthquake of May 22, 1960 which had a magnitude of 9.5. The great earthquake in  2004 in Sumatra, Indonesia measuring magnitude 9.1 produced Tsunamis that caused widespread disaster in 14 countries. In 2011, earthquake of japan having magnitude 9.0 also caused Tsunamis.")
					], style={'margin-right' : 25, 'margin-top' : 40})
			], className='four columns'),
		], className='row', style={'margin-top' : 40}),
		
		# html.Hr(),

		html.Div([
			html.Div([
				html.H6('Significance of Magnitude', style={'textAlign' : 'center'}),
				html.Div([
					html.P("Magnitude is the best available estimate of earthquake's size. It is the measure of the size of an earthquake at its source. At the same distance from the earthquake, the amplitude of the seismic waves from which the magnitude is determined are approximately 10 times as large during a magnitude 5 earthquake as during a magnitude 4 earthquake."),
					html.P("Earthquakes are commonly complex events that release energy over a wide range of frequencies and at varying amounts as faulting or rupture process occurs. The various types of magnitude measure different aspects of the seismic radiation.")
				], style={'margin-left' : 30, 'textAlign' : 'left'})
			], className='four columns', style={'margin-top' : 30}),
			html.Div([
				html.H6('Magnitudes of Earthquakes', style={'textAlign' : 'center'}),
				html.Div(id='mag-bar')
			], className='eight columns')
		], className='row', style={'margin-top' : 30}),
	
	])
])

######## update the state regions options ########
@app.callback(
	Output('region-options', 'options'),
	[Input('datatype', 'value'),	Input('magnitude-drop', 'value')],
	events=[Event('live-update', 'interval')]
)
def grab_region_options(datatype, filter_mag):
	grab_appropriate_data(datatype, filter_mag)
	eq = pd.read_csv('filtered_mags.csv')
	places = eq['place'].tolist()
	_, regions, _ = extract_places_regions(places)
	regions.insert(0, 'World Wide')
	return [{'label' : s, 'value' : s} for s in regions]

# @app.callback(
# 	Output('region-options', 'value'),
# 	[Input('region-options', 'options')],
# 	events=[Event('live-update', 'interval')]
# )
# def set_region_value(region_options):
# 	return region_options[0]['value']
##################################################

# 'Canada': [['165km WNW of Haines Junction', 61.4201, -140.2431, 
# 						'Magnitude: 2.1', 6.300000000000001, 'Depth: 0.0', 0.0]]

############# plot earthquakes ###################
@app.callback(
	Output('map-output', 'children'),
	[Input('datatype', 'value'), Input('magnitude-drop', 'value'), 
		Input('region-options', 'value')],
	events=[Event('live-update', 'interval')]
)
def plot_earthquakes(datatype, filter_mag, region_options):
	try:
		grab_appropriate_data(datatype, filter_mag)
		eq = pd.read_csv('filtered_mags.csv')

		latitudes = eq['latitude'].tolist()
		longitudes = eq['longitude'].tolist()
		places = eq['place'].tolist()
		mags = eq['mag'].tolist()
		depths = eq['depth'].tolist()

		mag_info = ['Magnitude: ' + str(i) for i in mags]
		mag_size = [float(i) * radius_multiplier['outer'] for i in mags]
		depth_size = [float(i) * radius_multiplier['inner'] for i in depths]
		depth_info = ['Depth: ' + str(i) for i in depths]

		_, eplaces, _ = extract_places_regions(places)
		seperate = []
		for p in range(len(places)):
			# split into, first name and last name example : "122km SSE Name, Iran" --> ["122km SSE Name", "Iran"]
			seperate.append([places[p].split(', '), latitudes[p], longitudes[p], 
				mag_info[p], mag_size[p], depth_info[p], depth_size[p]])

		state_regions = {}
		for p in eplaces:
			regions = []	
			for sep in seperate:
				locr = sep[0]
				if len(locr) == 2:
					if locr[1] == p:
						regions.append([locr[0], sep[1], sep[2], 
							sep[3], sep[4], sep[5], sep[6]])
				if len(locr) != 2:
					if locr[0] == p:
						regions.append([locr[0], sep[1], sep[2], 
							sep[3], sep[4], sep[5], sep[6]])
			state_regions[p] = regions
		state_regions['World Wide'] = []
		# print(state_regions)

		mi = []; ms = []; di = []; ds = []; lats = []; lons = []
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
					ds.append(about[6])
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
					ds.append(about[6])

		info = [region_names[i] + '<br>' + mi[i] + '<br>' + di[i] for i in range(len(region_names))]

		quakes = [
			go.Scattermapbox(
				lat=lats, lon=lons,	mode='markers',
				marker=dict(
					size=ms, color=ms, opacity=1,
					colorscale=colorscale_magnitude,
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
				pitch=0, zoom=zoom_value, 
				style='mapbox://styles/chaotic-enigma/cjpbbmuzmadb12spjq5n07nd1'
			)
		)
		map_deisgn = html.Div([
			dcc.Graph(id='map-earthquake', figure={'data' : quakes, 'layout' : layout})
		])
		return map_deisgn

	except Exception as e:
		return html.Div([
			html.H4('Could not load the map for some reasons'),
			html.H2('Please select the input...')
		], style={'margin-top' : 200, 'margin-bottom' : 200, 'textAlign' : 'center'})
##################################################

############# display the highest mag ############
@app.callback(
	Output('highest-mag', 'children'),
	[Input('datatype', 'value'), Input('magnitude-drop', 'value')],
	events=[Event('live-update', 'interval')]
)
def display_highest_mag(datatype, filter_mag):
	grab_appropriate_data(datatype, filter_mag)
	eq = pd.read_csv('filtered_mags.csv')
	hm_mags = eq['mag'].tolist()
	high_mag = max(hm_mags)
	places = eq['place'].tolist()

	for p in range(len(places)):
		if hm_mags[p] == high_mag:
			hm_place = places[p]

	return html.Div([html.H1(str(high_mag) + ' -- ' + str((hm_place)))
	], style={'textAlign' : 'center'})
##################################################

############# bar chart - update #################
def bar_chart_colouring(mags):
	min_mag = min(mags)
	threshold_mag = 5.0
	bar_highlight = []
	for m in mags:
		if m >= threshold_mag:
			bar_highlight.append('rgba(222,45,38,0.8)')
		elif m == min_mag:
			bar_highlight.append('rgb(40,180,99)')
		else:
			bar_highlight.append('rgb(41,128,185)')
	return bar_highlight

@app.callback(
	Output('mag-bar', 'children'),
	[Input('datatype', 'value'), Input('magnitude-drop' , 'value'), 
		Input('region-options', 'value')],
	events=[Event('live-update', 'interval')]
)
def mag_bar_diagram(datatype, filter_mag, region_options):
	try:
		if datatype == 'all_hour' or datatype == 'all_day':
			grab_appropriate_data(datatype, filter_mag)
			eq = pd.read_csv('filtered_mags.csv')
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
				html.H4('Sorry, could not display the chart for the ' + str(datatype) + '...')
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
	[Input('datatype' , 'value'), Input('magnitude-drop', 'value')],
	events=[Event('live-update', 'interval')]
)
def pie_region_diagram(datatype, filter_mag):
	try:
		if datatype == 'all_hour' or datatype == 'all_day':
			grab_appropriate_data(datatype, filter_mag)
			eq = pd.read_csv('filtered_mags.csv')
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
				html.H4('Sorry, could not display the chart for the ' + str(datatype) + '...')
			], style={'textAlign' : 'center', 'margin-top' : 150})
			return issue

	except Exception as e:
		return html.Div([
			html.H4('Network issues, try refreshing the page...')
		], style={'textAlign' : 'center', 'margin-top' : 150})
##################################################

###################################################################################################
############## history of earthquakes ############
logo_image = 'cartoon-globe.png'
en_logo = base64.b64encode(open(logo_image, 'rb').read())

entire_month = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv')

def extract_month_values():
	all_month = entire_month.copy()
	time = pd.to_datetime(all_month['time'])
	all_month['time'] = time
	fields = [field for field in all_month]
	month_values = all_month.values
	return fields, month_values
# print(extract_month_values())

def csv_feature_extraction(year, month, day):
	fields, month_values = extract_month_values()
	extraction = [fields]
	for vals in month_values:
		if vals[0].year == year and vals[0].month == month and vals[0].day == day:
			if vals[4] >= 4.5: # magnitude > 1
				extraction.append(vals)
	return extraction
# print(csv_feature_extraction(11, 20))

def day_wise_extraction(year, month, day):
	extraction = csv_feature_extraction(year, month, day)
	with open('month_day.csv', 'w') as extract:
		writer = csv.writer(extract)
		writer.writerows(extraction)
# print(day_wise_extraction(11, 21))

def get_dates_sorted():
	_, month_values = extract_month_values()
	all_dates = []
	for each_date in month_values:
		all_dates.append(str(each_date[0].date()))
	timestamps = sorted(list(set(all_dates)))
	return timestamps
# print(get_dates_sorted())

timestamps = get_dates_sorted()
date_start = dt.datetime.strptime(timestamps[0], '%Y-%m-%d')
date_end = dt.datetime.strptime(timestamps[len(timestamps)-1], '%Y-%m-%d')

def place_wise_extraction(place_name):
	all_month = entire_month.copy()
	all_places = all_month['place'].tolist()
	u_regions, _, _ = extract_places_regions(all_places) # specific last name
	# print(u_regions)
	fields, month_values = extract_month_values()
	place_data = [fields]
	if place_name in u_regions:
		for each_item in month_values:
			each_row = list(each_item)
			p = each_row[13].split(', ')
			if len(p) == 2:
				if p[1] == place_name:
					if each_row[4] >= 1:
						place_data.append(each_row)
			elif len(p) == 1:
				if p[0] == place_name:
					if each_row[4] >= 1:
						place_data.append(each_row)
	if place_name == 'earth' or place_name == 'world':
		for each_item in month_values:
			each_row = list(each_item)
			if each_row[4] >= 1:
				place_data.append(each_row)
	
	with open('place_data.csv', 'w') as pdata:
		writer = csv.writer(pdata)
		writer.writerows(place_data)

def history_eq(eq_some, zoom_value):
	lats = eq_some['latitude'].tolist()
	lons = eq_some['longitude'].tolist()
	places = eq_some['place'].tolist()
	mags = ['Magnitude : ' + str(i) for i in eq_some['mag']]
	mag_size = [float(i) * radius_multiplier['outer'] for i in eq_some['mag']]
	depth_size = [float(i) * radius_multiplier['inner'] for i in eq_some['mag']]
	depths = ['Depth : ' + str(i) for i in eq_some['depth']]
	info = [places[i] + '<br>' + mags[i] + '<br>' + depths[i] for i in range(len(places))]
	zooming = zoom_value
	return lats, lons, places, mags, mag_size, depth_size, depths, info, zooming
###################################################################################################

earthquake_history_layout = html.Div([

	html.Div([
		dcc.Link('Back to About', href='/seismic_about-page', className='six columns', style={'textAlign' : 'left'}),
		dcc.Link('Real Time Analysis', href='/realtime_analysis-page', className='six columns', style={'textAlign' : 'right'})
	], className='container'),

	html.Div([
		html.Div([
			html.Img(src='data:image/png;base64,{}'.format(en_logo.decode()), id='logo',
				style={'width' : 90, 'height' : 90})
		], className='two columns', style={'textAlign' : 'right'}),
		html.Div([
			dcc.Input(id='search-here', type='text', value='', 
				placeholder='Search Places : ', size=60
			)
		], className='four columns', style={'margin-top' : 25}),
		html.Div([
			html.P('Monthly data', style={'textAlign' : 'center'}),
			dcc.DatePickerRange(
				id='all-thirty',
				start_date=date_start,
				end_date=date_end,
				min_date_allowed=date_start,
				max_date_allowed=date_end
			)
		], className='five columns', style={'textAlign' : 'right'})
	], className='row', style={'margin-top' : 40}),

	html.Div([html.Div(id='map-daily-output')])

])

################ earthquake history ##############
@app.callback(
	Output('map-daily-output', 'children'),
	[Input('all-thirty', 'start_date'), Input('all-thirty', 'end_date'), 
		Input('search-here', 'value')]
)
def display_quakes_day(start, end, query):
	try:
		start = dt.datetime.strptime(start, '%Y-%m-%d')
		end = dt.datetime.strptime(end, '%Y-%m-%d')
		year, month, day = [start.year, start.month, start.day]
		query_value = query

		lats = []; lons = []; places = []; info = []
		mags = []; mag_size = []; depth_size = []; depths = []

		if query_value == '':
			day_wise_extraction(year, month, day)
			eq = pd.read_csv('month_day.csv')
			lats, lons, places, mags, mag_size, depth_size, depths, info, zoom_value = history_eq(eq, 1)
		else:
			if query_value == 'earth' or query_value == 'world':
				place_wise_extraction(query_value)
				eq = pd.read_csv('place_data.csv')
				lats, lons, places, mags, mag_size, depth_size, depths, info, zoom_value = history_eq(eq, 1)
			else:
				place_wise_extraction(query_value)
				eq = pd.read_csv('place_data.csv')
				lats, lons, places, mags, mag_size, depth_size, depths, info, zoom_value = history_eq(eq, 3)

		quakes = [
			go.Scattermapbox(
				lat=lats, lon=lons, mode='markers',
				marker=dict(
					size=mag_size, color=eq['mag'], opacity=1,
					colorscale=colorscale_magnitude,
				),
				text=info, hoverinfo='text', showlegend=False
			),
		]
		layout = go.Layout(
			height=700, autosize=True, showlegend=False,
		  hovermode='closest',
		  geo=dict(
			  projection=dict(type="equirectangular"),
		  ),
		  mapbox=dict(
		    accesstoken=map_token, bearing=1,
				center=dict(
					lat=lats[0], lon=lons[0]
				),
				pitch=0, zoom=zoom_value, 
				style='mapbox://styles/chaotic-enigma/cjpbbmuzmadb12spjq5n07nd1'
			)
		)

		map_deisgn = html.Div([
			dcc.Graph(id='map-earthquake', figure={'data' : quakes, 'layout' : layout})
		])
		return map_deisgn
		
	except Exception as e:
		return html.Div([
			html.H4('Network issues, could not load the map'),
			html.H2('Try refreshing the page...'),
			html.P(str(e))
		], style={'margin-top' : 200, 'margin-bottom' : 200, 'textAlign' : 'center'})
##################################################

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
	if pathname == '/realtime_analysis-page':
		return realtime_analysis_layout
	elif pathname == '/earthquake_history-page':
		return earthquake_history_layout
	elif pathname == '/video-page':
		return video_layout
	elif pathname == '/seismic_about-page':
		return seismic_layout
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

