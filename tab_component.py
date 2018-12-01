import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
	html.H3('Natural Disasters', style={'textAlign' : 'center'}),
	dcc.Tabs(id='tabs-example', value='tab-2', children=[
		dcc.Tab(label='Earthquakes', value='tab-1'),
		dcc.Tab(label='Volcanoes', value='tab-2'),
		dcc.Tab(label='Floods', value='tab-3')
	]),
	html.Div(id='tabs-content-example')
])

@app.callback(
	Output('tabs-content-example', 'children'),
	[Input('tabs-example', 'value')]
)
def render_content(tab):
	if tab == 'tab-1':
		return html.Div([
			html.H4('Earthquakes Data Plotting', style={'textAlign' : 'center'}),
			dcc.Graph(
				id='eq-data',
				figure={
					'data' : [{'x' : [1, 2, 3], 'y' : [3, 2, 1], 'type' : 'bar'}]
				}
			)
		])
	elif tab == 'tab-2':
		return html.Div([
			html.H4('Volcanoes Data Plotting', style={'textAlign' : 'center'}),
			dcc.Graph(
				id='vol-data',
				figure={
					'data' : [{'x' : [1, 2, 3], 'y' : [5, 10, 6], 'type' : 'bar'}]
				}
			)
		])
	elif tab == 'tab-3':
		return html.Div([
			html.H4('Floods Data Plotting', style={'textAlign' : 'center'}),
			dcc.Graph(
				id='flood-data',
				figure={
					'data' : [{'x' : [1, 2, 3], 'y' : [6, 3, 9], 'type' : 'bar'}]
				}
			)
		])

if __name__ == '__main__':
	app.run_server(debug=True)