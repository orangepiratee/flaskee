#!/usr/bin/env python

from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql,os

from datetime import datetime

class NameForm(FlaskForm):
    name = StringField('What\'s you name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

app = Flask(__name__)
#config private key
app.config['SECRET_KEY'] = 'nothing'
#config sqlalchemy uri to mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://debian-sys-maint:root@localhost:3306/flaskee'
app.config['SQLALCHEMY_COMMIT_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
#moment module to get system time
moment = Moment(app)
#bootstrap
bootstrap = Bootstrap(app)
#some variables
basepath = os.path.abspath(os.path.dirname(__file__))

#routes
@app.route('/', methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None or old_name != form.name.data:
            flash('yowza, you changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/overview')
def overview():
    return render_template('overview.html', current_time=datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html',name=name)

@app.route('/analysis')
def analysis():
    return render_template('analysis.html')

@app.route('/management')
def management():
    return render_template('management.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500