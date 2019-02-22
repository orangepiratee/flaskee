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

@main.route('/get_num/<int:inx>',methods=['GET'])
def get_num(inx):
    pass

sqls = ["",
        "select count(*) from flaskee.t_item where to_days(item_datetime) = to_days(now())", ## today
        "select count(*) from flaskee.t_item where yearweek(date_format(item_datetime,'%Y-%m-%d')) = yearweek(now())", ## this week
        "select count(*) from flaskee.t_item where date_format(item_datetime,'%Y%m') = date_format(curdate(),'%Y%m')", ## this month
        "select count(*) from flaskee.t_item where quarter(item_datetime) = quarter(now())", ## this season
        "select count(*) from flaskee.t_item where year(item_datetime) = year(now())", ## this year
        ""]

period = ['total','today','week','month','season','year']

def count_num(userid=0,category=0,index=0):
    conn = get_conn()
    cursor = conn.cursor()
    # get all items ignore userid and category
    if userid == 0 and category == 0:
        num_items = select(cursor, sqls[index])
    # get all category items by userid
    elif userid != 0 and category == 0:
        num_items = select(cursor, sqls[index]+" and item_author = '{}' ".format(userid))
    # get all user items by category
    elif userid == 0 and category != 0:
        num_items = select(cursor, sqls[index]+" and item_category = '{}' ".format(category))
    # get items by userid and category
    elif userid != 0 and category != 0:
        num_items = select(cursor, sqls[index]+" and item_author = '{}' and item_category = '{}' ".format(userid,category))
    cursor.close()
    conn.close()
    return num_items


def count_data():
    num_unread = Item.query.filter_by(item_read=0).count()
    num_users = User.query.filter_by(user_available=1).count()
    num_items = Item.query.filter_by(item_delete=0).count()
    num_items_today = count_num(index=1)
    data = {'num_unread': num_unread, 'num_users': num_users, 'num_items': num_items, 'num_items_today':num_items_today}
    users = User.query.filter_by(user_available=1).all()
    categorys = Category.query.filter_by(category_available=1).all()
    data['categorys'] = {}
    for cate in categorys:
        data['categorys'][cate.category_id]=cate.category_name
    data['users'] = {}
    inx = 1
    for user in users:
        if user.user_name:
            num_total = Item.query.filter_by(item_author=user.user_id).count()
            num_accept = Item.query.filter_by(item_author=user.user_id).filter_by(item_accept=1).count()
            num_reject = Item.query.filter_by(item_author=user.user_id).filter_by(item_accept=0).count()
            num_unread = Item.query.filter_by(item_author=user.user_id).filter_by(item_read=0).count()
            data['users'][user.user_name] = {'inx': inx, 'total': num_total, 'accept': num_accept, 'reject': num_reject,
                                             'unread': num_unread, 'percentage': int(num_total / num_items * 100)}
            inx += 1
            for i in range(1,6):
                data['users'][user.user_name][period[i]] = {}
                for category in categorys:
                    num = count_num(userid=user.user_id,category=category.category_id,index=i)
                    data['users'][user.user_name][period[i]][category.category_name] = num
                    temp_total = count_num(userid=user.user_id,index=i)
                    data['users'][user.user_name][period[i]]['total'] = temp_total
                    #data['users'][user.user_name][category.category_name] = {'num_today':num_today,'num_week':num_week,'num_month':num_month,
                    #                                           'num_season':num_season,'num_year':num_year}
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
