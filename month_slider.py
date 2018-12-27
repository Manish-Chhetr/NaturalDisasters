import csv
import time
import dash
import base64
import pandas as pd
import datetime as dt
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

logo_image = 'cartoon-globe.png'
en_logo = base64.b64encode(open(logo_image, 'rb').read())

with open('map_token.txt', 'r') as mk:
	map_token = mk.read()

colorscale_magnitude = [
	[0, '#a303b9'],	[0.25, '#ea6402'],[0.5, '#fa73a0'],	
	[0.75, '#f03b20'], [1, '#bd0026'],
]

radius_multiplier = {'inner' : 1.5, 'outer' : 3}

entire_month = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv')

# def read_data():
# 	all_month = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.csv')
# 	return all_month

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

def extract_places_regions(eq_places):
	# taking only last name from each place
	end_names = []
	for p in eq_places:
		fplp = p.split(', ')
		if len(fplp) == 2:
			end_names.append(fplp[1])
		if len(fplp) == 1:
			end_names.append(fplp[0])
	splaces = list(set(end_names))
	return splaces

def place_wise_extraction(place_name):
	all_month = entire_month.copy()
	all_places = all_month['place'].tolist()
	u_regions = extract_places_regions(all_places) # specific last name
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
	
	with open('place_data.csv', 'w') as pdata:
		writer = csv.writer(pdata)
		writer.writerows(place_data)

# ['Canada', 'East Timor', 'Montenegro', 'Wyoming', 'Illinois', 'Argentina', 'Bolivia', 'Louisiana', 'Kuril Islands', 'Texas', 'Northern Mid-Atlantic Ridge', 'Gulf of Alaska', 'Kansas', 'Chagos Archipelago region', 'Guatemala', 'Southern Mid-Atlantic Ridge', 'Dominica', 'Alaska', 'Southern East Pacific Rise', 'Greenland', 'South of the Kermadec Islands', 'Missouri', 'Wallis and Futuna', 'New Zealand', 'Kyrgyzstan', 'Pakistan', 'Galapagos Triple Junction region', 'North Atlantic Ocean', 'Guam', 'India', 'Off the coast of Oregon', 'Owen Fracture Zone region', 'Tajikistan', 'Turkey', 'Afghanistan', 'Northern Mariana Islands', 'Solomon Islands', 'Washington', 'North of Severnaya Zemlya', 'Mongolia', 'South of the Fiji Islands', 'Somalia', 'Peru', 'Vanuatu', 'Arizona', 'Ascension Island region', 'Oregon', 'Pacific-Antarctic Ridge', 'Carlsberg Ridge', 'Montana', 'China', 'Massachusetts', 'Dominican Republic', 'Banda Sea', 'Tonga', 'Indonesia', 'Hawaii', 'Reykjanes Ridge', 'Sweden', 'British Virgin Islands', 'Fiji region', 'Russia', 'Mauritius', 'Bering Sea', 'Fiji', 'South Georgia and the South Sandwich Islands', 'North Carolina', 'Japan', 'Japan region', 'Maine', 'Falkland Islands', 'U.S. Virgin Islands', 'Oklahoma', 'Costa Rica', 'Arkansas', 'New Mexico', 'Ecuador', 'Australia', 'Iran', 'Off the coast of Ecuador', 'El Salvador', 'Northern East Pacific Rise', 'Federated States of Micronesia region', 'California', 'Chile', 'Puerto Rico', 'Haiti', 'Eastern Greenland', 'NV', 'Georgia', 'West Chile Rise', 'Pennsylvania', 'Philippines', 'Albania', 'Southeast of Easter Island', 'Mid-Indian Ridge', 'Colorado', 'Southeast Indian Ridge', 'Lebanon', 'Uzbekistan', 'North of Ascension Island', 'Colombia', 'Taiwan', 'Nevada', 'Cyprus', 'Southwest of Africa', 'Italy', 'Prince Edward Islands region', 'Nepal', 'Democratic Republic of the Congo', 'Anguilla', 'Venezuela', 'Idaho', 'South Sandwich Islands', 'Utah', 'Central Mid-Atlantic Ridge', 'Papua New Guinea', 'Zimbabwe', 'New Hampshire', 'offshore Azerbaijan', 'Central East Pacific Rise', 'CA', 'Vermont', 'Mayotte', 'New Caledonia', 'Nebraska', 'Burma', 'Mexico', 'Nicaragua', 'Serbia', 'Tennessee', 'Greece']

# place_wise_extraction('')

timestamps = get_dates_sorted()
date_start = dt.datetime.strptime(timestamps[0], '%Y-%m-%d')
date_end = dt.datetime.strptime(timestamps[len(timestamps)-1], '%Y-%m-%d')

app.layout = html.Div([
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

@app.callback(
	Output('map-daily-output', 'children'),
	[Input('all-thirty', 'start_date'), Input('all-thirty', 'end_date'),
		Input('search-here', 'value')]
)
def display_quakes_day(start, end, query):
	try:
		query_value = query
		start = dt.datetime.strptime(start, '%Y-%m-%d')
		end = dt.datetime.strptime(end, '%Y-%m-%d')
		year, month, day = [start.year, start.month, start.day]

		lats = []; lons = []; places = []; info = []
		mags = []; mag_size = []; depth_size = []; depths = []

		if query_value == '':
			zoom_value = 1
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
		else:
			zoom_value = 3
			place_wise_extraction(query_value)
			eq = pd.read_csv('place_data.csv')
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

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
for css in external_css:
	app.css.append_css({'external_url' : css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
	app.scripts.append_script({'external_url' : js})

if __name__ == '__main__':
	app.run_server(debug=True)
