import csv
import time
import dash
import pandas as pd
import datetime as dt
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

with open('map_token.txt', 'r') as mk:
	map_token = mk.read()

colorscale_magnitude = [
	[0, '#a303b9'],	[0.25, '#ea6402'],[0.5, '#fa73a0'],	
	[0.75, '#f03b20'], [1, '#bd0026'],
]

radius_multiplier = {'inner' : 1.5, 'outer' : 3}

def extract_month_values():
	all_month = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv')
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

app.layout = html.Div([
	html.Div([
		html.Div([html.H3('Start and End dates')],
			className='six columns', style={'textAlign' : 'right'}),
		html.Div([
			dcc.DatePickerRange(
				id='all-thirty',
				start_date=date_start,
				end_date=date_end,
				min_date_allowed=date_start,
				max_date_allowed=date_end
			)
		], className='six columns', style={'textAlign' : 'left'})
	], className='row', style={'margin-top' : 30}),

	html.Div([html.Div(id='map-daily-output')])

])

@app.callback(
	Output('map-daily-output', 'children'),
	[Input('all-thirty', 'start_date'), Input('all-thirty', 'end_date')]
)
def display_quakes_day(start, end):
	start = dt.datetime.strptime(start, '%Y-%m-%d')
	end = dt.datetime.strptime(end, '%Y-%m-%d')
	year, month, day = [start.year, start.month, start.day]

	day_wise_extraction(year, month, day)
	eq = pd.read_csv('month_day.csv')

	lats = eq['latitude'].tolist()
	lons = eq['longitude'].tolist()
	places = eq['place'].tolist()
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
			pitch=0, zoom=1, 
			style='mapbox://styles/chaotic-enigma/cjpbbmuzmadb12spjq5n07nd1'
		)
	)

	map_deisgn = html.Div([
		dcc.Graph(id='map-earthquake', figure={'data' : quakes, 'layout' : layout})
	])

	return map_deisgn

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
for css in external_css:
	app.css.append_css({'external_url' : css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
	app.scripts.append_script({'external_url' : js})

if __name__ == '__main__':
	app.run_server(debug=True)
