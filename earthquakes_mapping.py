import plotly.graph_objs as go

with open('map_token.txt', 'r') as mk:
	map_token = mk.read()

def MapScatter(this_lat, this_lon, this_size, this_color, this_cs, this_text):
	return go.Scattermapbox(
		lat=this_lat, lon=this_lon,	mode='markers',
		marker=dict(
			size=this_size, color=this_color, opacity=1,
			colorscale=this_cs,
		),
		text=this_text, hoverinfo='text', showlegend=False
	)

def MapLayout(this_height, this_l, this_r, this_t, this_b, this_c_lat, this_c_lon, this_zoom):
	return go.Layout(
		height=this_height, autosize=True, showlegend=False,
	  hovermode='closest',
	  margin=dict(l=this_l, r=this_r, t=this_t, b=this_b),
	  geo=dict(
	  	projection=dict(type="equirectangular"),
	  ),
	  mapbox=dict(
	    accesstoken=map_token, bearing=1,
			center=dict(lat=this_c_lat, lon=this_c_lon),
			pitch=0, zoom=this_zoom, 
			style='mapbox://styles/chaotic-enigma/cjpbbmuzmadb12spjq5n07nd1'
		)
	)