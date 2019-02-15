#!/usr/bin/env python

from datetime import datetime
from flask import render_template, session, redirect, url_for, jsonify
from . import main
from .forms import *
from app import db
from ..models import *
from flask_login import login_required, current_user
import json

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
    return render_template('overview.html', items=items)

@main.route('/analysis')
@login_required
def analysis():
    return render_template('analysis.html')


@main.route('/count')
def count_unread():
    num_unread = Item.query.filter_by(item_read = 0).count()
    num_users = User.query.filter_by(user_available=1).count()
    num_items = Item.query.filter_by(item_delete=0).count()
    data = {'num_unread': num_unread, 'num_users': num_users, 'num_items': num_items}
    users = User.query.filter_by(user_available=1).all()
    for user in users:
        tempnum = Item.query.filter_by(item_author=user.user_id).count()
        data[user.user_name] = tempnum
    try:
        data['notifications']=[]
        notifications = Notification.query.filter_by(notification_reader=current_user._get_current_object().user_id)\
                                            .filter_by(notification_read=0).order_by(Notification.notification_datetime.desc()).all()
        for notification in notifications:
            data['notifications'].append(((notification.notification_id,notification.notification_content,notification.notification_datetime)))
    except:
        pass
    return jsonify(data)

NOTIFICATIONS = ['',
                 ' post a new broadcast.',
                 ' submited a new item.',
                 ' modified an item',
                 ' modified your item.',
                 ' accepted your item.',
                 ' rejected your item']
def add_notification(author,author_name,reader,target,index):
    try:
        notification = Notification(notification_author=author,
                                    notification_reader=reader,
                                    notification_content=author_name+NOTIFICATIONS[index],
                                    notification_target=target,
                                    notification_datetime=datetime.utcnow(),
                                    notification_read=0)
        db.session.add(notification)
        db.session.commit()
    except Exception as e:
        print(e)
        pass

@main.route('/notification/<int:id>',methods=['GET'])
@login_required
def notification_read(id):
    notification = Notification.query.filter_by(notification_id=id).first_or_404()
    try:
        Notification.query.filter_by(notification_id=id).update({'notification_read':1})
        db.session.commit()
    except Exception as e:
        print(e)
        db.session.rollback()
    return redirect(notification.notification_target)

@main.route('/temp')
def temp():
    return render_template('temp.html')
