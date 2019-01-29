#!/usr/bin/env python

from datetime import datetime
from flask import render_template, session, redirect, url_for, jsonify
from . import main
from .forms import *
from app import db
from ..models import *
from flask_login import login_required, current_user

@main.route('/test')
def test():
    #return main.send_static_file('theme181/index.html')
    return render_template('webbase.html')

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
    items = Item.query.order_by(Item.item_datetime.desc()).all()
    users = User.query.order_by(User.user_name.desc()).all()
    '''tempusers = []
    for user in users:
        temp = {}
        temp['user_name']=user.user_name
        temp['user_id']=user.user_id
        tempusers.append(temp)
    session['users'] = users'''
    return render_template('overview.html', items=items,users=users)

@main.route('/analysis')
@login_required
def analysis():
    return render_template('analysis.html')

@main.route('/manage', methods=['GET','POST'])
@login_required
def management():
    items = Item.query.order_by(Item.item_datetime.desc()).filter_by(item_author=current_user._get_current_object().user_id)
    return render_template('manage.html', items=items)


@main.route('/item/<id>')
@login_required
def read(id):
    item = Item.query.filter_by(item_id=id).first_or_404()
    return render_template('/item/item_read.html', item=item)

@main.route('/item/modify/<id>')
@login_required
def modify(id):
    item = Item.query.filter_by(item_id=id).first_or_404()
    return render_template('/item/item_modify.html', item=item)

@main.route('/item/write', methods=['GET','POST'])
@login_required
def write():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(item_title=form.title.data,
                    item_content=form.content.data,
                    item_datetime=datetime.utcnow(),
                    item_author=current_user._get_current_object().user_id)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('.management'))
    return render_template('/item/item_write.html', form=form)

@main.route('/users')
@login_required
def users():
    users = User.query.order_by(User.user_id).all()
    return render_template('/user/users.html', users=users)
