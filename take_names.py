import dash
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

with open('map_token.txt', 'r') as mk:
	map_token = mk.read()

eq = pd.read_csv('https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_day.csv')
places = list(eq['place'])
latitudes = list(eq['latitude'])
longitudes = list(eq['longitude'])
# print(len(eq))
# places = list(set(places))
# print(places)

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
# print(counter_places)
# print("\n")

eplaces = counter_places.keys()
# print(eplaces)

first_names = []
for p in places:
	fplp = p.split(', ')
	first_names.append(fplp[0])

seperate = []
for p in range(len(places)):
	seperate.append([places[p].split(', '), latitudes[p], longitudes[p]])
# print("\n")

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
# print(len(state_regions['Nevada']))
region_places = state_regions.keys()
region_places.remove('World Wide')
print(region_places)

def take_region_locations(state_name):
	region_names = []
	lats = []
	lons = []
	for k, v in state_regions.items():
		if k == state_name:
			details = v
			for about in details:
				region_names.append(about[0])
				lats.append(about[1])
				lons.append(about[2])
	if state_name == 'World Wide':
		for k, v in state_regions.items():
			details = v
			# print details
			for about in details:
				# print about
				region_names.append(about[0])
				lats.append(about[1])
				lons.append(about[2])
	return region_names, lats, lons

app.layout = html.Div([
	html.Div([
		html.Div([
			html.H5('Select the region', style={'textAlign' : 'right'})
		], className='four columns'),
		html.Div([
			dcc.Dropdown(
				id='state-names',
				options=[
					{'label' : s, 'value' : s} for s in state_regions.keys()
				],
				value='World Wide'
			)
		], className='four columns', style={'textAlign' : 'left'})
	], className='row', style={'textAlign' : 'center', 'margin-top' : 45}),
	html.Div([
		dcc.Graph(id='region-states')
	])
])

@app.callback(
	Output('region-states', 'figure'),
	[Input('state-names', 'value')]
)
def show_region(state_name):
	region_names, lats, lons = take_region_locations(state_name)
	regions = go.Data([
		go.Scattermapbox(
			lat=lats,
			lon=lons,
			mode='markers',
			marker=dict(
				size=10
			),
			text=region_names,
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
	return {'data' : regions, 'layout' : layout}

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
for css in external_css:
	app.css.append_css({'external_url' : css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
	app.scripts.append_script({'external_url' : js})

# if __name__ == '__main__':
# 	app.run_server(debug=True)

#['291km ESE of Gisborne']
# state_regions = []
# for p in eplaces:
# 	regions = []	
# 	for sep in seperate:
# 		if len(sep) == 2:
# 			if sep[1] == p:
# 				regions.append(sep[0])
# 		if len(sep) != 2:
# 			if sep[0] == p:
# 				regions.append(sep[0])
# 	state_regions.append({p : regions})
# print(state_regions)

