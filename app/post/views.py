#!/usr/bin/env python
from flask import render_template, redirect, url_for, jsonify, request, send_from_directory, abort
from app import db
from flask_login import login_required,current_user
from . import post
from ..models import *

@post.route('/write',methods=['GET'])
@login_required
def write():
    return render_template('/post/post_write.html')