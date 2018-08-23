"""
    Title: miniproject 3
    Author: Itaru Kishikawa
    Class CS 122 Advanced Python Sec 02
"""

from flask import Flask, render_template, redirect
from choose_images import *
from cleaning_data import *
import smtplib
from email.mime.text import MIMEText

# Creates a Flask application, named app
app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/index')


@app.route('/index')
def index():
    """
        Get user's current location by default.
        And display weather forecast.

    :return:
    """
    lat, lon = get_current_loc()
    current = 'http://api.openweathermap.org/data/2.5/weather?units=metric&lon={lon}' \
              '&lat={lat}&type=like&APPID=0f4fea93d5538d4ea1b562819aff6ac9'.format(lon=lon, lat=lat)
    forecast = 'http://api.openweathermap.org/data/2.5/forecast?units=metric&lon={lon}' \
               '&lat={lat}&type=like&APPID=0f4fea93d5538d4ea1b562819aff6ac9'.format(lon=lon, lat=lat)
    current = urlopen(current).read()
    forecast = urlopen(forecast).read()
    result = data_from_json(forecast)
    j_current = json.loads(current)
    background = choose_background(j_current['weather'][0]['id'])
    j_forecast = result.to_json()
    result_forecast = json.loads(j_forecast)
    return render_template('index.html', current=j_current, forecast=result_forecast, background=background)


@app.route('/info', methods=['POST', 'GET'])
def info():
    """
        Get location that the user input.
        Then pass the data to frontend.

    :return:
    """
    if request.method == 'POST':
        location = request.form['location']
        current, forecast = access_api(location)
        if current == 500:
            return render_template('500.html'), 500
        else:
            background = choose_background(current['weather'][0]['id'])
            return render_template('index.html', current=current, forecast=forecast, background=background)


@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/send', methods=['POST'])
def send():
    """
        Get in put from user and send email to my address.
        Then route send.html
    :return:
    """
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        company = request.form['company'] if request.form['company'] else 'None'
        website = request.form['website'] if request.form['website'] else 'None'
        body = request.form['msg']
        msg = MIMEText('Name: ' + name +
                       '\nEmail: ' + email +
                       '\nCompany: ' + company +
                       '\nWebsite: ' + website +
                       '\nBody:\n' + body)
        msg['Subject'] = 'Mail from weather app'
        msg['From'] = 'contactitaru@gmail.com'
        msg['To'] = 'ir172178@gmail.com'
        sender = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        sender.ehlo()
        sender.login('contactitaru@gmail.com', 'contactitar')
        sender.sendmail('contactitaru@gmail.com', 'ir172178@gmail.com', msg.as_string())
        sender.quit()

        return render_template('send.html')


@app.errorhandler(404)
def page_not_found(e):
    """
    Return 404 error

    :param e:
    :return:
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(error):
    """
    Return 500 error

    :param error:
    :return:
    """
    app.logger.error('Server Error: %s', error)
    return render_template('500.html'), 500


if __name__ == '__main__':
    app.debug = True
    app.run(port=33507)
