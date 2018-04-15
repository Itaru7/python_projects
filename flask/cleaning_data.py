import pandas as pd
import json
import requests
from flask import request
from pandas.io.json import json_normalize
from urllib.request import urlopen
from choose_images import choose_icon



def data_from_json(current, forecast):
    forecast_j = json.loads(forecast)
    df = json_normalize(forecast_j['list'], 'weather', ['dt_txt', ['main', 'temp'],['main', 'temp_min'], ['main', 'temp_max']])
    df['dt_txt'] = pd.to_datetime(df['dt_txt'], format='%Y-%m-%d %X')
    info = df.groupby(df['dt_txt'].dt.day).agg({'main.temp': 'mean', 'main.temp_min': 'min', 'main.temp_max': 'max', 'main': lambda x: list(x)}).reset_index()
    info.columns = ['date', 'temp','temp_min', 'temp_max', 'weather']
    info = info.round(1)
    info = choose_icon(info)
    return info


def access_api(location):
    current = ('http://api.openweathermap.org/data/2.5/weather?units=metric&q=%s&APPID=0f4fea93d5538d4ea1b562819aff6ac9' % location)
    forecast = ('http://api.openweathermap.org/data/2.5/forecast?units=metric&q=%s&APPID=0f4fea93d5538d4ea1b562819aff6ac9' % location)
    current = urlopen(current).read()
    forecast = urlopen(forecast).read()
    j_current = json.loads(current)
    if j_current['cod'] == u'404':
        return 500, 500
    else:
        result = data_from_json(current, forecast)
        j_forecast = result.to_json()
        return json.loads(current), json.loads(j_forecast)


def get_current_loc():
    if not request.headers.getlist("X-Forwarded-For"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Forwarded-For")[0]

    # If want to test locally, access to https://ipdata.co/index.html, and get IP address
    # Then replace IP address with ip
    url = 'http://freegeoip.net/json/%s' % ip
    r = requests.get(url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return lat, lon
