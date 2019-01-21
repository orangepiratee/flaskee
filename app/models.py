#!/usr/bin/env python

from app import db

class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(255), unique=True, nullable=False)
    user_passwd = db.Column(db.String(255), unique=True, nullable=False)
    user_regtime = db.Column(db.DateTime, unique=True, nullable=False)
    user_lastlogtime = db.Column(db.DateTime, unique=True, nullable=True)
    user_available = db.Column(db.Integer, unique=True, nullable=False)
    user_department = db.Column(db.Integer, unique=True, nullable=False)

def __repr__(self):
    return '<User %r>' % self.user_name

