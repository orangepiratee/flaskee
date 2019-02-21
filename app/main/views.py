#!/usr/bin/env python


from flask import render_template, session, redirect, url_for, jsonify
from . import main
from .forms import *
from app import db,base_dir,pt1,pt2,pt3
from ..models import *
from flask_login import login_required, current_user
import json
from datetime import datetime,timedelta
from ..mysql import *


@main.route('/test', methods=['GET','POST'])
def test():
    form = NameForm()
    if form.validate_on_submit():
        #return redirect(url_for('.index'))
        items = Item.query.filter_by(item_read=0).all()
        for item in items:
            add_notification(item.item_author,User.query.filter_by(user_id=item.item_author).first_or_404().user_name,
                             User.query.filter_by(user_role=2).first_or_404().user_id,'/item/'+str(item.item_id),1)
    return render_template('test.html',form=form, current_time=datetime.utcnow())

@main.route('/')
def index():
    return render_template('index.html',pt2='HomePage',data=count_data())

@main.route('/overview')
def overview():
    items = Item.query.order_by(Item.item_datetime.desc()).all()
    return render_template('overview.html', items=items,pt1=pt1[0],pt2=pt2[3])

@main.route('/analysis')
@login_required
def analysis():
    return render_template('analysis.html')

@main.route('/posts',methods=['GET'])
@login_required
def posts():
    posts = Post.query.order_by(Post.post_datetime.desc()).all()
    return render_template('/post/post_manage.html',posts=posts,pt1=pt1[1],pt2=pt2[3])

@main.route('/count')
def count_notifications():
    data = {}
    try:
        data['notifications']=[]
        notifications = Notification.query.filter_by(notification_reader=current_user._get_current_object().user_id)\
                                            .filter_by(notification_read=0).order_by(Notification.notification_datetime.desc()).all()
        for notification in notifications:
            data['notifications'].append(((notification.notification_id,notification.notification_content,notification.notification_datetime)))
    except:
        pass
    return jsonify(data)



months = ['1','2','3','4','5',',6',',7']
today = datetime.now().strftime('%Y-%m-%d')
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


def count_data_bytime(userid,n=0):
    delta = timedelta(days=n)
    n_days = datetime.now() - delta
    time_start = n_days.strftime('%Y-%m-%d')
    num_Items = select(cursor,"select count(*) from flaskee.t_item where item_author = '{}' "
                              "and item_datetime >= '{}'".format(userid,time_start))
    return num_Items

def count_data_bymonth(userid,y=2019,m=0):
    m_start = '{}-{}'.format(y,m)
    m_end = '{}-{}'.format(y,m+1)
    num_items = select(cursor,"select count(*) from flaskee.t_item where item_author = '{}' "
                              "and item_datetime >= '{}' and item_datetime < '{}'".format(userid,m_start,m_end))
    return num_items

def count_data_byyear(userid,y=2019):
    num_items = select(cursor,"select count(*) from flaskee.t_item where item_author = '{}' "
                              "and item_datetime >= '{}' and item_datetime < '{}'".format(userid,y,y+1))
    return num_items


def count_data():
    num_unread = Item.query.filter_by(item_read=0).count()
    num_users = User.query.filter_by(user_available=1).count()
    num_items = Item.query.filter_by(item_delete=0).count()
    data = {'num_unread': num_unread, 'num_users': num_users, 'num_items': num_items}
    users = User.query.filter_by(user_available=1).all()
    data['users'] = {}
    inx = 1
    for user in users:
        if user.user_name:
            temp_total = Item.query.filter_by(item_author=user.user_id).count()
            temp_accept = Item.query.filter_by(item_author=user.user_id).filter_by(item_accept=1).count()
            temp_reject = Item.query.filter_by(item_author=user.user_id).filter_by(item_accept=0).count()
            temp_unread = Item.query.filter_by(item_author=user.user_id).filter_by(item_read=0).count()
            num_today = count_data_bytime(user.user_id)
            num_week = count_data_bytime(user.user_id,3)
            num_month = count_data_bytime(user.user_id,30)
            num_month_1 = count_data_bymonth(user.user_id,m=1)
            num_year_19 = count_data_byyear(user.user_id,2019)

            data['users'][user.user_name] = {'inx':inx,'total': temp_total, 'accept': temp_accept, 'reject': temp_reject,
                                             'unread': temp_unread, 'percentage':int(temp_total/num_items*100),
                                             'num_today':num_today,'num_week':num_week,'num_month':num_month,'num_mon1':num_month_1,
                                             'num_year_19':num_year_19}
            inx +=1
        else:
            continue
    return data


NOTIFICATIONS = ['',
                 ' post a new broadcast.',#1
                 ' submited a new item.',#2
                 ' modified an item',#3
                 ' modified your item.',#4
                 ' accepted your item.',#5
                 ' rejected your item']#6
def add_notification(author,author_name,reader,target,index):
    try:
        notification = Notification(notification_author=author,
                                    notification_reader=reader,
                                    notification_content=str(author_name)+NOTIFICATIONS[index],
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
