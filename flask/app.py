"""
    Title: miniproject 3
    Author: Itaru Kishikawa
    Class CS 122 Advanced Python Sec 02
"""

from flask import Flask, render_template, redirect, request
import urllib
import pandas as pd
import json
from pandas.io.json import json_normalize
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter


# Creates a Flask application, named app
app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index')
def index():
    current = ('http://api.openweathermap.org/data/2.5/weather?units=metric&id=5392171&APPID=0f4fea93d5538d4ea1b562819aff6ac9')
    forecast = ('http://api.openweathermap.org/data/2.5/forecast?units=metric&id=5392171&APPID=0f4fea93d5538d4ea1b562819aff6ac9')
    current = urllib.urlopen(current).read()
    forecast = urllib.urlopen(forecast).read()
    result = data_from_json(current, forecast)
    j_current = json.loads(current)
    j_forecast = result.to_json()
    result_forecast = json.loads(j_forecast)
    return render_template('index.html', current=j_current, forecast=result_forecast)


def choose_the_icon(lst):
    result = ''
    if len(lst) is 1:
        result = lst[0] + '.svg'
    else:
        if 'Thunderstorm' in lst:
            if 'Drizzle' in lst:
                result = 'thunder-drizzle.svg'
            elif 'Rain' in lst:
                result = 'thunder-rain.svg'
            elif 'Snow' in lst:
                result = 'thunder-snow.svg'
            elif 'Atmosphere' in lst:
                result = 'thunder-fog.svg'
            elif 'Clear' in lst:
                result = 'thunder-clear.svg'
            elif 'Clouds' in lst:
                result = 'thunder-clouds.svg'
            elif 'Extreme' in lst:
                result = 'thunder-extreme.svg'
            else:
                result = 'Additional.svg'

        elif 'Drizzle' in lst:
            if 'Rain' in lst:
                result = 'drizzle-rain.svg'
            elif 'Snow' in lst:
                result = 'drizzle-snow.svg'
            elif 'Atmosphere' in lst:
                result = 'drizzle-fog.svg'
            elif 'Clear' in lst:
                result = 'drizzle-clear.svg'
            elif 'Clouds' in lst:
                result = 'drizzle-clouds.svg'
            elif 'Extreme' in lst:
                result = 'drizzle-extreme.svg'
            else:
                result = 'Additional.svg'

        elif 'Rain' in lst:
            if 'Snow' in lst:
                result = 'rain-snow.svg'
            elif 'Atmosphere' in lst:
                result = 'rain-fog.svg'
            elif 'Clear' in lst:
                result = 'rain-clear.svg'
            elif 'Clouds' in lst:
                result = 'rain-clouds.svg'
            elif 'Extreme' in lst:
                result = 'rain-extreme.svg'
            else:
                result = 'Additional.svg'

        elif 'Snow' in lst:
            if 'Atmosphere' in lst:
                result = 'snow-fog.svg'
            elif 'Clear' in lst:
                result = 'snow-clear.svg'
            elif 'Clouds' in lst:
                result = 'snow-clouds.svg'
            elif 'Extreme' in lst:
                result = 'snow-extreme.svg'
            else:
                result = 'Additional.svg'

        elif 'Atmosphere' in lst:
            if 'Clear' in lst:
                result = 'atmosphere-clear.svg'
            elif 'Clouds' in lst:
                result = 'atmosphere-clouds.svg'
            elif 'Extreme' in lst:
                result = 'atmosphere-extreme.svg'
            else:
                result = 'Additional.svg'

        elif 'Clear' in lst:
            if 'Clouds' in lst:
                result = 'clear-clouds.svg'
            elif 'Extreme' in lst:
                result = 'clear-extreme.svg'
            else:
                result = 'Additional.svg'

        elif 'Clouds' in lst:
            if 'Extreme' in lst:
                result = 'clouds-extreme.svg'
            else:
                result = 'Additional.svg'

        else:
            result = 'Additional.svg'
    return result


def choose_icon(df):
    i = 0
    while i < len(df):
        value = df['weather'][i]
        count = Counter(value)
        k = []
        for x in count:
            if count[x] > 1:
                k.append(x)
        icon = choose_the_icon(k)
        df.at[i, 'weather'] = icon
        i += 1
    return df


def plot_data(df, city_name):
    plt.style.use("dark_background")
    sns.barplot(x='date', y='temp', data=df, palette='winter_d')
    plt.xlabel("Date")
    plt.ylabel("Temperature in C")
    plt.title("Temperature Graph in {city_name}".format(city_name=city_name))
    plt.savefig('static/temp_graph.png')


def data_from_json(current, forecast):
    forecast_j = json.loads(forecast)
    current_j = json.loads(current)
    df = json_normalize(forecast_j['list'], 'weather', ['dt_txt', ['main', 'temp'],['main', 'temp_min'],['main', 'temp_max']])
    df['dt_txt'] = pd.to_datetime(df['dt_txt'], format='%Y-%m-%d %X')
    info = df.groupby(df['dt_txt'].dt.day).agg({'main.temp' : 'mean', 'main.temp_min' : 'min', 'main.temp_max':'max', 'main':lambda x: list(x)}).reset_index()
    info.columns = ['date', 'temp', 'weather', 'temp_max', 'temp_min']
    info = info.round(1)
    plot_data(info, current_j['name'])
    info = choose_icon(info)
    return info


def access_api(location):
    current = ('http://api.openweathermap.org/data/2.5/weather?units=metric&q=%s&APPID=0f4fea93d5538d4ea1b562819aff6ac9' % location)
    forecast = ('http://api.openweathermap.org/data/2.5/forecast?units=metric&q=%s&APPID=0f4fea93d5538d4ea1b562819aff6ac9' % location)
    current = urllib.urlopen(current).read()
    forecast = urllib.urlopen(forecast).read()
    j_current = json.loads(current)
    if j_current['cod'] == '404':
        return redirect('/index')
    else:
        result = data_from_json(current, forecast)
        j_forecast = result.to_json()
        return json.loads(current), json.loads(j_forecast)


@app.route('/info', methods=['POST', 'GET'])
def info():
    if request.method == 'POST':
        location = request.form['location']
        current, forecast = access_api(location)
        return render_template('index.html', current=current, forecast=forecast)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    app.logger.error('Server Error: %s', error)
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.debug = True
    app.run(port=33507)
