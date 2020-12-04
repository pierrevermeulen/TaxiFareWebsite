import streamlit as st
import datetime
import requests
import numpy as np
import pandas as pd
import pydeck as pdk

'''
# TaxiFareModel Prediction
'''

init_lat = 40.783
init_long = -73.966

st.sidebar.markdown("<font color='red'> Pick-up</font>", unsafe_allow_html=True)
d = st.sidebar.date_input("Pickup date", datetime.datetime.now())
t = st.sidebar.time_input('Pickup time', datetime.time(12,0))
pickup_datetime = datetime.datetime.combine(d, t)
pass_number = st.sidebar.number_input('Passenger number', min_value=1, max_value=20)
pu_lat = st.sidebar.number_input('Pickup latitude', min_value=38.0, max_value=42.0, \
    value = init_lat, format="%.5f")
pu_long = st.sidebar.number_input('Pickup longitude', min_value=-75.0, max_value=-72.0, \
    value = init_long, format="%.5f")
st.sidebar.markdown("<font color='blue'> Drop-off</font>", unsafe_allow_html=True)
do_lat = st.sidebar.number_input('Dropoff latitude', min_value=38.0, max_value=42.0, \
    value = init_lat, format="%.5f")
do_long = st.sidebar.number_input('Dropoff longitude', min_value=-75.0, max_value=-72.0, \
    value = init_long, format="%.5f")

url = 'https://taxifare.lewagon.ai/predict_fare/'
params = {'key': 'key',
    'pickup_datetime': r' '.join([str(d), str(t), 'UTC']),
    'pickup_longitude': pu_long,
    'pickup_latitude': pu_lat,
    'dropoff_longitude': do_long,
    'dropoff_latitude': do_lat,
    'passenger_count': pass_number}

if st.button('Fare prediction'):
    response = requests.get(url, params = params)
    pred = response.json()
    st.write(f"Predicted fare = {pred['prediction']:.2f}$")

df_pu = pd.DataFrame(np.array([[pu_lat, pu_long]]),
            columns=['lat', 'lon'])
df_do = pd.DataFrame(np.array([[do_lat, do_long]]),
            columns=['lat', 'lon'])
#st.map(df)
st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=init_lat,
        longitude=init_long,
        zoom = 12,
        pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df_pu,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=100,
        ),
        pdk.Layer(
            'ScatterplotLayer',
            data=df_do,
            get_position='[lon, lat]',
            get_color='[0, 30, 200, 160]',
            get_radius=100,
        )
    ],
))
