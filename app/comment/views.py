#!/usr/bin/env python


from . import comment
from ..models import *
from flask_login import login_required, current_user
from flask import render_template, redirect, url_for, jsonify, request, send_from_directory, abort
import os,datetime
from ..main.views import add_notification


@comment.route('/add/<int:id>',methods=['POST'])
@login_required
def addcomment(id):
    if current_user._get_current_object().user_role >= 2:
        try:
            content = request.form.get('input_content')
            comment = Comment(comment_content = content,
                              comment_author = current_user._get_current_object().user_id,
                              comment_author_name = current_user._get_current_object().user_name,
                              comment_target = id,
                              comment_datetime = datetime.datetime.utcnow())
            db.session.add(comment)
            db.session.commit()
        except Exception as e:
            print(e)
            db.session.rollback()
    return redirect('/item/read/'+str(id))

@comment.route('<int:id>',methods=['GET'])
@login_required
def comment_read(id):
    comment = Comment.query.filter_by(comment_id=id).first_or_404()
    return redirect(url_for('item.read',id=comment.comment_target))
