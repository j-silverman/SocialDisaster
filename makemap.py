#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
import folium
from folium import IFrame
import json
import requests
import sqlite3
import os
import re

sql = sqlite3.connect('tweets.db')
df = pd.read_sql_query("SELECT * FROM shelterCoords", sql)
df.drop_duplicates(subset=['Tweet'], keep=False)
map1 = folium.Map(location=[30.2, -98.1], zoom_start=6)
places = {}

for index, i in df.iterrows():
    if i['coords'] == 'None':
        continue

    urls = re.findall(r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro
        |tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr
        |cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il
        |im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz
        |na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy
        |sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)
        [^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu
        |gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj
        |bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf
        |gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv
        |ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru
        |rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf
        |ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))""",i['Tweet'])
    if 'pic.twitter.com' in i['Tweet']:
        a, b, c = i['Tweet'].partition('pic.twitter.com')
        try:
            places[i['chunks']] += str('<li>' + a +  '<a target ="_blank" rel = "external nofollow" href= http:/' + b+c + '>' + 'link' + '</a>' + '</li>')
        except:
            places[i['chunks']] = str('<li>' + a + '<a target ="_blank" rel = "external nofollow" href=http:/' + b+c + '>' + 'link' + '</a>' + '</li>')
            pass

    elif urls == []:
        try:
            places[i['chunks']] += str("<li>" + (i['Tweet']) + "</li>")
        except:
            places[i['chunks']] = "<li>" + (i['Tweet']) + "</li>"
            pass
    elif urls != []:
        try:
            places[i['chunks']] += str('<li>' + i['Tweet'] +  '<a target ="_blank" rel = "external nofollow" href=' + urls[0] + '>' + 'link' + '</a>' + '</li>')
        except:
            places[i['chunks']] = str('<li>' + i['Tweet'] + '<a target ="_blank" rel = "external nofollow" href=' + urls[0]+ '>' + 'link' + '</a>' + '</li>')
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
filename = os.path.join(dir_path, 'socialdisaster\\templates\sheltmap.html')
map1.save(filename)