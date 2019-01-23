#!/usr/bin/env python

from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User



@main.route('/', methods=['GET','POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        #return redirect(url_for('.index'))
        db.create_all()
    return render_template('index.html',form=form,username=session.get('username'),
                           known=session.get('known',False),current_time=datetime.utcnow())

@main.route('/overview')
def overview():
    return render_template('overview.html')

@main.route('/analysis')
def analysis():
    return render_template('analysis.html')

@main.route('/management')
def management():
    return render_template('management.html')
@main.route('/signin')
def signin():
    return redirect('auth/signin')

@main.route('/signup')
def signup():
    return redirect('auth/signup')
