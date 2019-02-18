#!/usr/bin/env python

from datetime import datetime
from flask import render_template, redirect, url_for, jsonify, request, send_from_directory, abort
from . import item
from .forms import *
from app import db, base_dir,pt1,pt2,pt3
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
    return render_template('/item/item_read.html', item=item, comments=comments,pt1=pt1[0],pt2=pt2[0],pt3=pt3[2])

@item.route('<int:id>',methods=['GET'])
@login_required
def item_read(id):
    return redirect(url_for('item.read',id=id))

@item.route('/modify/<int:id>')
@login_required
def modify(id):
    item = Item.query.filter_by(item_id=id).first_or_404()
    return render_template('/item/item_modify.html', item=item,pt1=pt1[0],pt2=pt2[2],pt3=pt3[2])

@item.route('/write', methods=['GET','POST'])
@login_required
def write():
    return render_template('/item/item_write.html',pt1=pt1[0],pt2=pt2[1])

@item.route('/update/<int:id>', methods=['POST'])
@login_required
def update(id):
    try:
        title = request.form.get('input_title')
        content = request.form.get('input_content')
        category = request.form.get('select_category')
        Item.query.filter_by(item_id=id).update({'item_title':title,'item_content':content,'item_category':category,'item_read':0})
        db.session.commit()
        # generate a notification
        try:
            user = current_user._get_current_object()
            if user.user_role == 2:
                add_notification(user.user_id, user.user_name, Item.query.filter_by(item_id=id).first_or_404().item_author,
                                 '/item/' + str(id), 4)
            else:
                add_notification(user.user_id, user.user_name, User.query.filter_by(user_role=2).first_or_404().user_id,
                                 '/item/' + str(id), 3)
        except Exception as e:
            print(e)
            pass
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
            # handle uploadfile first
            try:
                f = request.files['file_attachment']
                if f and allowed_file(f.filename):
                    f.save(os.path.join(upload_dir,f.filename))
                item = Item(item_title=title,
                            item_content=content,
                            item_category=category,
                            item_datetime=datetime.utcnow(),
                            item_author=current_user._get_current_object().user_id,
                            item_attachment=f.filename)
            except:
                item = Item(item_title=title,
                            item_content=content,
                            item_category=category,
                            item_datetime=datetime.utcnow(),
                            item_author=current_user._get_current_object().user_id)
            db.session.add(item)
            db.session.commit()
            temp_id = item.item_id
            # generate a notification to manager
            temp_user = current_user._get_current_object()
            add_notification(temp_user.user_id, temp_user.user_name,
                             User.query.filter_by(user_role=2).first_or_404().user_id, '/item/'+str(temp_id),2)
            return redirect(url_for('item.read',id=temp_id))
        else:
            return render_template('/item/item_write.html')
    except Exception as e:
        print(e)
        db.session.rollback()
        return render_template('/item/item_write.html')

@item.route('/accept/<int:id>')
@login_required
def accept(id):
    if current_user._get_current_object().user_role >=2:
        try:
            Item.query.filter_by(item_id=id).update({'item_accept':1})
            db.session.commit()
            add_notification(current_user._get_current_object().user_id,
                             current_user._get_current_object().user_name,
                             Item.query.filter_by(item_id=id).first_or_404().item_author,
                             '/item/'+str(id),5)
        except:
            db.session.rollback()
    return redirect(url_for('item.read',id=id))

@item.route('/reject/<int:id>')
@login_required
def reject(id):
    if current_user._get_current_object().user_role >=2:
        try:
            Item.query.filter_by(item_id=id).update({'item_accept':0})
            db.session.commit()
            add_notification(current_user._get_current_object().user_id,
                             current_user._get_current_object().user_name,
                             Item.query.filter_by(item_id=id).first_or_404().item_author,
                             '/item/' + str(id), 6)
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
        item_author=current_user._get_current_object().user_id).all()
    return render_template('manage.html', items=items,pt1=pt1[0],pt2=pt2[4])

@item.route('/categoryshow/<int:id>',methods=['GET'])
@login_required
def categoryshow(id):
    items = Item.query.filter_by(item_category=id).order_by(Item.item_datetime.desc()).all()
    return render_template('manage.html', items=items,pt1=pt1[0],pt2=pt2[3],pt3=pt3[0])

@item.route('/authorshow/<int:id>',methods=['GET'])
@login_required
def authorshow(id):
    items = Item.query.filter_by(item_author=id).order_by(Item.item_datetime.desc()).all()
    return render_template('manage.html', items=items,pt1=pt1[0],pt2=pt2[3],pt3=pt3[1])