import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import pydeck as pdk

DATE_TIME = 'date/time'
DATA_URL = ('http://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz')

st.title('Uber Pickups in NYC')
st.markdown(
        '''
        This is a demo of a streamlit app that shows the Uber pickups
        geographical distribution in New York City. Use the slider to pick a specific
        hour and look at how the charts change.
        ''')

@st.cache(persist=True)
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)   # Read n rows from data at the URL into our data frame
    lowercase = lambda x: str(x).lower()        # One line of code to turn all the letters in a word to lowercase (ie; Adam --> adam)
    data.rename(lowercase, axis='columns', inplace=True)    # Rename all the columns in our dataframe to their lowercase versions
    data[DATE_TIME] = pd.to_datetime(data[DATE_TIME])       # Convert the date column from a string into a 'Datetime' object
    return data

data = load_data(100000)


st.markdown('## First Pickup Visualization')

hour = st.slider('Hour to look at', 0, 23)
data = data[data[DATE_TIME].dt.hour == hour]
st.map(data)

st.markdown('## Second Pickup Visualization')

hour = st.number_input('hour', 0, 23, 10)
st.subheader('Geo data between %i:00 and %i:00' % (hour, (hour + 1) % 24))
midpoint = (np.average(data['lat']), np.average(data['lon']))

st.write(pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    initial_view_state={
        "latitude": midpoint[0],
        "longitude": midpoint[1],
        "zoom": 11,
        "pitch": 50,
    },
    layers=[
        pdk.Layer(
            "HexagonLayer",
            data=data,
            get_position=["lon", "lat"],
            radius=100,
            elevation_scale=4,
            elevation_range=[0, 1000],
            pickable=True,
            extruded=True,
        ),
    ],
))

if st.checkbox("Show raw data", False):
    st.subheader("Raw data by minute between %i:00 and %i:00" % (hour, (hour + 1) % 24))
    st.write(data)
