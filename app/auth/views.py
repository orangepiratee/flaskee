#!/usr/bin/env python

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user
from . import auth
from ..models import *
from .forms import *

@auth.route('/signin', methods=['GET','POST'])
def signin():
    form = SigninForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name=form.username.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
            return redirect(next)
        flash('Invalid username or password!')
    return render_template('signin.html', form=form)

@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    return render_template('signup.html', form=form)

@auth.route('/signout', methods=['GET','POST'])
@login_required
def signout():
    logout_user()
    flash('You have been Signed out!')
    return redirect(url_for('main.index'))