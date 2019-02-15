#!/usr/bin/env python

from datetime import datetime
from flask import render_template, redirect, url_for, jsonify, request, send_from_directory, abort
from . import item
from .forms import *
from app import db, base_dir
from ..models import *
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os, base64
from ..main.views import add_notification

ALLOWED_EXTENSIONS = set(['zip','rar','tar','pdf'])
upload_dir = os.path.join(base_dir, 'upload')
if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@item.route('/read/<int:id>', methods=['GET','POST'])
@login_required
def read(id):
    item = Item.query.filter_by(item_id=id).first_or_404()
    if(current_user._get_current_object().user_role ==2):
        Item.query.filter_by(item_id=id).update({'item_read':1})
        db.session.commit()
    comments = Comment.query.filter_by(comment_target=id).order_by(Comment.comment_datetime.desc()).all()
    return render_template('/item/item_read.html', item=item, comments=comments)

@item.route('/modify/<int:id>')
@login_required
def modify(id):
    item = Item.query.filter_by(item_id=id).first_or_404()
    return render_template('/item/item_modify.html', item=item)

@item.route('/write', methods=['GET','POST'])
@login_required
def write():
    return render_template('/item/item_write.html')

@item.route('/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    try:
        title = request.form.get('input_title')
        content = request.form.get('input_content')
        category = request.form.get('select_category')
        Item.query.filter_by(item_id=id).update({'item_title':title,'item_content':content,'item_category':category,'item_read':0})
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
        f = request.files['file_attachment']
        if len(title)!=0 and len(content)!=0 :
            # handle uploadfile first
            if f and allowed_file(f.filename):
                f.save(os.path.join(upload_dir,f.filename))
            item = Item(item_title=title,
                        item_content=content,
                        item_category=category,
                        item_datetime=datetime.utcnow(),
                        item_author=current_user._get_current_object().user_id,
                        item_attachment=f.filename)
            db.session.add(item)
            db.session.commit()
            temp_id = item.item_id
            return redirect(url_for('item.read',id=temp_id))
    except Exception as e:
        print(e)
        db.session.rollback()
        return render_template('/item/item_write.html')

@item.route('/accept/<int:id>')
@login_required
def accept(id):
    if current_user._get_current_object().user_id >=2:
        try:
            Item.query.filter_by(item_id=id).update({'item_accept':1})
            db.session.commit()
        except:
            db.session.rollback()
    return redirect(url_for('item.read',id=id))

@item.route('/reject/<int:id>')
@login_required
def reject(id):
    if current_user._get_current_object().user_id >=2:
        try:
            Item.query.filter_by(item_id=id).update({'item_accept':0})
            db.session.commit()
        except:
            db.session.rollback()
    return redirect(url_for('item.read',id=id))


@item.route('/download/<string:filename>', methods=['GET'])
@login_required
def download(filename):
        if os.path.exists(os.path.join(upload_dir,filename)):
            return send_from_directory(upload_dir,filename,as_attachment=True)
        abort(404)

@item.route('/manage', methods=['GET', 'POST'])
@login_required
def management():
    items = Item.query.order_by(Item.item_datetime.desc()).filter_by(
        item_author=current_user._get_current_object().user_id)
    return render_template('manage.html', items=items)