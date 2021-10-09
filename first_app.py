

import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import numpy as np
from chart_studio.plotly import plot, iplot
import plotly.tools as tls
import plotly.graph_objs as go



'''
# The HSL project - Trustworthy Transport

We provide means to evaluate the _reliability_ of public transport in the **HSL area**.
'''


df = pd.read_csv('sample1.csv')

st.write("This is how some raw data looks like")
st.write(df.head())


df1 = df[df['trip_realtime']==True]

""" 


**Mean departure delays per transport type**  """
chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['train', 'bus', 'tram'])

st.line_chart(chart_data)



""" 


**The average delays per route for each stop**  """


stops = pd.read_csv("./Test Stops.csv")
stops = stops.query("route in ['a', 'b']")

fig = px.line_mapbox(stops, lat="lat", lon="lon", color = "route", zoom=3.5, height=300)

fig2 = px.scatter_mapbox(stops, lat="lat", lon="lon", color="delay", size="delay",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=10,
                  mapbox_style="carto-positron")

for i in range (0,1):
    fig.add_trace(fig2.data[i])

fig.update_layout(mapbox_style="stamen-terrain", mapbox_zoom=10, mapbox_center_lat = 60.2,
    margin={"r":0,"t":0,"l":0,"b":0})
fig

"""



"""

add_selectbox = st.selectbox(
    "Which public transport route you are interested in?",
    ("M1", "84", "56", "P")
)

if (add_selectbox == 'M1'):
    chart_data = pd.DataFrame(
        np.random.randn(15, 1),
        columns=['M1'])
    st.line_chart(chart_data)

if (add_selectbox == '84'):
    chart_data = pd.DataFrame(
        np.random.randn(10, 1),
        columns=['84'])
    st.line_chart(chart_data)
if (add_selectbox == '56'):
    chart_data = pd.DataFrame(
        np.random.randn(12, 1),
        columns=['56'])
    st.line_chart(chart_data)
if (add_selectbox == 'P'):
    chart_data = pd.DataFrame(
        np.random.randn(9, 1),
        columns=['P'])
    st.line_chart(chart_data)

