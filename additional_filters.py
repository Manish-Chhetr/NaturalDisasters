import csv
import dash
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# quake_data = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_hour.csv')
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
							{'label' : 'Past Month', 'value' : 'all_month'}
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
						value=3
					)
				], className='two columns', style={'textAlign' : 'center'})
			], className='row', style={'textAlign' : 'center'}),
			html.Div([
				html.Div([
					dcc.Graph(id='maplayout'),
				]),
				html.Div([
					html.Div([
						html.H4('Significance of Magnitude'),
					], style={'textAlign' : 'center'}),
					html.Div([
						html.H6("Magnitude is the best available estimate of earthquake's size. It is the measure of the size of an earthquake at its source. At the same distance from the earthquake, the amplitude of the seismic waves from which the magnitude is determined are approximately 10 times as large during a magnitude 5 earthquake as during a magnitude 4 earthquake."
							),
						html.H6("Earthquakes are commonly complex events that release energy over a wide range of frequencies and at varying amounts as faulting or rupture process occurs. The various types of magnitude measure different aspects of the seismic radiation.")
					], style={'margin-right' : 100, 'margin-left' : 100, 'textAlign' : 'left'})
				])
			])
		]),
		html.Hr(),
		html.Div([
			html.H4('Correlation of Magnitude and depth', 
				style={'margin-right' : 100, 'margin-left' : 100, 'textAlign' : 'center'}),
			html.Div([
				dcc.Graph(id='mag-depth')
			])
		])
	])
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

		mags = []
		mag_size = []
		depth_size = []
		for i in eq['mag']:
			mags.append('Magnitude : ' + str(i))
			mag_size.append(float(i) * radius_multiplier['outer'])
			depth_size.append(float(i) * radius_multiplier['inner'])

		depths = []
		for i in eq['depth']:
			depths.append('Depth : ' + str(i))
		# print(eq['mag'].corr(eq['depth']))
		info = []
		for i in range(len(places)):
			info.append(places[i] + '<br>' + mags[i] + '<br>' + depths[i])
		quakes = go.Data([
			go.Scattermapbox(
				lat=lats,
				lon=lons,
				mode='markers',
				marker=dict(
					size=mag_size,
					colorscale=colorscale_magnitude,
					color=eq['mag'],
					opacity=1
				),
				text=info,
				hoverinfo='text',
				showlegend=False
			),
			go.Scattermapbox(
				lat=lats,
				lon=lons,
				mode='markers',
				marker=dict(
					size=depth_size,
					colorscale=colorscale_depth,
					color=eq['depth'],
					opacity=1
				),
				hoverinfo='skip',
				showlegend=False
			)
		])

		layout = go.Layout(
			height=650,
		  autosize=True,
		  showlegend=False,
		  hovermode='closest',
		  geo=dict(
			  projection=dict(type="equirectangular"),
		  ),
		  mapbox=dict(
		    accesstoken=map_token,
		  	bearing=1,
				center=dict(
					lat=lats[0],
					lon=lons[0]
				),
				pitch=0,
				zoom=1,
				style='dark'
			)
		)
		return {'data' : quakes, 'layout' : layout}
	except Exception as e:
		print(str(e))

@app.callback(
	Output('mag-depth', 'figure'),
	[Input('type-data', 'value'), Input('magnitude', 'value')]
)
def scatter_diagram(type_data, filter_mag):
	grab_appropriate_data(type_data, filter_mag)
	eq = pd.read_csv('filtered_mags.csv')
	traces = []
	traces.append(
		go.Scatter(
			x=list(eq['mag']),
			y=list(eq['depth']),
			name='Magnitude Depth Relationship',
			mode='markers'
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