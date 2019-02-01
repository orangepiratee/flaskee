#!/usr/bin/env python

from datetime import datetime
from flask import render_template, session, redirect, url_for, jsonify, request
from . import item
from .forms import *
from app import db
from ..models import *
from flask_login import login_required, current_user

@item.route('/read/<int:id>', methods=['GET','POST'])
@login_required
def read(id):
    item = Item.query.filter_by(item_id=id).first_or_404()
    return render_template('/item/item_read.html', item=item)

@item.route('/modify/<int:id>')
@login_required
def modify(id):
    item = Item.query.filter_by(item_id=id).first_or_404()
    return render_template('/item/item_modify.html', item=item)

@item.route('/write', methods=['GET','POST'])
@login_required
def write():
    form = ItemForm()
    if form.validate_on_submit():
        item = Item(item_title=form.title.data,
                    item_content=form.content.data,
                    item_category=form.classification.data,
                    item_datetime=datetime.utcnow(),
                    item_author=current_user._get_current_object().user_id)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('/item/item_write.html', form=form)

@item.route('/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    try:
        title = request.form.get('input_title')
        content = request.form.get('input_content')
        category = request.form.get('select_category')
        Item.query.filter_by(item_id=id).update({'item_title':title,'item_content':content,'item_category':category})
        db.session.commit()
    except:
        db.session.rollback()
    return redirect(url_for('item.read',id=id))

@item.route('/add', methods=['POST'])
@login_required
def add():
    try:
        title = request.form.get('input_title')
        content = request.form.get('input_content')
        category = request.form.get('select_category')
        if len(title)!=0 and len(content)!=0 :
            item = Item(item_title=title,
                        item_content=content,
                        item_category=category,
                        item_datetime=datetime.utcnow(),
                        item_author=current_user._get_current_object().user_id)
            db.session.add(item)
            db.session.commit()
            temp_id = item.item_id
            return redirect(url_for('item.read',id=temp_id))
    except:
        db.session.rollback()
        return render_template('/item/item_write.html')

@item.route('/accept/<int:id>')
@login_required
def accept():
    return

@item.route('/download/<int:id>')
@login_required
def download():
    return