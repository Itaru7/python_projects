"""
    Title: miniproject 3
    Author: Itaru Kishikawa
    Class CS 122 Advanced Python Sec 02
"""

from choose_images import *
from cleaning_data import *

# Creates a Flask application, named app
app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index')
def index():
    lat, lon = get_current_loc()
    current = ('http://api.openweathermap.org/data/2.5/weather?units=metric&lon={lon}&lat={'
               'lat}&type=like&APPID=0f4fea93d5538d4ea1b562819aff6ac9'.format(lon=lon, lat=lat))
    forecast = ('http://api.openweathermap.org/data/2.5/forecast?units=metric&lon={lon}&lat={'
                'lat}&type=like&APPID=0f4fea93d5538d4ea1b562819aff6ac9'.format(lon=lon, lat=lat))
    current = urllib.urlopen(current).read()
    forecast = urllib.urlopen(forecast).read()
    result = data_from_json(current, forecast)
    j_current = json.loads(current)
    background = choose_background(j_current['weather'][0]['id'])
    j_forecast = result.to_json()
    result_forecast = json.loads(j_forecast)
    return render_template('index.html', current=j_current, forecast=result_forecast, background=background)


@app.route('/info', methods=['POST', 'GET'])
def info():
    if request.method == 'POST':
        location = request.form['location']
        current, forecast = access_api(location)
        background = choose_background(current['weather'][0]['id'])
        return render_template('index.html', current=current, forecast=forecast, background=background)


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
