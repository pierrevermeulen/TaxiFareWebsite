import streamlit as st
import datetime
import requests
import numpy as np
import pandas as pd

'''
# TaxiFareModel Prediction
'''

d = st.date_input(
    "Pickup date", datetime.datetime.now())
t = st.time_input('Pickup time', datetime.time(12,0))

pickup_datetime = datetime.datetime.combine(d, t)
pass_number = st.number_input('Passenger number', min_value=1, max_value=20)
pu_lat = st.number_input('Pickup latitude', min_value=38.0, max_value=42.0, value = 40.783)
pu_long = st.number_input('Pickup longitude', min_value=-75.0, max_value=-72.0, value = -73.966)

do_lat = st.number_input('Dropoff latitude', min_value=38.0, max_value=42.0, value = 40.783)
do_long = st.number_input('Dropoff longitude', min_value=-75.0, max_value=-72.0, value = -73.966)

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
    df = pd.DataFrame(
            np.array([[pu_lat, pu_long], [do_lat, do_long]]),
            columns=['lat', 'lon'])
    st.map(df)
