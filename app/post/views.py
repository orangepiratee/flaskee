#!/usr/bin/env python
from flask import render_template, redirect, url_for, jsonify, request, send_from_directory, abort
from app import db,base_dir
from flask_login import login_required,current_user
from . import post
from ..models import *
import os
from datetime import datetime

ALLOWED_EXTENSIONS = set(['pdf'])
upload_dir = os.path.join(base_dir, 'upload')
if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1] in ALLOWED_EXTENSIONS

@post.route('/write',methods=['GET'])
@login_required
def write():
    return render_template('/post/post_write.html')

@post.route('/add', methods=['POST'])
@login_required
def add():
    try:
        title = request.form.get('input_title')
        content = request.form.get('input_content')
        if len(title)!=0 and len(content)!=0 :
            # handle uploadfile first
            try:
                f = request.files['file_attachment']
                if f and allowed_file(f.filename):
                    f.save(os.path.join(upload_dir,f.filename))
                    post = Post(post_title=title,
                                post_content=content,
                                post_datetime=datetime.utcnow(),
                                post_author=current_user._get_current_object().user_id,
                                post_attachment=f.filename)
            except:
                post = Post(post_title=title,
                            post_content=content,
                            post_datetime=datetime.utcnow(),
                            post_author=current_user._get_current_object().user_id)
            db.session.add(post)
            db.session.commit()
            temp_id = post.post_id
            return redirect(url_for('post.read',id=temp_id))
    except Exception as e:
        print(e)
        db.session.rollback()
        return render_template('/post/post_write.html')

@post.route('/read/<int:id>', methods=['GET'])
@login_required
def read(id):
    post = Post.query.filter_by(post_id=id).first_or_404()
    return render_template('/post/post_read.html', post=post)

@post.route('/manage', methods=['GET', 'POST'])
@login_required
def management():
    posts = Post.query.order_by(Post.post_datetime.desc()).filter_by(
        post_author=current_user._get_current_object().user_id)
    return render_template('/post/post_manage.html', posts=posts)