import dash
import base64
import dash_core_components as dcc
import dash_html_components as html
import base64 as b64

from realtime_details import measuring_mags
from historical_overview import select_countries

colors_useful = {
	'text_color' : '#154360',
	'btn_color' : '#d4e6f1',
	'light_shade_back' : '#ebf5fb',
	'bar_max_val' : 'rgba(222,45,38,0.8)',
	'bar_normal' : 'rgb(41,128,185)',
	'bar_min_val' : 'rgb(40,180,99)'
}

logo_image = 'cartoon-globe.png'
en_logo = b64.b64encode(open(logo_image, 'rb').read())

################################ layout page #####################################
##################### home page ##################
index_page = html.Div([
	html.Div([
		html.Div([
			html.H2('Earthquakes - Seismic Analysis', 
				style={'textAlign' : 'left', 'textDecoration' : 'underline'}),
			html.Div([
				html.H5('Earthquake is a sudden shaking surface of the earth creating seismic waves. They are measured in terms of magnitude that signifies the occurrence type, basically varies from those that are so weak that they cannot be felt to those that are tremendous enough to create a widespread havoc.'),
			]),
		]),
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
			html.H2('To explore the Seismic Analysis', className='eight columns', 
				style={'textAlign' : 'right'}),
			dcc.Link(html.Button('Explore here', style={'backgroundColor' : colors_useful['btn_color']}), href='/realtime_analysis-page', className='four columns', style={'margin-top' : 22, 'textAlign' : 'left'})
		], className='row', style={'margin-top' : 40}),
	], className='container', style={'backgroundColor' : '#fff', 'padding' : '30px 30px', 'boxShadow' : '8px 8px #d4e6f1', 'border' : 'thin #e5e8e8 solid', 'fontFamily' : 'Dosis, sans-serif'})

], style={'backgroundColor' : '#eaf2f8', 'padding' : '60px 60px', 'color' : colors_useful['text_color']}
# style={'background-image' : 'url(https://static.vecteezy.com/system/resources/previews/000/101/237/non_2x/free-abstract-background-11-vector.jpg)', 'background-repeat' : 'no-repeat', 'background-size' : 'cover', 'background-position' : 'center', 'padding' : '20px 20px'}

)
##################################################

##################### real time analysis ##################
realtime_analysis_layout = html.Div([

	html.Div([
		dcc.Link(html.Button('Back to Home', style={'backgroundColor' : colors_useful['btn_color']}), href='/', className='six columns', style={'textAlign' : 'left'}),
		dcc.Link(html.Button('Earthquake History', style={'backgroundColor' : colors_useful['btn_color']}), href='/earthquake_history-page', className='six columns', style={'textAlign' : 'right'})
	], className='container'),

	dcc.Interval(id='live-update', interval='300000'), # update every 5 min

	html.Div([html.H3('Seismic Data Visualization', style={'textAlign' : 'center', 'margin-top' : 30, 'margin-bottom' : 30}),
		html.Div([
			html.Div([html.H5('Occurence')], className='three columns', style={'textAlign' : 'right'}),
			html.Div([
				dcc.Dropdown(
					id='occurence_type',
					options=[
						{'label' : 'This Hour', 'value' : 'all_hour'},
						{'label' : 'Today', 'value' : 'all_day'},
						{'label' : 'Last Week', 'value' : 'all_week'},
						{'label' : 'Last Month', 'value' : 'all_month'}
					],
					value='all_day',
				)
			], className='three columns', style={'textAlign' : 'left'}),
			html.Div([html.H5('Mag above')], className='two columns', style={'textAlign' : 'right'}),
			html.Div([
				dcc.Dropdown(
					id='magnitude-drop',
					options=[{'label' : s, 'value' : s} for s in measuring_mags],
					value=3
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
			'backgroundColor' : colors_useful['light_shade_back'], 
			'padding': '10px 10px', 'margin-left' : 30, 
			'margin-right' : 30, 'margin-top' : 40
	}),

	html.Div([
		html.Div(id='map-output', className='nine columns', style={'margin-top' : 20}),
		html.Div([
			html.Div([
				html.H6('Number(s) Reported', style={'backgroundColor' : colors_useful['light_shade_back'], 'textAlign' : 'center'}),
				html.Div([
					html.Div(id='people-reports')
				], style={'overflowY' : 'scroll', 'height' : 200})
			]),
			html.Div([
				html.H6('Alert Color', style={'backgroundColor' : colors_useful['light_shade_back'], 'textAlign' : 'center'}),
				html.Div([
					html.Div(id='alert-reports')
				], style={'overflowY' : 'scroll', 'height' : 120})
			]),
			html.Div([
				html.H6('Triggered Tsunami', style={'backgroundColor' : colors_useful['light_shade_back'], 'textAlign' : 'center'}),
				html.Div([
					html.Div(id='tsunami-reports')
				], style={'overflowY' : 'scroll', 'height' : 120})
			]),
		], className='three columns', style={'margin-top' : 80, 'margin-left' : 20})
	], className='row'),

	html.Hr(),

	html.Div([
		html.Div(id='highest-mag'),
		html.Div([
			html.Div([
				html.H6('Total Earthquakes across the states',
						style={'textAlign' : 'center'}),
				html.Div(id='region-pie')
			], className='eight columns'),
			html.Div([
				html.H6('No: of earthquakes in a year', style={'textAlign' : 'center'}),
					html.Div([
						html.P("NEIC (National Earthquake Information Center) reports that 12000 - 14000 earthquakes happen each year. Smaller earthquakes of magnitude 2 occur several hundred times a day world wide and Major earthquakes of magnitude greater than 7 happen more than a once per month."),
						html.P("The largest recorded earthquake was Great Chilean Earthquake of May 22, 1960 which had a magnitude of 9.5. The great earthquake in  2004 in Sumatra, Indonesia measuring magnitude 9.1 produced Tsunamis that caused widespread disaster in 14 countries. In 2011, earthquake of japan having magnitude 9.0 also caused Tsunamis.")
					], style={'margin-right' : 25, 'margin-top' : 40})
			], className='four columns'),
		], className='row', style={'margin-top' : 40}),
		
		# html.Hr(),

		html.Div([
			html.Div([
				html.H6('Significance of Magnitude', style={'textAlign' : 'center'}),
				html.Div([
					html.P("Magnitude is the best available estimate of earthquake's size. It is the measure of the size of an earthquake at its source. At the same distance from the earthquake, the amplitude of the seismic waves from which the magnitude is determined are approximately 10 times as large during a magnitude 5 earthquake as during a magnitude 4 earthquake."),
					html.P("Earthquakes are commonly complex events that release energy over a wide range of frequencies and at varying amounts as faulting or rupture process occurs. The various types of magnitude measure different aspects of the seismic radiation.")
				], style={'margin-left' : 30, 'textAlign' : 'left'})
			], className='four columns', style={'margin-top' : 30}),
			html.Div([
				html.H6('Magnitudes of Earthquakes', style={'textAlign' : 'center'}),
				html.Div(id='mag-bar')
			], className='eight columns')
		], className='row', style={'margin-top' : 30}),
	
	])
], style={'fontFamily' : 'Dosis, sans-serif'})
##################################################################

#################### earthquake history ##########################
earth_history_layout = html.Div([

	html.Div([
		dcc.Link(html.Button('Back to Home', style={'backgroundColor' : colors_useful['btn_color']}), href='/', className='six columns', style={'textAlign' : 'left'}),
		dcc.Link(html.Button('Real Time Analysis', style={'backgroundColor' : colors_useful['btn_color']}), href='/realtime_analysis-page', className='six columns', style={'textAlign' : 'right'})
	], className='container'),

	html.Div([
		html.Div([
			html.Img(src='data:image/png;base64,{}'.format(en_logo.decode()), id='logo',
				style={'width' : 70, 'height' : 70})
		], className='three columns', style={'textAlign' : 'right'}),
		html.Div([
			html.H5('Country wise occurence')
		], className='three columns', style={'textAlign' : 'right', 'margin-top' : 15}),
		html.Div([
			dcc.Dropdown(
				id='countries-dropdown',
				options=[{'label' : k, 'value' : v} for k, v in select_countries.items()],
				value='JP',
				placeholder='Select Country: ',
			)
		], className='six columns', style={'width' : 400, 'textAlign' : 'left', 'margin-top' : 15}),
	], className='row', style={'borderBottom' : 'thin lightgrey solid', 
		'backgroundColor' : colors_useful['light_shade_back'], 
		'padding': '40px 40px', 'margin-left' : 30, 
		'margin-right' : 30, 'margin-top' : 40, 'textAlign' : 'center'
	}),
	html.Div(id='history-map')
], style={'fontFamily' : 'Dosis, sans-serif'})
##################################################################

################################ layout page #####################################
