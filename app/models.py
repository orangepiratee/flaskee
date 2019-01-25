#!/usr/bin/env python
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import Column, DateTime, String, Text, text, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base
from . import login_manager

Base = declarative_base()
metadata = Base.metadata


class Permission:
    WRITE = 1
    MODIFY = 2
    ADMIN = 4
    SUPER = 8
#users: 0->superadmin, 1->user, 2->admin
class Role(Base):
    __tablename__ = 't_role'

    role_id = Column(INTEGER(11), primary_key=True)
    role_name = Column(String(45))
    role_default = Column(TINYINT(4), server_default=text("'0'"))
    role_permission = Column(INTEGER(11))

    def __init__(self, **kwargs):
        super(Role, self).__init__(**kwargs)
        if self.role_permission is None:
            self.role_permission = 0


# rewrite the User Item extends to model( which is autogenerate from  mysql through sqlacodegen)
# users: 0->superadmin, 1->user, 2->admin
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

    items = db.relationship('Item', backref='user')

    @property
    def id(self):
        return self.user_id

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.user_password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.user_password, password)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.user_available is None:
            self.user_available = 1
        if self.user_role is None:
            self.user_role = 1
        if self.user_department is None:
            self.user_department = 0

    def __repr__(self):
        return '<User %r>' % self.user_name

# Items
# 0->not classified
class Item(db.Model):
    __tablename__ = 't_item'

    item_id = Column(INTEGER(11), primary_key=True)
    item_title = Column(String(255), nullable=False)
    item_content = Column(Text, nullable=False)
    item_class = Column(INTEGER(11), nullable=False)
    item_datetime = Column(DateTime)
    item_read = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    item_accept = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    item_delete = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    item_attachment = Column(String(255))
    item_author = Column(INTEGER(11),ForeignKey('t_user.user_id'), nullable=False, index=True)

    #t_user = db.relationship('User')

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)
        if self.item_read is None:
            self.item_read = 0
        if self.item_accept is None:
            self.item_accept = 0
        if self.item_delete is None:
            self.item_delete = 0
        if self.item_class is None:
            self.item_class = 0

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))