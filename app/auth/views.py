#!/usr/bin/env python
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..models import *
from .forms import *
from app import db
from datetime import datetime
import os


@auth.route('/signin', methods=['GET','POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(user_name=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/') or next not in ['overview','management','analysis', 'usermanage','test']:
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password!')
    return render_template('/auth/signin.html', form=form, pt2='Sign In')

@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(user_name=form.username.data,
                    password=form.password.data,
                    user_regtime=datetime.utcnow())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.signin'))
    return render_template('/auth/signup.html', form=form, pt2='Sign Up')

@auth.route('/signout', methods=['GET','POST'])
@login_required
def signout():
    logout_user()
    flash('You have been Signed out!')
    return redirect(url_for('main.index'))

@auth.route('/users', methods=['GET','POST'])
@login_required
def users():
    users = User.query.order_by(User.user_regtime.asc()).filter_by(user_available=1).all()
    return render_template('/user/userlist.html',users=users)

@auth.route('/delete/<int:id>', methods=['GET'])
@login_required
def delete(id):
    if (current_user._get_current_object().user_role >= 2):
        User.query.filter_by(user_id=id).update({'user_available':0})
        db.session.commit()
    return redirect(url_for('auth.users'))

