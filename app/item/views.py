#!/usr/bin/env python
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import item
from ..models import *
from .forms import *
from app import db
from datetime import datetime

@item.route('/<id>')
@login_required
def read(id):
    item = Item.item_id.query_by(item_id=id).all()
    return render_template('test.html', item=item)

