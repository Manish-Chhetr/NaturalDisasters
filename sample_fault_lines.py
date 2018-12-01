import dash
import pandas as pd
import plotly.graph_objs as go
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)

with open('map_token.txt', 'r') as mk:
	map_token = mk.read()

app.layout = html.Div([
	dcc.Checklist(
		id='display-plates',
		options=[{'label' : 'Show Fault Lines', 'value' : 'Plates'}],
		values=['Plates']
	),
	dcc.Graph(id='place-fault')
])

@app.callback(
	Output('place-fault', 'figure'),
	[Input('display-plates', 'values')]
)
def draw_fault_lines(values):
	tectonic_plates = pd.read_csv('all_fault_lines.csv')
	latitudes = tectonic_plates['latitudes']
	longitudes = tectonic_plates['longitudes']

	if values:
		fault_lines = [
			go.Scattermapbox(
				lat=latitudes, lon=longitudes,	mode='markers',
				text='', hoverinfo='text', showlegend=False,
				marker=dict(size=3, color='rgb(41,128,185)')
			)
		]

		layout = go.Layout(
			height=680, autosize=True, showlegend=False,
		  hovermode='closest',
		  geo=dict(
		  	projection=dict(type="equirectangular"),
		  ),
		  mapbox=dict(
		    accesstoken=map_token, 
		    bearing=1,
				# center=dict(lat=lats[0], lon=lons[0]),
				pitch=0, zoom=1, style='dark'
			)
		)
		
		return {'data' : fault_lines, 'layout' : layout}

external_css = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
for css in external_css:
	app.css.append_css({'external_url' : css})

external_js = ['https://cdnjs.cloudflare.com/ajax/libs/materialize/0.100.2/js/materialize.min.js']
for js in external_js:
	app.scripts.append_script({'external_url' : js})

if __name__ == '__main__':
	app.run_server(debug=True)