import pandas as pd
import numpy as np
import folium
from folium import IFrame
import vincent, json
import requests
import sqlite3
import socialdisaster.config as config
import os

def getCoords():
    sql = sqlite3.connect('tweets.db')
    df = pd.read_sql_query("SELECT * FROM medTweets", sql)
    df['coords'] = ""
    #df = df[pd.notnull(df['chunks'])]
    df = df.drop(['level_0'], axis = 1)
    #map1 = folium.Map(location=[30.2, -98.1], zoom_start=6)
    places = {}
    for i in range(0, len(df['chunks'])):
        if df['chunks'][i].lower() == 'texas' or df['chunks'][i].lower() == 'TX':
            df['coords'][i] = 'None'
        elif df['chunks'][i] == 'None':
            df['coords'][i] = 'None'
        elif df['chunks'][i] != 'None':
            response = requests.get(
                "https://maps.googleapis.com/maps/api/geocode/json?address={}&bounds=25.1847679727,-104.4518006518|34.3250264381,-86.8736756518&key={}".format(df['chunks'][i], config.MAPS_API_KEY))
            resp_json_payload = response.json()
            if resp_json_payload['status'] == 'ZERO_RESULTS':
                df['coords'][i] = 'None'
            elif (resp_json_payload['results'][0]['address_components'][0]['types'][0] == 'administrative_area_level_1'):
                df['coords'][i] = 'None'

            elif 'bounds' not in resp_json_payload['results'][0]['geometry']:

                coords = resp_json_payload['results'][0]['geometry']['location']
                coords = str(coords['lat'])+','+ str(coords['lng'])
                df['coords'][i] = coords

            else:

                bounds = resp_json_payload['results'][0]['geometry']['bounds']
                northeast = str(bounds['northeast']['lat']) + ',' + str(bounds['northeast']['lng'])
                southwest = str(bounds['southwest']['lat']) + ',' + str(bounds['southwest']['lng'])
                southeast = str(bounds['southwest']['lat']) + ',' + str(bounds['northeast']['lng'])
                northwest = str(bounds['northeast']['lat']) + ',' + str(bounds['southwest']['lng'])
                df['coords'][i] = (northeast+ ','+ southeast+',' + southwest+',' + northwest)
    df.to_sql("medCoords", sql, if_exists="replace")


getCoords()