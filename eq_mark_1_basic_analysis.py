import csv
import dash
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

measuring_mags = [1.0, 2.0, 3.0, 4.0, 4.5, 5.0, 5.5, 6.0, 6.5, 7.0]
radius_multiplier = {'inner' : 1.5, 'outer' : 3}

with open('map_token.txt', 'r') as mk:
	map_token = mk.read()

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True

colorscale_magnitude = [
	[0, '#ffffb2'],
	[0.25, '#fecc5c'],
	[0.5, '#fd8d3c'],
	[0.75, '#f03b20'],
	[1, '#bd0026'],
]
colorscale_depth = [
	[0, '#f0f0f0'],
	[0.5, '#bdbdbd'],
	[0.1, '#636363'],
]

app.layout = html.Div([
	html.H2('Natural Disasters', style={'textAlign' : 'center'}),
	dcc.Tabs(id='natural-disasters', children=[
		dcc.Tab(label='Earthquakes', children=[
			html.H3('Earthquake Data Plotting', style={'textAlign' : 'center'}),
			html.Hr(),
			html.Div([
				html.Div([
					html.Div([
						html.Div([
							html.H5('Type of the data')
						], className='three columns', style={'textAlign' : 'right'}),
						html.Div([
							dcc.Dropdown(
								id='type-data',
								options=[
									{'label' : 'Past Hour', 'value' : 'all_hour'},
									{'label' : 'Past Day', 'value' : 'all_day'},
									{'label' : 'Past Week', 'value' : 'all_week'},
								],
								value='all_day',
							)
						], className='three columns', style={'textAlign' : 'left'}),
						html.Div([
							html.H5('Magnitude ( > )')
						], className='two columns', style={'textAlign' : 'right'}),
						html.Div([
							dcc.Dropdown(
								id='magnitude',
								options=[
									{'label' : s, 'value' : s} for s in measuring_mags
								],
								value=2
							)
						], className='two columns', style={'textAlign' : 'center'})
					], className='row', style={'textAlign' : 'center'}),
					html.Div([
						html.Div([
							dcc.Graph(id='maplayout'),
						]),
					])
				]),
				html.Div([
					html.Div([
						html.H6('Significance of Magnitude', style={'textAlign' : 'center'}),
						html.Div([
							html.P("Magnitude is the best available estimate of earthquake's size. It is the measure of the size of an earthquake at its source. At the same distance from the earthquake, the amplitude of the seismic waves from which the magnitude is determined are approximately 10 times as large during a magnitude 5 earthquake as during a magnitude 4 earthquake."
								),
							html.P("Earthquakes are commonly complex events that release energy over a wide range of frequencies and at varying amounts as faulting or rupture process occurs. The various types of magnitude measure different aspects of the seismic radiation.")
						], style={'margin-left' : 30, 'textAlign' : 'left'})
					], className='four columns'),
					html.Div([
						html.H6('Magnitude and Places', style={'textAlign' : 'center'}),
						dcc.Tabs(id='grpahs', value='bar', children=[
							dcc.Tab(label='Line Graph', value='line', children=[
								dcc.Graph(id='mag-line')
							]),
							dcc.Tab(label='Bar Graph', value='bar', children=[
								dcc.Graph(id='mag-bar')
							])
						])
					], className='eight columns')
				], className='row')
			]),
			html.Hr(),
			html.Div([
				html.Div([
					html.H6('Total Earthquakes across the states', style={'textAlign' : 'center'}),
					dcc.Graph(id='total-pie')
				], className='eight columns'),
				html.Div([
					html.H6('No: of earthquakes across each state', style={'textAlign' : 'center'})
				], className='four columns')
			], className='row'),
			html.Hr()
		]),
		dcc.Tab(label='Volcanoes', children=[
			html.Div([
				html.H3('Working in progress', style={'textAlign' : 'center'})
			])
		]),
		dcc.Tab(label='Floods', children=[
			html.Div([
				html.H3('Working in progress', style={'textAlign' : 'center'})
			])
		])
	]),
	html.Div(id='show-content'),
])

def grab_appropriate_data(type_data, filter_mag):
	quake_data = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' + str(type_data) + '.csv')
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
	Output('maplayout', 'figure'),
	[Input('type-data', 'value'), Input('magnitude', 'value')]
)
def show_earthquakes(type_data, filter_mag):
	try:
		grab_appropriate_data(type_data, filter_mag)
		eq = pd.read_csv('filtered_mags.csv')
		lats = list(eq['latitude'])
		lons = list(eq['longitude'])
		places = list(eq['place'])
		mags = ['Magnitude : ' + str(i) for i in eq['mag']]
		mag_size = [float(i) * radius_multiplier['outer'] for i in eq['mag']]
		depth_size = [float(i) * radius_multiplier['inner'] for i in eq['mag']]
		depths = ['Depth : ' + str(i) for i in eq['depth']]

		info = [places[i] + '<br>' + mags[i] + '<br>' + depths[i] for i in range(len(places))]

		quakes = [
			go.Scattermapbox(
				lat=lats, lon=lons, mode='markers',
				marker=dict(
					size=mag_size, color=eq['mag'], opacity=1,
					colorscale=colorscale_magnitude,
				),
				text=info, hoverinfo='text', showlegend=False
			),
			go.Scattermapbox(
				lat=lats, lon=lons, mode='markers',
				marker=dict(
					size=depth_size, color=eq['depth'], opacity=1,
					colorscale=colorscale_depth,
				),
				hoverinfo='skip', showlegend=False
			)
		]

		layout = go.Layout(
			height=680, autosize=True, showlegend=False,
		  hovermode='closest',
		  geo=dict(
			  projection=dict(type="equirectangular"),
		  ),
		  mapbox=dict(
		    accesstoken=map_token, bearing=1,
				center=dict(
					lat=lats[0], lon=lons[0]
				),
				pitch=0, zoom=1, style='dark'
			)
		)
		return {'data' : quakes, 'layout' : layout}
	except Exception as e:
		print(str(e))

@app.callback(
	Output('mag-line', 'figure'),
	[Input('type-data', 'value'), Input('magnitude', 'value')]
)
def line_diagram(type_data, filter_mag):
	grab_appropriate_data(type_data, filter_mag)
	eq = pd.read_csv('filtered_mags.csv')
	traces = []
	traces.append(
		go.Scatter(
			x=list(eq['place']), y=list(eq['mag']),
			name='Magnitude Places', mode='lines+markers'
		)
	)
	return {'data' : traces}

@app.callback(
	Output('mag-bar', 'figure'),
	[Input('type-data', 'value'), Input('magnitude', 'value')]
)
def bar_diagram(type_data, filter_mag):
	grab_appropriate_data(type_data, filter_mag)
	eq = pd.read_csv('filtered_mags.csv')
	magnis = list(eq['mag'])
	max_mag = max(magnis)
	min_mag = min(magnis)
	bar_highlight = []
	for m in magnis:
		if m == max_mag:
			bar_highlight.append('rgba(222,45,38,0.8)')
		elif m == min_mag:
			bar_highlight.append('rgb(40,180,99)')
		else:
			bar_highlight.append('rgb(41,128,185)')
	traces = []
	traces.append(
		go.Bar(
			x=list(eq['place']), y=magnis, name='Magnitude Places',
			marker=dict(
				color=bar_highlight,
			)
		)
	)
	return {'data' : traces}

@app.callback(
	Output('total-pie', 'figure'),
	[Input('type-data', 'value'), Input('magnitude', 'value')]
)
def pie_diagram(type_data, filter_mag):
	grab_appropriate_data(type_data, filter_mag)
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
	return {'data' : traces}

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
for css in external_css:
	app.css.append_css({'external_url' : css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
	app.scripts.append_script({'external_url' : js})

if __name__ == '__main__':
	app.run_server(debug=True)

