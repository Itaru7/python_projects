"""
    Title: miniproject 3
    Author: Itaru Kishikawa
    Date:
    Class CS 122 Advanced Python Sec 02
"""

from flask import Flask, render_template

# Creates a Flask application, named app
app = Flask(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.debug = True
    app.run(port=33507)

