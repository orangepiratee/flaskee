#!/usr/bin/env python

from flask import Flask
from flask import make_response
from flask import abort
from flask import render_template
from flask_bootstrap import Bootstrap


app = Flask(__name__)

bootstrap = Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/management')
def management():
    return render_template('management.html')

@app.route('/400')
def bad_request():
    return '<h1>Bad Request!</h1>',400

@app.route('/cookie')
def cookie():
    response = make_response('<h1>this document carries a cookie!</h1>')
    response.set_cookie('answer','42')
    return response

@app.route('/user/<id>')
def get_user(id):
    #user = load_user(id)
    if not user:
        abort(404)
    return '<h1>hello {}!</h1>'.format(user.name)

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/500')
def internal_s_e():
    return render_template('500.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500