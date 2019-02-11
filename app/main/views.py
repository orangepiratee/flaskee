#!/usr/bin/env python

from datetime import datetime
from flask import render_template, session, redirect, url_for, jsonify
from . import main
from .forms import *
from app import db
from ..models import *
from flask_login import login_required, current_user


@main.route('/test', methods=['GET','POST'])
def test():
    form = NameForm()
    if form.validate_on_submit():
        #return redirect(url_for('.index'))
        db.create_all()
    return render_template('test.html',form=form, current_time=datetime.utcnow())

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/overview')
def overview():
    items = Item.query.order_by(Item.item_datetime.desc()).all()
    '''tempusers = []
    for user in users:
        temp = {}
        temp['user_name']=user.user_name
        temp['user_id']=user.user_id
        tempusers.append(temp)
    session['users'] = users'''
    return render_template('overview.html', items=items)

@main.route('/analysis')
@login_required
def analysis():
    return render_template('analysis.html')

@main.route('/manage', methods=['GET','POST'])
@login_required
def management():
    items = Item.query.order_by(Item.item_datetime.desc()).filter_by(item_author=current_user._get_current_object().user_id)
    return render_template('manage.html', items=items)

@main.route('/count')
def count_unread():
    num_unread = Item.query.filter_by(item_read = 0).count()
    num_users = User.query.filter_by(user_available=1).count()
    num_items = Item.query.filter_by(item_delete=0).count()
    data = {'num_unread':num_unread,'num_users':num_users,'num_items':num_items}
    return jsonify(data)



@main.route('/temp')
def temp():
    return render_template('temp.html')
