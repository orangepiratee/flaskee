#!/usr/bin/env python

from datetime import datetime
from flask import render_template, session, redirect, url_for, jsonify
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
                    item_class=form.classification.data,
                    item_datetime=datetime.utcnow(),
                    item_author=current_user._get_current_object().user_id)
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('/item/item_write.html', form=form)

@item.route('/accept/<int:id>')
@login_required
def accept():
    return