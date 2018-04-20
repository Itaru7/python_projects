"""
    This file is for cleaning data, accessing API,
    accessing user's current location.
"""

import pandas as pd
import json
import requests
from flask import request
from pandas.io.json import json_normalize
from urllib.request import urlopen
from choose_images import choose_icon


def data_from_json(forecast: 'weather forecast data') -> pd.core.frame.DataFrame:
    """
    Get data from API and clean up the huge data to only, date, temperature,
    minimum temperature, and  max temperature.
    Also adds the relevant icon for each day by calling choose_icon.

    :param forecast: bytes(type)
    :return: info: dataFrame(type)
    """
    forecast_j = json.loads(forecast)
    df = json_normalize(forecast_j['list'], 'weather',
                        ['dt_txt', ['main', 'temp'], ['main', 'temp_min'], ['main', 'temp_max']])
    df['dt_txt'] = pd.to_datetime(df['dt_txt'], format='%Y-%m-%d %X')
    info = df.groupby(df['dt_txt'].dt.day).agg(
        {'main.temp': 'mean', 'main.temp_min': 'min', 'main.temp_max': 'max', 'main': lambda x: list(x)}).reset_index()
    info.columns = ['date', 'temp', 'temp_min', 'temp_max', 'weather']
    info = info.round(1)
    info = choose_icon(info)
    return info


def access_api(location: str) -> json:
    """
    Access to weather forecast API and return json

    :param location: string(type)
    :return: if location is valid, return json data for current forecast.
            Otherwise, return 500 error and redirect to 500 page.
    """
    current = 'http://api.openweathermap.org/data/2.5/weather?units=metric&q=%s' \
              '&APPID=0f4fea93d5538d4ea1b562819aff6ac9' % location
    forecast = 'http://api.openweathermap.org/data/2.5/forecast?units=metric&q=%s' \
               '&APPID=0f4fea93d5538d4ea1b562819aff6ac9' % location
    try:
        current = urlopen(current).read()
        forecast = urlopen(forecast).read()
        j_current = json.loads(current)
        result = data_from_json(forecast)
        j_forecast = result.to_json()
        return json.loads(current), json.loads(j_forecast)
    except:
        return 500, 500


def get_current_loc() -> [str, str]:
    """
    Get user's current location based on IP address

    :return: lat: string
             lon: string
    """
    if not request.headers.getlist("X-Forwarded-For"):
        ip = request.remote_addr
    else:
        ip = request.headers.getlist("X-Forwarded-For")[0]

    # If want to test locally, access to https://ipdata.co/index.html, and get IP address
    # Then replace IP address with ip
    # '76.21.124.7': Alum Rock (Home)
    # '130.65.254.13': San Jose
    url = 'http://freegeoip.net/json/%s' % '130.65.254.13'
    r = requests.get(url)
    j = json.loads(r.text)
    lat = j['latitude']
    lon = j['longitude']
    return lat, lon
