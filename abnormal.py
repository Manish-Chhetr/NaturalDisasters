import dash
import pandas as pd
import simplejson as js
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input

with open('map_token.txt', 'r') as mk:
	map_token = mk.read()

app = dash.Dash(__name__)
app.config['suppress_callback_exceptions'] = True

app.layout = html.Div([
	html.H3('Earthquake Data Plotting', style={'textAlign' : 'center'}),
	html.Div([
		html.Div([
			html.H5('Type of the data')
		], className='six columns', style={'textAlign' : 'right'}),
		html.Div([
			dcc.Dropdown(
				id='type-data',
				options=[
					{'label' : 'Past Hour', 'value' : 'all_hour'},
					{'label' : 'Past Day', 'value' : 'all_day'},
					{'label' : 'Past Week', 'value' : 'all_week'},
					{'label' : 'Past Month', 'value' : 'all_month'}
				],
				value='all_hour',
			)
		], className='four columns', style={'textAlign' : 'left'})
	], className='row', style={'textAlign' : 'center'}),
	html.Div([
		dcc.Graph(id='maplayout')
	])
])

def grab_location(type_data):
	earthquake_data = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/' + str(type_data) + '.csv')
	lats = []
	for i in earthquake_data['latitude']:
		lats.append(i)
	lons = []
	for i in earthquake_data['longitude']:
		lons.append(i)
	mags = []
	mag_size = []
	for i in earthquake_data['mag']:
		mags.append('Magnitude : ' + str(i))
		mag_size.append(i + 8.0)
	return lats, lons, mags, mag_size

@app.callback(
	Output('maplayout', 'figure'),
	[Input('type-data', 'value')]
)
def show_earthquakes(type_data):
	lldata = grab_location(type_data)
	lats = lldata[0]
	lons = lldata[1]
	mags = lldata[2]
	mag_size = lldata[3]

	quakes = go.Data([
		go.Scattermapbox(
			lat=lats,
			lon=lons,
			mode='markers',
			marker=dict(
				size=mag_size
			),
			text=mags,
			hoverinfo='text'
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

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
for css in external_css:
	app.css.append_css({'external_url' : css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
	app.scripts.append_script({'external_url' : js})

if __name__ == '__main__':
	app.run_server(debug=True)