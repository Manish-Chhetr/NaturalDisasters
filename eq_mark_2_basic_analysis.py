import csv
import dash
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

measuring_mags = [1.0, 2.0, 3.0, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0, 8.0]
radius_multiplier = {'inner' : 1.5, 'outer' : 3}

with open('map_token.txt', 'r') as mk:
	map_token = mk.read()

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True

colorscale_magnitude = [
	[0, '#a303b9'],
	[0.25, '#ea6402'], 
	[0.5, '#fa73a0'],
	[0.75, '#f03b20'],
	[1, '#bd0026'],
]
colorscale_depth = [
	[0, '#f0f0f0'],
	[0.5, '#bdbdbd'],
	[0.1, '#636363'],
]

about_mags = pd.read_csv('magnitude_scale.csv')

app.layout = html.Div([
	html.H1('Natural Disasters', 
		style={'textAlign' : 'center', 'margin-top' : 45, 'margin-bottom' : 35}),
	dcc.Tabs(id='natural-disasters', children=[
		dcc.Tab(label='Earthquakes', children=[
			html.Hr(),
			html.Div([
				html.H3('Earthquake Data Plotting', 
					style={'textAlign' : 'center', 'margin-top' : 30, 'margin-bottom' : 30}),
				html.Div([
					html.Div([html.H5('Type of the data')], 
						className='three columns', style={'textAlign' : 'right'}),
					html.Div([
						dcc.Dropdown(
							id='datatype',
							options=[
								{'label' : 'This Hour', 'value' : 'all_hour'},
								{'label' : 'Yesterday', 'value' : 'all_day'},
								{'label' : 'Last Week', 'value' : 'all_week'},
							],
							value='all_hour',
						)
					], className='three columns', style={'textAlign' : 'left'}),
					html.Div([html.H5('Magnitude ( > )')], className='two columns',
						style={'textAlign' : 'right'}),
					html.Div([
						dcc.Dropdown(
							id='magnitude-drop',
							options=[{'label' : s, 'value' : s} for s in measuring_mags],
							value=2
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
					'padding': '10px 10px',
					'margin-left' : 30, 
					'margin-right' : 30,
			}),

			html.Div([dcc.Graph(id='map-layout')]),

			html.Div([
				html.Div([
					html.Div([html.Div(id='highest-mag')]),
					html.Div([
						html.Table([
							html.Thead(
								html.Tr([html.Th(col.title()) for col in about_mags.columns.values])
							),
							html.Tbody([
								html.Tr([html.Td(data) for data in rd]) for rd in about_mags.values.tolist()
							])
						])
					], style={'margin-left' : 50, 'margin-top' : 40})
				], className='four columns'),
				html.Div([
					html.H6('Magnitude and Places', style={'textAlign' : 'center'}),
					dcc.Tabs(id='mag-grpahs', value='mbar', children=[
						dcc.Tab(label='Line Graph', value='mline', children=[
							dcc.Graph(id='mag-line')
						]),
						dcc.Tab(label='Bar Graph', value='mbar', children=[
							dcc.Graph(id='mag-bar')
						])
					])
				], className='eight columns')
			], className='row'),
			html.Hr(),

			html.Div([
				html.Div([
					html.H5('Total Earthquakes across the states', style={'textAlign' : 'center'}),
					dcc.Graph(id='pie-chart')
				], className='eight columns'),
				html.Div([
					html.H6('No: of earthquakes in a year', style={'textAlign' : 'center'}),
					html.Div([
						html.P("NEIC (National Earthquake Information Center) reports that 12000 - 14000 earthquakes happen each year. Smaller earthquakes of magnitude 2 occur several hundred times a day world wide and Major earthquakes of magnitude greater than 7 happen more than a once per month."),
						html.P("The largest recorded earthquake was Great Chilean Earthquake of May 22, 1960 which had a magnitude of 9.5. The great earthquake in  2004 in Sumatra, Indonesia measuring magnitude 9.1 produced Tsunamis that caused widespread disaster in 14 countries. In 2011, earthquake of japan having magnitude 9.0 also caused Tsunamis.")
					], style={'margin-right' : 25, 'margin-top' : 40})
				], className='four columns', style={'margin-top' : 50})
			], className='row'),
			html.Hr(),

		]),
		dcc.Tab(label='Volcanoes', children=[
			html.Hr(),
			html.H3('Working in progress', 
				style={'textAlign' : 'center', 'margin-top' : 30, 'margin-bottom' : 30})
		]),
		dcc.Tab(label='Floods', children=[
			html.Hr(),
			html.H3('Working in progress', 
				style={'textAlign' : 'center', 'margin-top' : 30, 'margin-bottom' : 30})
		])
	])
])

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

@app.callback(
	Output('region-options', 'options'),
	[Input('datatype', 'value'), Input('magnitude-drop', 'value')]
)
def grab_region_option(datatype, filter_mag):
	grab_appropriate_data(datatype, filter_mag)
	eq = pd.read_csv('filtered_mags.csv')
	places = list(eq['place'])
	latitudes = list(eq['latitude'])
	longitudes = list(eq['longitude'])

	end_names = []
	for p in places:
		fplp = p.split(', ')
		if len(fplp) == 2:
			end_names.append(fplp[1])
		if len(fplp) == 1:
			end_names.append(fplp[0])

	counter_places = {}
	splaces = list(set(end_names))
	for entry in splaces:
		counter_places[entry] = end_names.count(entry)

	regions = counter_places.keys()
	regions.insert(0, 'World Wide')
	all_regions = {str(datatype) : regions}
	return [{'label' : s, 'value' : s} for s in regions]

@app.callback(
	Output('region-options', 'value'),
	[Input('region-options', 'options')]
)
def set_region_value(region_options):
	return region_options[0]['value']

@app.callback(
	Output('map-layout', 'figure'),
	[ Input('datatype', 'value'), Input('magnitude-drop', 'value'), 
		Input('region-options', 'value')]
)
def show_earthquakes(datatype, filter_mag, region_options):
	grab_appropriate_data(datatype, filter_mag)
	eq = pd.read_csv('filtered_mags.csv')

	latitudes = list(eq['latitude'])
	longitudes = list(eq['longitude'])
	places = list(eq['place'])
	mag_info = ['Magnitude: ' + str(i) for i in eq['mag']]
	mag_size = [float(i) * radius_multiplier['outer'] for i in eq['mag']]
	depth_size = [float(i) * radius_multiplier['inner'] for i in eq['mag']]
	depth_info = ['Depth: ' + str(i) for i in eq['depth']]

	end_names = []
	for p in places:
		fplp = p.split(', ')
		if len(fplp) == 2:
			end_names.append(fplp[1])
		if len(fplp) == 1:
			end_names.append(fplp[0])

	counter_places = {}
	splaces = list(set(end_names))
	for entry in splaces:
		counter_places[entry] = end_names.count(entry)

	eplaces = counter_places.keys()
	seperate = []
	for p in range(len(places)):
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

	mi = []; ms = []; di = []
	ds = []; lats = []; lons = []
	region_names = []
	# zoom_value = 0
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
	return {'data' : quakes, 'layout' : layout}

@app.callback(
	Output('highest-mag', 'children'),
	[Input('datatype', 'value'), Input('magnitude-drop', 'value')]
)
def display_highest(datatype, filter_mag):
	grab_appropriate_data(datatype, filter_mag)
	eq = pd.read_csv('filtered_mags.csv')
	hm_mags = eq['mag'].tolist()
	high_mag = max(hm_mags)
	places = eq['place'].tolist()

	for p in range(len(places)):
		if hm_mags[p] == high_mag:
			hm_place = places[p]

	return html.Div([
			html.Div([html.H1(str(high_mag))], style={'margin-bottom' : -20}),
			html.Div([html.P(hm_place)]),
		], style={'margin-top' : 40, 'textAlign' : 'center'})

@app.callback(
	Output('mag-line', 'figure'),
	[ Input('datatype', 'value'), Input('magnitude-drop', 'value'), 
		Input('region-options', 'value')]
)
def mag_line_diagram(datatype, filter_mag, region_options):
	grab_appropriate_data(datatype, filter_mag)
	eq = pd.read_csv('filtered_mags.csv')
	places = list(eq['place'])
	mags = list(eq['mag'])

	end_names = []
	for p in places:
		fplp = p.split(', ')
		if len(fplp) == 2:
			end_names.append(fplp[1])
		if len(fplp) == 1:
			end_names.append(fplp[0])

	counter_places = {}
	splaces = list(set(end_names))
	for entry in splaces:
		counter_places[entry] = end_names.count(entry)

	eplaces = counter_places.keys()
	seperate = []
	for p in range(len(places)):
		seperate.append([places[p].split(', '), mags[p]])

	state_regions = {}
	for p in eplaces:
		regions = []	
		for sep in seperate:
			locr = sep[0]
			if len(locr) == 2:
				if locr[1] == p:
					regions.append([locr[0], sep[1]])
			if len(locr) != 2:
				if locr[0] == p:
					regions.append([locr[0], sep[1]])
		state_regions[p] = regions
	state_regions['World Wide'] = []

	line_region = []
	line_mag = []
	for k, v in state_regions.items():
		if k == region_options:
			details = v
			for about in details:
				line_region.append(about[0])
				line_mag.append(about[1])
	if region_options == 'World Wide':
		for k, v in state_regions.items():
			details = v
			for about in details:
				line_region.append(about[0])
				line_mag.append(about[1])

	traces = []
	traces.append(
		go.Scatter(
			x=line_region, y=line_mag,
			mode='lines+markers',
			name='Region Magnitude'
		)
	)
	layout = go.Layout(
		title=str(region_options)
	)
	return {'data' : traces, 'layout' : layout}

@app.callback(
	Output('mag-bar', 'figure'),
	[ Input('datatype', 'value'), Input('magnitude-drop', 'value'), 
		Input('region-options', 'value')]
)
def mag_bar_diagram(datatype, filter_mag, region_options):
	grab_appropriate_data(datatype, filter_mag)
	eq = pd.read_csv('filtered_mags.csv')
	places = list(eq['place'])
	mags = list(eq['mag'])

	end_names = []
	for p in places:
		fplp = p.split(', ')
		if len(fplp) == 2:
			end_names.append(fplp[1])
		if len(fplp) == 1:
			end_names.append(fplp[0])

	counter_places = {}
	splaces = list(set(end_names))
	for entry in splaces:
		counter_places[entry] = end_names.count(entry)

	eplaces = counter_places.keys()
	seperate = []
	for p in range(len(places)):
		seperate.append([places[p].split(', '), mags[p]])

	state_regions = {}
	for p in eplaces:
		regions = []	
		for sep in seperate:
			locr = sep[0]
			if len(locr) == 2:
				if locr[1] == p:
					regions.append([locr[0], sep[1]])
			if len(locr) != 2:
				if locr[0] == p:
					regions.append([locr[0], sep[1]])
		state_regions[p] = regions
	state_regions['World Wide'] = []

	region_places = state_regions.keys()
	region_places.remove('World Wide')

	traces = []
	line_region = []
	line_mag = []
	if region_options in region_places:
		for k, v in state_regions.items():
			if k == region_options:
				details = v
				for about in details:
					line_region.append(about[0])
					line_mag.append(about[1])
		max_mag = max(line_mag)
		min_mag = min(line_mag)
		threshold_mag = 5.0
		bar_highlight = []
		for m in line_mag:
			if m >= threshold_mag:
				bar_highlight.append('rgba(222,45,38,0.8)')
			elif m == min_mag:
				bar_highlight.append('rgb(40,180,99)')
			else:
				bar_highlight.append('rgb(41,128,185)')
		traces.append(
			go.Bar(
				x=line_region, y=line_mag,
				name='Region Magnitude',
				marker=dict(color=bar_highlight)
			)
		)
		layout = go.Layout(
			title=str(region_options)
		)
		return {'data' : traces, 'layout' : layout}

	elif region_options == 'World Wide':
		for k, v in state_regions.items():
			details = v
			for about in details:
				line_region.append(about[0])
				line_mag.append(about[1])
		# max_mag = max(line_mag)
		min_mag = min(line_mag)
		threshold_mag = 5.0
		bar_highlight = []
		for m in line_mag:
			if m >= threshold_mag:
				bar_highlight.append('rgba(222,45,38,0.8)')
			elif m == min_mag:
				bar_highlight.append('rgb(40,180,99)')
			else:
				bar_highlight.append('rgb(41,128,185)')
		traces.append(
			go.Bar(
				x=line_region, y=line_mag,
				name='Region Magnitude',
				marker=dict(color=bar_highlight)
			)
		)
		layout = go.Layout(
			title=str(region_options)
		)
		return {'data' : traces, 'layout' : layout}

@app.callback(
	Output('pie-chart', 'figure'),
	[Input('datatype', 'value'), Input('magnitude-drop', 'value')]
)
def pie_diagram(datatype, filter_mag):
	grab_appropriate_data(datatype, filter_mag)
	eq = pd.read_csv('filtered_mags.csv')
	places = list(eq['place'])

	lname = []
	for area in places:
		aplace = area.split(', ')
		if len(aplace) == 2:
			lname.append(aplace[1])
		if len(aplace) == 1:
			lname.append(aplace[0])

	counter_places = {}
	splaces = list(set(lname))
	for entry in splaces:
		counter_places[entry] = lname.count(entry)

	traces = []
	traces.append(
		go.Pie(
			labels=counter_places.keys(),
			values=counter_places.values(),
			pull=.1
		)
	)
	layout = go.Layout(
		title='World Wide'
	)
	return {'data' : traces, 'layout' : layout}

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
for css in external_css:
	app.css.append_css({'external_url' : css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
	app.scripts.append_script({'external_url' : js})

if __name__ == '__main__':
	app.run_server(debug=True)
