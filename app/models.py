#!/usr/bin/env python

from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from . import login_manager

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_name = db.Column(db.String(255), unique=True, nullable=False)
    user_password = db.Column(db.String(128), unique=True, nullable=False)
    user_regtime = db.Column(db.DateTime)
    user_lastlogtime = db.Column(db.DateTime)
    user_available = db.Column(db.Integer)
    user_department = db.Column(db.Integer)
    user_role = db.Column(db.Integer)

class Item(db.Model):
    __tablename__ = 'item'
    item_id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    item_title = db.Column(db.String(255), nullable=False)
    item_content = db.Column(db.Text, nullable=False)
    item_class = db.Column(db.Integer, nullable=False)
    item_datetime = db.Column(db.DateTime, nullable=False)
    item_author = db.Column(db.Integer, nullable=False)
    item_read = db.Column(db.Integer, nullable=False, default=0)
    item_accept = db.Column(db.Integer, nullable=False, default=0)

    @property
    def user_password(self):
        raise AttributeError('password is not a readable attribute')

    @user_password.setter
    def user_password(self, password):
        self.user_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_password, password)

def __repr__(self):
    return '<User %r>' % self.user_name

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))