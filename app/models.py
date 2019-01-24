#!/usr/bin/env python
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import Column, DateTime, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base
from . import login_manager

Base = declarative_base()
metadata = Base.metadata

# rewrite the User Item extends to model( which is autogenerate from  mysql through sqlacodegen)
class User(UserMixin, db.Model):
    __tablename__ = 't_user'
    user_id = Column(INTEGER(11), primary_key=True)
    user_name = Column(String(255), nullable=False)
    user_password = Column(String(128), nullable=False)
    user_available = Column(INTEGER(11), nullable=False, server_default=text("'1'"))
    user_department = Column(INTEGER(11), nullable=False)
    user_role = Column(INTEGER(11), nullable=False)
    user_regtime = Column(DateTime)
    user_lastlogtime = Column(DateTime)

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.user_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_password, password)

    def __repr__(self):
        return '<User %r>' % self.user_name


class Item(db.Model):
    __tablename__ = 't_item'

    item_id = Column(INTEGER(11), primary_key=True)
    item_title = Column(String(255), nullable=False)
    item_content = Column(Text, nullable=False)
    item_class = Column(INTEGER(11), nullable=False)
    item_datetime = Column(DateTime)
    item_author = Column(INTEGER(11), nullable=False)
    item_read = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    item_accept = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    item_delete = Column(INTEGER(11), nullable=False, server_default=text("'0'"))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))