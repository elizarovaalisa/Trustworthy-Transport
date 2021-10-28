
import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from chart_studio.plotly import plot, iplot
import plotly.tools as tls
import plotly.graph_objs as go
import matplotlib.pyplot as plt
import pickle


st.set_page_config(layout="wide")


with open('routes.pkl', 'rb') as f:
    routes_dict = pickle.load(f)
    
with open('stops.pkl', 'rb') as f:
    stops_dict = pickle.load(f)

routenames = []
routename_to_id = {}
for key in routes_dict.keys():
    name = routes_dict[key]["name"] + " - " + routes_dict[key]["headsign"]
    routenames.append(name)
    routename_to_id[name] = key


def format_delay1(stop, x):
    if np.abs(x) < 60:
        return stop + ':<br>' + str(round(x)) +' seconds early' if x < 0 else stop + ':<br>' + str(round(x)) +' seconds late'
    minutes = int(x/60)
    seconds = round(x%60)
    return stop + ':<br>' + str(minutes) +' min ' + str(seconds) +' sec early' if x < 0 else stop + ':<br>' + str(minutes) +' min ' + str(seconds) +' sec late'


legend_SUPER_LATE = 'More than 3 minutes late'
legend_LATE = 'More than 1 minute late but less than 3 minutes late'
legend_EARLY = 'Delayed or early by less than 1 minute'
legend_SUPER_EARLY = 'More than 1 minute early'

def classify_delay(x):
    if x < -60:
        return legend_SUPER_EARLY
    if x < 60:
        return legend_EARLY
    if x < 180:
        return legend_LATE
    return legend_SUPER_LATE

color_line = '#072ac8'
color_stop = '#072ac8'
color_delay_SUPER_LATE = 'purple'      # dark purple
color_delay_LATE = 'blue'            # light purple
color_delay_EARLY = 'pink'           # orange
color_delay_SUPER_EARLY = 'orange'     # red

width_line = 2.8 

size_stop = 5
opacity_stop = 0.9

max_size_delay = 12


def plot_map_for_pattern_id(pattern_id):
    # get delays for the pattern
    route = routes_dict[pattern_id]
    # get location of the stops
    name = []
    lat = []
    lon = []
    for stop_id in route['stops_id']:
        stop = stops_dict[stop_id]
        name.append(stop['name'])
        lat.append(stop['lat'])
        lon.append(stop['lon'])

    d = pd.DataFrame({
        'delay': route['delays'], 
        'name': name,
        'lat': lat,
        'lon': lon
    })
    
    d['color'] = [classify_delay(i) for i in d['delay']]
    d['delay_text'] = [format_delay1(d.name[i], d.delay[i]) for i in range(d.shape[0])]
    d['delay'] = np.abs(d['delay'])
    
    # print(d)
    
    fig = px.line_mapbox(d, lat="lat", lon="lon")
    fig.update_traces(line=dict(color=color_line, width=width_line),
                      hoverinfo = 'skip',
                      hovertemplate = None
                     )
    
    fig_stops = px.scatter_mapbox(d, lat="lat", lon="lon")
    fig_stops.update_traces(marker=dict(color=color_stop, size=size_stop), 
                            hoverinfo = 'skip', 
                            hovertemplate = None
                           )
    for i in range(len(fig_stops.data)):
        fig.add_trace(fig_stops.data[i])

    fig_delays = px.scatter_mapbox(d, lat="lat", lon="lon",  size="delay", 
                                   size_max = max_size_delay,
                                   opacity = opacity_stop,
                                   color="color", color_discrete_map = {
                                       legend_SUPER_LATE : color_delay_SUPER_LATE,
                                       legend_LATE : color_delay_LATE,
                                       legend_EARLY : color_delay_EARLY,
                                       legend_SUPER_EARLY : color_delay_SUPER_EARLY
                                   },
                                   hover_name = 'delay_text', hover_data = { 
                                       "delay": False,
                                       'lat' : False,
                                       'lon': False,
                                       'color': False,
                                       'delay_text': False
                                   })
    
    for i in range(len(fig_delays.data)):
        fig.add_trace(fig_delays.data[i])
    
    fig.update_layout(
        mapbox_style="stamen-terrain", 
        mapbox_zoom=10.6,
        margin={"r":0,"t":0,"l":0,"b":0},
        height=600, width = 600
    )
    fig


def stacked_mode():
    fig = go.Figure()
    template = '%{x}%'
    
    fig.add_trace(go.Bar(
        y=['Tram', 'Metro', 'Train', 'Bus'],
        x=[6.68, 1.66, 0.22, 5.63],
        name='More than 1 minute early',
        orientation='h',
        marker=dict(color='orange'),
        hovertemplate = template
    ))

    fig.add_trace(go.Bar(
        y=['Tram', 'Metro', 'Train', 'Bus'],
        x=[51.95, 64.63, 53.51, 48.06],
        name='Delayed or early by less than 1 minute',
        orientation='h',
        marker=dict(color='pink'),
        hovertemplate = template
    ))

    fig.add_trace(go.Bar(
        y=['Tram', 'Metro', 'Train', 'Bus'],
        x=[29.59, 32.30, 36.69, 32.22],
        name='More than 1 minute late but less than 3 minutes late',
        orientation='h',
        marker=dict(color='blue'),
        hovertemplate = template
    ))

    fig.add_trace(go.Bar(
        y=['Tram', 'Metro', 'Train', 'Bus'],
        x=[11.77, 1.42, 9.58, 14.08],
        name='More than 3 minutes late',
        orientation='h',
        marker=dict(color='purple'),
        hovertemplate = template
    ))

    fig.update_layout(barmode='stack', bargap=0.6, autosize=False,
        width=900,
        height=280,
        margin={"r":10,"t":10,"l":10,"b":10},
        legend={'traceorder':'normal'})
    fig

def stacked_week():
    fig = go.Figure()
    template = '%{x}%'
    width = 0.4

    fig.add_trace(go.Bar(
        y=['Weekend', 'Weekday'],
        x=[4.05, 5.96],
        name='More than 1 minute early',
        orientation='h',
        marker=dict(color='orange'),
        hovertemplate = template,
        width = width
    ))

    fig.add_trace(go.Bar(
        y=['Weekend', 'Weekday'],
        x=[47.25, 49.16],
        name='Delayed or early by less than 1 minute',
        orientation='h',
        marker=dict(color='pink'),
        hovertemplate = template,
        width = width
    ))

    fig.add_trace(go.Bar(
        y=['Weekend', 'Weekday'],
        x=[34.44, 31.48],
        name='More than 1 minute late but less than 3 minutes late',
        orientation='h',
        marker=dict(color='blue'),
        hovertemplate = template,
        width = width
    ))

    fig.add_trace(go.Bar(
        y=['Weekend', 'Weekday'],
        x=[14.27, 13.39],
        name='More than 3 minutes late',
        orientation='h',
        marker=dict(color='purple'),
        hovertemplate = template,
        width = width
    ))

    fig.update_layout(barmode='stack', bargap = 0, autosize=False,
        width=900,
        height=150,
        margin={"r":10,"t":10,"l":10,"b":10},
        legend={'traceorder':'normal'})
    fig




d = pd.read_csv('all_delays.csv', sep = ';')
d['hour'] = d['hour'].astype(str)  

def web_format_delay(time, x):
    if np.abs(x) < 60:
        return 'At ' + str(time) + ':00' + '<br>' + str(round(x)) + ' seconds early' if x < 0 else 'At ' + str(time) + ':00' + '<br>' + str(round(x)) +' seconds late'
    minutes = int(x/60)
    seconds = round(x%60)
    return 'At ' + str(time) + ':00' + '<br>' + str(minutes) + ' min ' + str(seconds) +' sec early' if x < 0 else 'At ' + str(time) + ':00' + '<br>' + str(minutes) +' min ' + str(seconds) +' sec late'

def webchart(d, time, modes):
    fig = go.Figure()
    mode = 'lines+markers'
    
    for t in time:
        for m in modes:
            column = t + '_' + m
            text = [web_format_delay(d.hour[i], d[column][i]) for i in range(d.shape[0])]
            fig.add_trace(go.Scatterpolar(
                r=d[column],
                theta=d['hour'],
                mode = mode,
                name = m + " , " + t,
                hovertext = text,
                hoverinfo = 'text'
            ))
    fig.update_layout(
        showlegend=True,
        width=700, height=500,
        margin={"r":10,"t":10,"l":10,"b":10},
        #title='Average delay on weekday and weekend in seconds from 00.00 to 23.59',
    )
    
    fig


st.title("The HSL project - Trustworthy Transport")

st.subheader("Evaluating the _reliability_ of public transport in the HSL area ")

""" 


** A Streamlit web app by Data Science students at University of Helsinki **

"""

st.write("#")

row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3, row0_3 = st.columns((.1, 1, .1, 0.5, .1,2))


row1_1,row1_2,row1_3,row1_4 = st.columns(4)
with row0_1:
    selected_route = st.selectbox(
        'Select a route:',
        routenames)
    plot_map_for_pattern_id(routename_to_id[selected_route])


with row0_3:
    """
    This website allows you to check how reliably the public transport operates within the HSL area.

    Select the route that you use on the left, and our interactive map will show you the average delays for
    your route, stop by stop.
    
    Below you can see how likely trams, buses, trains and metros are to arrive to their stop late or early,
    and how the delays overall look like during the weekend and weekdays.

    If you scroll down, you can check the timeliness of the transport types (buses, trains, trams and metros) during different
    times of the day and week. 

    Enjoy your journey!
    """
    st.write("#")
    stacked_mode()
    stacked_week()




cols = st.columns(4)

#row1_spacer1, row1_1, row1_spacer2, row1_2, row1_spacer3 = st.columns(
#    (.1, 0.2, .8, 0.5, .1))
row0_spacer1, row0_1, row0_spacer2, row0_2, row0_spacer3, row0_3, row0_spacer4, row0_4 = st.columns(
    (.1, 0.9, .1, 3, .1 , 3, .1,1))

weektimes = []
modelist = []
with row0_1:
    """Select mode of transport:"""
    all = st.checkbox('all')
    if all:
        modelist.append("all")
    bus = st.checkbox('bus')
    if bus:
        modelist.append("bus")
    train = st.checkbox('train')
    if train:
        modelist.append("train")
    metro = st.checkbox('metro')
    if metro:
        modelist.append("metro")
    tram = st.checkbox('tram')
    if tram:
        modelist.append("tram")


with row0_2:
    st.write("#")
    "Select time of the week:"
    weekdays = st.checkbox('Weekdays')
    if weekdays:
        weektimes.append("weekday")
    weekend = st.checkbox('Weekend')
    if weekend:
        weektimes.append("weekend")
    wholeweek = st.checkbox('Whole week')
    if wholeweek:
        weektimes.append("all")
    
    if not all and not bus and not train and not tram and not weekdays and not weekend and not wholeweek:

        webchart(d, time = ["all"], modes = ["all"])
    else:
        webchart(d, time = weektimes, modes = modelist)




