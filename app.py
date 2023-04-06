import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import pygeodesic
from geopy.distance import geodesic 

st.title("Universities within 1 km of Selected Subway Stations in NYC")
st.write("This app displays universities within 1 km of selected subway stations in NYC.")


df_stations = pd.read_excel("stations.xlsx")
df_stations = df_stations[['STATION', 'latitude', 'longitude']]

university= pd.read_csv("COLLEGE_UNIVERSITY.csv")
# Extract the latitude and longitude values from the_geom column
university['longitude'] = university['the_geom'].str.split(' ').str[1].str.replace('(', '').astype(float)
university['latitude'] = university['the_geom'].str.split(' ').str[2].str.replace(')', '').astype(float)
university = university[["NAME", "latitude", "longitude"]]

station_names = st.sidebar.multiselect("Select Subway Stations", ["14 ST-UNION SQ", "23 ST", "34 ST-PENN STA", "34 ST-HERALD SQ", "GRD CNTRL-42 ST", "JAY ST-METROTEC"],
                                       ["14 ST-UNION SQ", "23 ST", "34 ST-PENN STA", "34 ST-HERALD SQ", "GRD CNTRL-42 ST", "JAY ST-METROTEC"])

station_lat, station_lon = df_stations.loc[df_stations['STATION'] == "14 ST-UNION SQ", ['latitude', 'longitude']].iloc[0]

# Create map centered on New York City
nyc_map = folium.Map(location=[station_lat, station_lon], zoom_start=12, width=360, tiles='cartodbpositron')

# Add subway stations to the map
for index, row in df_stations.iterrows():
    if row['STATION'] in station_names:
        folium.Marker(location=[row['latitude'], row['longitude']], popup=row['STATION'], icon=folium.features.CustomIcon('subway.png', icon_size=(30,30))).add_to(nyc_map)

# Add universities within 1 km of the selected subway stations to the map
for index, row in df_stations.iterrows():
    if row['STATION'] in station_names:
        for index2, row2 in university.iterrows():
            if geodesic((row['latitude'], row['longitude']), (row2['latitude'], row2['longitude'])).km <= 1:
                if row2['NAME'] == 'Polytechnic University / Brooklyn-Metrotech Campus':
                    folium.CircleMarker(location=[row2['latitude'], row2['longitude']], radius=5, popup=row2['NAME'], color='black', fill=True, fill_color='white').add_to(nyc_map)
                else:
                    folium.CircleMarker(location=[row2['latitude'], row2['longitude']], radius=5, popup=row2['NAME'], color='red', fill=True, fill_color='white').add_to(nyc_map)

# Display the map
st_folium(nyc_map, width=800, height=800)

