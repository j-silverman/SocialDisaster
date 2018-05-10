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
        id = request.POST.keys()
        if 'shelter' in id:
            return render(request, 'tags.html', {'map': 'sheltmap'})
        elif 'evacuation' in id:
            return render(request, 'tags.html', {'map': 'evacmap'})
        elif 'damage' in id:
            return render(request, 'tags.html', {'map': 'dammap'})
        elif 'medicine' in id:
            return render(request, 'tags.html', {'map': 'medmap'})

    return render(request, 'tags.html', {'map':'sheltmap'})

def customtags(request):
    return render(request, 'customtags.html', {})
