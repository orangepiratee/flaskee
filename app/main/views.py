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

@main.route('/count/unread')
@login_required
def count_unread():
    if current_user._get_current_object().user_role >=2:
        unread = Item.query.filter_by(item_read = 0).count()
        return str(unread)
    else:
        return

@main.route('/count/user',methods=['GET'])
def count_user():
    num_users = User.query.filter_by(user_available=1).count()
    return str(num_users)


@main.route('/count/item', methods=['GET'])
def count_item():
    num_items = Item.query.filter_by(item_delete=0).count()
    return str(num_items)


@main.route('/temp')
def temp():
    return render_template('temp.html')
