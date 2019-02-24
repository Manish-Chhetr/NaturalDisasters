import dash
import base64
import dash_core_components as dcc
import dash_html_components as html
import base64 as b64

from historical_overview import (select_countries, show_histogram, show_boxplot, year_wise_frequency)

colors_useful = {
	'text_color' : '#154360',
	'bar_max_val' : 'rgba(222,45,38,0.8)',
	'bar_normal' : 'rgb(41,128,185)',
	'bar_min_val' : 'rgb(40,180,99)',
	'symmetry' : '#d0ece7',
	'rev_symmetry' : '#fff',
	'danger' : '#fc131a',
	'loc_color' : '#d35400',
	'report_color' : '#8e44ad',
	'tsunami_color' : '#0240da'
}

globe_image = 'cartoon-globe.png'
en_globe = b64.b64encode(open(globe_image, 'rb').read())

main_logo = 'Quake_Logo.png'
en_main_logo = b64.b64encode(open(main_logo, 'rb').read())

################################ layout page #####################################
##################### home page ##################
index_page = html.Div([
	html.Div([
		html.Div([
			html.Div([
				html.H2('Earthquake Tracking System', 
					style={'textAlign' : 'left', 'textDecoration' : 'underline', 'margin-top' : 50}),
				html.H5('Earthquake is a sudden shaking surface of the earth creating seismic waves. They are measured in terms of magnitude that signifies the occurrence type, basically varies from those that are so weak that they cannot be felt to those that are tremendous enough to create a widespread havoc.', style={'margin-right' : 20}),
			], className='eight columns'),
			html.Div([
				html.Img(src='data:image/png;base64,{}'.format(en_main_logo.decode()), style={'width' : 270, 'height' : 270})
			], style={'textAlign' : 'left', 'margin-top' : 50}, className='four columns')
		], className='row', style={'margin-top' : -30}),
		html.Div([
			html.Div([
				html.Div([html.H2('National Earthquake Information Center', style={'textDecoration' : 'underline'})]),
				html.Div([
					html.H5('NEIC (National Earthquake Information Center) is a part of United States Geological Survey (USGS) located in the campus of the Colorado School of Mines. The NEIC has three main missions:'),
					html.Ul([
						html.H6(html.Li('Determine the location and size of all significant earthquakes that occur worldwide.')),
						html.H6(html.Li('Provide an extensive seismic database to scientists for doing scientific research.')),
						html.H6(html.Li('Improve the ability to locate earthquakes and understand its mechanism.'))
					], className='container'),
				]),
				html.Div([
					html.H5('This reports that 12000 - 14000 earthquakes happen each year.'),
					html.Ul([
						html.H6(html.Li('Smaller earthquakes of magnitude 2 occur several hundred times a day world wide.')),
						html.H6(html.Li('Major earthquakes of magnitude greater than 7 happen more than a once per month.'))
					], className='container')
				]),
			], style={'margin-top' : 40}),

			html.Div([
				html.Div([html.H2('Major Earthquakes', style={'textDecoration' : 'underline'})]),
				html.Div([
					html.Ul([
						html.H6(html.Li('The Great Chilean Earthquake of May 22, 1960 had a magnitude of 9.5.')),
						html.H6(html.Li('The earthquake of Sumatra and Indonesia in 2004 had a magnitude of 9.1.')),
						html.H6(html.Li('The earthquake of Japan in 2011 had a magnitude of 9.0.'))
					]),
				])
			], style={'margin-top' : 40})
		]),

		html.Div([
			html.H2('To explore the Real time tracking', className='eight columns', 
				style={'textAlign' : 'right'}),
			dcc.Link(html.Button('Explore here', style={'backgroundColor' : colors_useful['symmetry'], 'color' : colors_useful['text_color']}), href='/realtime_tracking-page', className='four columns', style={'margin-top' : 22, 'textAlign' : 'left'})
		], className='row', style={'margin-top' : 40}),
	], className='container', style={'backgroundColor' : colors_useful['rev_symmetry'], 'padding' : '30px 30px', 'boxShadow' : '8px 8px #aed6f1', 'border' : 'thin #e5e8e8 solid', 'fontFamily' : 'Dosis, sans-serif'})

], style={'backgroundColor' : colors_useful['symmetry'], 'padding' : '40px 40px', 'color' : colors_useful['text_color']}
)
##################################################

##################### real time Tracking ##################
realtime_tracking_layout = html.Div([

	html.Div([
		dcc.Link(html.Button('Back to Home', style={'backgroundColor' : colors_useful['rev_symmetry'], 'color' : colors_useful['text_color'], 'margin-top' : 25}), href='/', className='five columns', style={'textAlign' : 'center'}),
		html.Img(src='data:image/png;base64,{}'.format(en_main_logo.decode(), id='main-logo'), className='two columns', style={'width' : 90, 'height' : 90, 'textAlign' : 'center'}),
		dcc.Link(html.Button('Earthquake History', style={'backgroundColor' : colors_useful['rev_symmetry'], 'color' : colors_useful['text_color'], 'margin-top' : 25}), href='/earthquake_history-page', className='five columns', style={'textAlign' : 'center'})
	], className='row', style={'backgroundColor' : colors_useful['symmetry'], 'padding' : '5px 5px', 'margin-right' : 15, 'margin-left' : 15, 'textAlign' : 'center'}),

	dcc.Interval(id='live-update', interval='300000'), # update every 5 min

	html.Div([
		html.Div([
			html.Div([html.H5('Occurence')], className='two columns', style={'textAlign' : 'center'}),
			html.Div([
				dcc.Dropdown(
					id='occurence_type',
					options=[
						{'label' : 'This Hour', 'value' : 'all_hour'},
						{'label' : 'Yesterday', 'value' : 'all_day'},
						{'label' : 'Last Week', 'value' : 'all_week'},
					],
					value='all_day',
				)
			], className='two columns'),
			html.Div([html.H5('Magnitude (+)')], className='two columns'),
			html.Div([dcc.Dropdown(id='magnitude-drop')], className='two columns', 
				style={'textAlign' : 'center'}),
			html.Div([html.H5('Region')], className='one columns'),
			html.Div([dcc.Dropdown(id='region-options')], className='three columns')
		], className='row', 
		style={'margin-right' : 50, 'margin-left' : 30, 'margin-bottom' : 10, 'margin-top' : 20}),
	], style={'borderBottom' : 'thin lightgrey solid', 
			'backgroundColor' : colors_useful['symmetry'], 
			'padding': '5px 5px', 'margin-left' : 20, 
			'margin-right' : 20, 'margin-top' : 10,
	}),

	html.Div(id='highest-mag', style={'margin-top' : 20}),

	html.Div([
		html.Div(id='map-output', className='nine columns', style={'margin-top' : 5}),
		html.Div([
			html.Div([
				html.H6('Number(s) Reported', style={'backgroundColor' : colors_useful['symmetry'], 'textAlign' : 'center'}),
				html.Div([
					html.Div(id='people-reports')
				], style={'overflowY' : 'scroll', 'height' : 200})
			]),
			html.Div([
				html.H6('Alert Color', style={'backgroundColor' : colors_useful['symmetry'], 'textAlign' : 'center'}),
				html.Div([
					html.Div(id='alert-reports')
				], style={'overflowY' : 'scroll', 'height' : 150})
			]),
			html.Div([
				html.H6('Triggered Tsunami', style={'backgroundColor' : colors_useful['symmetry'], 'textAlign' : 'center'}),
				html.Div([
					html.Div(id='tsunami-reports')
				], style={'overflowY' : 'scroll', 'height' : 130})
			]),
		], className='three columns', style={'margin-top' : 30, 'margin-left' : 20})
	], className='row', style={'margin-top' : -20}),

	html.Div([
		html.Div([
			html.Div([
				html.H6('Total Earthquakes across the World',	style={'textAlign' : 'center'}),
				html.Div(id='region-pie')
			], className='eight columns'),
			html.Div([
				html.H6('No: of earthquakes in a year', style={'textAlign' : 'center', 'backgroundColor' : colors_useful['symmetry'], 'margin-left' : 30, 'margin-right' : 30}),
					html.Div([
						html.P("NEIC (National Earthquake Information Center) reports that 12000 - 14000 earthquakes happen each year. Smaller earthquakes of magnitude 2 occur several hundred times a day world wide and Major earthquakes of magnitude greater than 7 happen more than a once per month."),
						html.P("The largest recorded earthquake was Great Chilean Earthquake of May 22, 1960 which had a magnitude of 9.5. The great earthquake in  2004 in Sumatra, Indonesia measuring magnitude 9.1 produced Tsunamis that caused widespread disaster in 14 countries. In 2011, earthquake of japan having magnitude 9.0 also caused Tsunamis.")
					], style={'margin-right' : 25, 'margin-top' : 20})
			], className='four columns'),
		], className='row', style={'margin-top' : 20}),

		html.Div([
			html.Div([
				html.H6('Significance of Magnitude', style={'textAlign' : 'center', 'backgroundColor' : colors_useful['symmetry'], 'margin-left' : 30, 'margin-right' : 30}),
				html.Div([
					html.P("Magnitude is the best available estimate of earthquake's size. It is the measure of the size of an earthquake at its source. At the same distance from the earthquake, the amplitude of the seismic waves from which the magnitude is determined are approximately 10 times as large during a magnitude 5 earthquake as during a magnitude 4 earthquake."),
					html.P("Earthquakes are commonly complex events that release energy over a wide range of frequencies and at varying amounts as faulting or rupture process occurs. The various types of magnitude measure different aspects of the seismic radiation.")
				], style={'margin-left' : 30, 'textAlign' : 'left', 'margin-top' : 20})
			], className='four columns', style={'margin-top' : 20}),
			html.Div([
				html.Div([
					dcc.Tabs(id='mag-depth-tab', children=[
						dcc.Tab(label='Bar / Contour Plot', children=[
							html.Div(id='mag-bar')
						]),
						dcc.Tab(label='Magnitude - Depth Relationship', children=[
							html.Div(id='mag-depth-relation')
						])
					])
				])
			], className='eight columns', style={'margin-top' : 20})
		], className='row', style={'margin-top' : 20}),
	
	])

], style={'fontFamily' : 'Dosis, sans-serif', 'color' : colors_useful['text_color']})
##################################################################

#################### earthquake history ##########################
earth_history_layout = html.Div([

	html.Div([
		dcc.Link(html.Button('Back to Home', style={'backgroundColor' : colors_useful['rev_symmetry'], 'color' : colors_useful['text_color'], 'margin-top' : 25}), href='/', className='five columns', style={'textAlign' : 'center'}),
		html.Img(src='data:image/png;base64,{}'.format(en_main_logo.decode(), id='main-logo'), className='two columns', style={'width' : 90, 'height' : 90, 'textAlign' : 'center'}),
		dcc.Link(html.Button('Real Time Tracking', style={'backgroundColor' : colors_useful['rev_symmetry'], 'color' : colors_useful['text_color'], 'margin-top' : 25}), href='/realtime_tracking-page', className='five columns', style={'textAlign' : 'center'})
	], className='row', style={'backgroundColor' : colors_useful['symmetry'], 'padding' : '5px 5px', 'margin-right' : 15, 'margin-left' : 15, 'textAlign' : 'center'}),

	html.Div([
		dcc.Tabs(id='hml-quake-tab', children=[
			dcc.Tab(label='History (1965-2016)', children=[
				html.Div([
					html.Div([
						html.Img(src='data:image/png;base64,{}'.format(en_globe.decode()),
							style={'width' : 70, 'height' : 70})
					], className='one columns', style={'margin-top' : 10}),
					html.Div([
						html.H5('Country wise occurence')
					], className='three columns', style={'textAlign' : 'left', 'margin-top' : 20}),
					html.Div([
						dcc.Dropdown(
							id='countries-dropdown',
							options=[{'label' : k, 'value' : v} for k, v in select_countries.items()],
							value='JP',
							placeholder='Select Country: ',
						)
					], className='four columns', style={'width' : 400, 'textAlign' : 'left', 'margin-top' : 25}),
					html.Div([html.H5('Year')], className='one columns', style={'margin-top' : 20}),
					html.Div([dcc.Dropdown(id='history-year-dropdown')], 
						className='two columns', style={'margin-top' : 25})
				], className='row', style={'borderBottom' : 'thin lightgrey solid', 
					'backgroundColor' : colors_useful['symmetry'], 
					'padding': '5px 5px', 'margin-top' : 20, 'textAlign' : 'center',
				}),
				html.Div(id='history-map'),
				html.Div([
					html.Div([
						html.H6('Intensity and overview of the earthquake magnitudes',
							style={'textAlign' : 'center', 'backgroundColor' : colors_useful['symmetry'], 'padding' : '10px 10px'}),
						html.Div([dcc.Graph(id='histo-mag', figure=show_histogram())], className='five columns'),
						html.Div([dcc.Graph(id='box-mag', figure=show_boxplot())], className='five columns')
					], className='row', style={'textAlign' : 'center'}),
					html.Div([
						html.H6('Frequency of the occurence yearly wise', 
							style={'textAlign' : 'center', 'backgroundColor' : colors_useful['symmetry'], 'padding' : '10px 10px', 'position' : 'static'}),
						dcc.Graph(id='year-frequency', figure=year_wise_frequency())
					])
				]),
			]),
			dcc.Tab(label='Predictive Model', children=[
				html.Div([
					html.H5('Prone Countries', className='three columns', style={'textAlign' : 'right'}),
					html.Div([
						dcc.Dropdown(
							id='country-means',
							options=[
								{'label' : 'Japan', 'value' : 'JP'},
								{'label' : 'Indonesia', 'value' : 'ID'},
								{'label' : 'United States', 'value' : 'US'},
								{'label' : 'India', 'value' : 'IN'}
							],
							value='JP'
						)
					], className='three columns', style={'margin-top' : 5, 'textAlign' : 'left'}),
					html.H5('Specific Place', className='three columns', style={'textAlign' : 'right'}),
					html.Div([dcc.Dropdown(id='place-inside')
					], className='three columns', style={'margin-top' : 5, 'textAlign' : 'left'})
				], className='row', style={'borderBottom' : 'thin lightgrey solid', 
					'backgroundColor' : colors_useful['symmetry'], 
					'padding': '5px 5px', 'margin-top' : 20}
				),
				html.Div(id='quake-means-map')
			])
		])
	], style={'margin-right' : 15, 'margin-left' : 15, 'margin-top' : 20})
], style={'fontFamily' : 'Dosis, sans-serif', 'color' : colors_useful['text_color']})
##################################################################

################################ layout page #####################################
