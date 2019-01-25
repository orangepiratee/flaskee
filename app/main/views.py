#!/usr/bin/env python

from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import *
from .. import db
from ..models import *
from flask_login import login_required, current_user



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
    return render_template('overview.html', items=items)

@main.route('/analysis')
@login_required
def analysis():
    return render_template('analysis.html')

@main.route('/management', methods=['GET','POST'])
@login_required
def management():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(item_title=form.title.data,
                    item_content=form.content.data,
                    item_datetime=datetime.utcnow(),
                    item_author=current_user._get_current_object().user_id)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('.index'))
    items = Item.query.order_by(Item.item_datetime.desc()).all()
    return render_template('management.html', form=form, items=items)

@main.route('/signin')
def signin():
    return redirect('auth/signin')

@main.route('/signup')
def signup():
    return redirect('auth/signup')

@main.route('/signout')
def signout():
    return redirect('auth/signout')
