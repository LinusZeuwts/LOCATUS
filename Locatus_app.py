# importeer packages
import streamlit as st
import folium
import pandas as pd
import osmnx as ox
import geopandas as gpd
from geopy.geocoders import Nominatim
import folium
import numpy as np
import random
import matplotlib.colors as mcolors
import secrets
from streamlit_folium import st_folium


### STREAMLIT
st.title('SINCR - Leegstand')   #titel


## INDIEN NIEUW EXCEL BESTAND


### DATA


## Functie voor het herwerken van de data zit in SINCR dataframe maken voor streamlit.ipynb
## inladen van de data
## databestand laden en parameters samenstellen
## importeer databestand
# data_mechelen = pd.read_excel('df_mechelen_locatus.xlsx')

# # plaatsnamen samenstellen
# data_mechelen['plaatsnaam'] = data_mechelen['STRAAT'] + ' ' + data_mechelen['HUISNR'].astype(str) + ', ' + data_mechelen['GEMEENTE']

# # jaartallen afronden
# data_mechelen['JAARDATE'] = [i.year for i in data_mechelen['JAARDATE']]

# ## adressen naar polygonen
# # alle adressen in lijst
# lijst_adressen = list(data_mechelen['plaatsnaam'].unique())

# # leeg dataframe om de polygonen op te slaan
# df_polygonen = pd.DataFrame()

# # for-loop om de adressen aan polygonen te koppelen
# for i in lijst_adressen:
#     try:
#         pn = i
#         area = ox.geocode_to_gdf(pn)
#         area = pd.DataFrame(area)
#         area['plaatsnaam'] = i
#         df_polygonen = pd.concat([df_polygonen, area])
        
#     except: 
#         # (RuntimeError, TypeError, NameError)
#         pass

# # merge met het df van Mechelen
# data_mechelen = pd.merge(data_mechelen, df_polygonen, how = 'left', on = 'plaatsnaam')#### GeoDataFrame

# # schrijf naar GeoJSON
# df = gpd.GeoDataFrame(data=data_mechelen, geometry=data_mechelen['geometry'], crs=4329) # eerst naar gdf en dan naar GEOJSON, inladen nog testen
# # 
# df.to_file("data_mechelen.geojson", driver = 'GeoJSON')


## INDIEN BESTAAND EXCEL BESTAND


### DATA IMPORTEREN
data_mechelen = gpd.read_file('data_mechelen.geojson')


### STREAMLIT 
# FILTER voor jaartal
jaren = np.sort(data_mechelen['JAARDATE'].unique())
jaar_filter = st.select_slider('Selecteer een jaartal', options = [str(i) for i in jaren])    #slider

## filter data en splits data
# filter volgens jaar
data_mechelen_filter = data_mechelen[data_mechelen['JAARDATE'] == int(jaar_filter)]

# filter voor bewoond
data_mechelen_filter_bewoond = data_mechelen_filter[data_mechelen_filter['PINC_HOOFDBRANCHE'] != 'leegstand'] # alle leegstand eruit

# filter voor leegstand
data_mechelen_filter_leegstand = data_mechelen_filter[data_mechelen_filter['PINC_HOOFDBRANCHE'] == 'leegstand'] # hier behoud je alle leegstand


### STREAMLIT

## HOOFDSCHERM

# maak een kaart van Mechelen
m = folium.Map(location = [51.0258761, 4.477536], zoom_start = 15, tiles = "CartoDB positron")

# plot de coordinaten van alle 'bewoonde' gebouwen op de kaart
for _, r in data_mechelen_filter_bewoond.iterrows():
    sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance = 0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data = geo_j, style_function = lambda x: {'fillColor': 'grey',
                                                                     'color': "black",
                                                                     'weight': 1})
    geo_j.add_to(m)

# plot de coordinaten van alle 'leegstaande' gebouwen op de kaart
for _, r in data_mechelen_filter_leegstand.iterrows():
    sim_geo = gpd.GeoSeries(r['geometry']).simplify(tolerance = 0.001)
    geo_j = sim_geo.to_json()
    geo_j = folium.GeoJson(data = geo_j, style_function = lambda x: {'fillColor': 'orange',
                                                                     'color': "black",
                                                                     'weight': 4})
    geo_j.add_to(m)

# plot de kaart
st_data = st_folium(m, width = 750) #kaart

## ZIJBALK

# zijbalk informatie
st.sidebar.write('Voor welke parameters wil je nog filteren?')
st.sidebar.write('databestand inladen + y/n')

