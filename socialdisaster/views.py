from __future__ import unicode_literals
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
import pandas as pd
import numpy as np
import folium
from folium import IFrame
import vincent, json
import requests
import sqlite3
import os

def index(request):
    if request.method == 'POST':
        return HttpResponseRedirect('selecttags')
    else:
        return render(request, 'home.html', {})

def selecttags(request):
    sql = sqlite3.connect('tweets.db')
    df = pd.read_sql_query("SELECT * FROM evacuationCoords", sql)
    #df = df[pd.notnull(df['chunks'])]
    #df = df.reset_index()
    map1 = folium.Map(location=[30.2, -98.1], zoom_start=6)
    places = {}
    for index, i in df.iterrows():
        if i['coords'] == 'None':
            continue
        try:
            places[i['chunks']] += str("<li>" + (i['Tweet']) + "</li>")
        except:
            places[i['chunks']] = "<li>" + (i['Tweet']) + "</li>"
            pass
        coords = i['coords']
        coords = coords.split(',')
        html = ("<h1>Tweet Text </h1><br>{}".format(places[i['chunks']]))
        iframe = IFrame(html=html, width=300, height=200)
        popup = folium.Popup(iframe, max_width=400)
        if len(coords) == 2:
            coords = map(float, coords)
            folium.Marker(coords, popup=popup).add_to(map1)
        else:
            coords = [map(float, coords[j:j + 2]) for j in range(0, len(coords), 2)]
            coords.append(coords[0])
            folium.PolyLine(coords, popup=popup).add_to(map1)
    dir_path = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(dir_path, 'templates\evacmap.html')
    map1.save(filename)

    return render(request, 'tags.html', {})

def customtags(request):
    return render(request, 'customtags.html', {})
