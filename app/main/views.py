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

@main.route('/items')
def overview():
    items = Item.query.order_by(Item.item_datetime.desc()).all()
    return render_template('/item/items.html', items=items,pt1=pt1[0],pt2=pt2[3])

@main.route('/posts',methods=['GET'])
def posts():
    posts = Post.query.order_by(Post.post_datetime.desc()).all()
    return render_template('/post/posts.html',posts=posts,pt1=pt1[1],pt2=pt2[3])

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


conn = get_conn()
cursor = conn.cursor()

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

def count_today(userid=0):
    if userid == 0:
        num_items = select(cursor, "select count(*) from flaskee.t_item where to_days(item_datetime) = to_days(now());")
    else:
        num_items = select(cursor,"select count(*) from flaskee.t_item where item_author = '{}' "
                        "and to_days(item_datetime) = to_days(now());".format(userid))
    return num_items

def count_thismonth(userid=0):
    if userid == 0:
        num_items = select(cursor, "select count(*) from flaskee.t_item where date_format(item_datetime,'%Y%m') = date_format(curdate(),'%Y%m');")
    else:
        num_items = select(cursor,"select count(*) from flaskee.t_item where item_author = '{}' "
                              "and date_format(item_datetime,'%Y%m') = date_format(curdate(),'%Y%m');".format(userid))
    return num_items

def count_thisweek(userid=0):
    if userid == 0:
        num_items = select(cursor, "select count(*) from flaskee.t_item where yearweek(date_format(item_datetime,'%Y-%m-%d')) = yearweek(now())")
    else:
        num_items = select(cursor,"select count(*) from flaskee.t_item where item_author = '{}' "
                              "and yearweek(date_format(item_datetime,'%Y-%m-%d')) = yearweek(now())".format(userid))
    return num_items

def count_thisyear(userid=0):
    if userid ==0:
        num_items = select(cursor, "select count(*) from flaskee.t_item year(item_datetime) = year(now())")
    else:
        num_items = select(cursor,"select count(*) from flaskee.t_item where item_author = '{}' "
                              "and year(item_datetime) = year(now())".format(userid))
    return num_items

def count_thisseason(userid=0):
    if userid ==0:
        num_items = select(cursor, "select count(*) from flaskee.t_item where quarter(item_datetime) = quarter(now())")
    else:
        num_items = select(cursor,"select count(*) from flaskee.t_item where item_author = '{}' "
                              "and quarter(item_datetime) = quarter(now())".format(userid))
    return num_items

sqls = ["",
        "select * from 表名 where (时间字段名) = to_days(now());",#today
        "SELECT * FROM 表名 WHERE TO_DAYS( NOW( ) ) - TO_DAYS( 时间字段名) <= 1;",#yesterday
        "SELECT * FROM 表名 where DATE_SUB(CURDATE(), INTERVAL 7 DAY) <= date(时间字段名);",#last 7days
        "SELECT * FROM 表名 WHERE DATE_FORMAT( 时间字段名, '%Y%m' ) = DATE_FORMAT( CURDATE( ) , '%Y%m' )",#this month
        "SELECT * FROM 表名 WHERE PERIOD_DIFF( date_format( now( ) , '%Y%m' ) , date_format( 时间字段名, '%Y%m' ) ) =1",#last month
        "select * from 表名 where QUARTER(时间字段名)=QUARTER(now());",#this season
        "select * from 表名 where QUARTER(时间字段名)=QUARTER(DATE_SUB(now(),interval 1 QUARTER));",#last season
        "select * from 表名 where YEAR(时间字段名)=YEAR(NOW())",#this year
        "select * from 表名 where year(时间字段名)=year(date_sub(now(),interval 1 year));",#last year
        "SELECT * FROM 表名 WHERE YEARWEEK(date_format(时间字段名,'%Y-%m-%d')) = YEARWEEK(now());",#this week
        "SELECT *  FROM 表名 WHERE YEARWEEK(date_format(时间字段名,'%Y-%m-%d')) = YEARWEEK(now())-1;",#last week
        "select * from enterprise where date_format(时间字段名,'%Y-%m')=date_format(DATE_SUB(curdate(), INTERVAL 1 MONTH),'%Y-%m');"#last month
        ]

def count_data():
    num_unread = Item.query.filter_by(item_read=0).count()
    num_users = User.query.filter_by(user_available=1).count()
    num_items = Item.query.filter_by(item_delete=0).count()
    num_items_today = count_today()
    data = {'num_unread': num_unread, 'num_users': num_users, 'num_items': num_items, 'num_items_today':num_items_today}
    users = User.query.filter_by(user_available=1).all()
    data['users'] = {}
    inx = 1
    for user in users:
        if user.user_name:
            temp_total = Item.query.filter_by(item_author=user.user_id).count()
            temp_accept = Item.query.filter_by(item_author=user.user_id).filter_by(item_accept=1).count()
            temp_reject = Item.query.filter_by(item_author=user.user_id).filter_by(item_accept=0).count()
            temp_unread = Item.query.filter_by(item_author=user.user_id).filter_by(item_read=0).count()
            num_today = count_today(user.user_id)
            num_month = count_thismonth(user.user_id)
            num_week = count_thisweek(user.user_id)
            num_year = count_thisyear(user.user_id)
            num_season = count_thisseason(user.user_id)
            data['users'][user.user_name] = {'inx':inx,'total': temp_total, 'accept': temp_accept, 'reject': temp_reject,
                                             'unread': temp_unread, 'percentage':int(temp_total/num_items*100),
                                             'num_today':num_today,'num_week':num_week,'num_month':num_month,'num_season':num_season,
                                             'num_year':num_year}
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
