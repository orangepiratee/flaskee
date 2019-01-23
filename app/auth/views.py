#!/usr/bin/env python

from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user
from . import auth
from ..models import *
from .forms import *

@auth.route('/signin', methods=['GET','POST'])
def signin():
    form = SigninForm()
    return render_template('signin.html', form=form)

@auth.route('/signup', methods=['GET','POST'])
def signup():
    form = SignupForm()
    return render_template('signup.html', form=form)