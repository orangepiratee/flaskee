#!/usr/bin/env python
from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from sqlalchemy import Column, DateTime, String, Text, text, ForeignKey
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.ext.declarative import declarative_base
from . import login_manager

from datetime import  datetime

Base = declarative_base()
metadata = Base.metadata


class Permission:
    #write a new item
    WRITE = 1
    #modify the item
    MODIFY = 2
    #accept or reject the item
    MANAGE = 4
    #super privilege
    ADMIN = 8

#users: 0->superadmin, 1->user, 2->manager
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

    def add_permission(self, perm):
        self.role_permission += perm

    def remove_permission(self, perm):
        self.role_permission -= perm

    def reset_permission(self):
        self.role_permission = 1

    def has_permission(self, perm):
        return self.role_permission & perm ==perm


# rewrite the User Item extends to model( which is autogenerate from  mysql through sqlacodegen)
# users: 0->superadmin, 1->user, 2->manager
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

    def ping(self):
        self.user_lastlogtime = datetime.utcnow()
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return '<User %r>' % self.user_name

# Items
# 0->not classified
class Item(db.Model):
    __tablename__ = 't_item'

    item_id = Column(INTEGER(11), primary_key=True)
    item_title = Column(String(255), nullable=False)
    item_content = Column(Text, nullable=False)
    item_category = Column(INTEGER(11), nullable=False)
    item_datetime = Column(DateTime)
    item_read = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    item_accept = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    item_delete = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    item_attachment = Column(String(255))
    item_author = Column(INTEGER(11),ForeignKey('t_user.user_id'), nullable=False, index=True)
    item_stars = Column(INTEGER(11), nullable=False, server_default=text("'0'"))

    #t_user = db.relationship('User')

    def __init__(self, **kwargs):
        super(Item, self).__init__(**kwargs)
        if self.item_read is None:
            self.item_read = 0
        if self.item_accept is None:
            self.item_accept = 0
        if self.item_delete is None:
            self.item_delete = 0
        if self.item_category is None:
            self.item_category = 0

class Comment(db.Model):
    __tablename__ = 't_comment'

    comment_id = Column(INTEGER(11), primary_key=True)
    comment_content = Column(Text, nullable=False)
    comment_author = Column(ForeignKey('t_user.user_id'), nullable=False, index=True)
    comment_author_name = Column(String(45), nullable=False)
    comment_target = Column(ForeignKey('t_item.item_id'), nullable=False, index=True)
    comment_datetime = Column(DateTime, nullable=False)

    #t_user = db.relationship('User')
    #t_item = db.relationship('Item')

class Category(db.Model):
    __tablename__ = 't_category'

    category_id = Column(INTEGER(11), primary_key=True)
    category_name = Column(String(255), nullable=False)
    category_available = Column(INTEGER(11), nullable=False, server_default=text("'1'"))

class Post(db.Model):
    __tablename__ = 't_post'

    post_id = Column(INTEGER(11), primary_key=True)
    post_title = Column(Text, nullable=False)
    post_content = Column(Text, nullable=False)
    post_author = Column(ForeignKey('t_user.user_id'), nullable=False, index=True)
    post_datetime = Column(DateTime, nullable=False)
    post_delete = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    post_attachment = Column(Text)

    #t_user = relationship('User')

class Notification(db.Model):
    __tablename__ = 't_notification'

    notification_id = Column(INTEGER(11), primary_key=True)
    notification_content = Column(Text, nullable=False)
    notification_author = Column(ForeignKey('t_user.user_id'), nullable=False, index=True)
    notification_reader = Column(ForeignKey('t_user.user_id'), nullable=False, index=True)
    notification_target = Column(Text)
    notification_datetime = Column(DateTime, nullable=False)
    notification_read = Column(INTEGER(11), nullable=False, server_default=text("'0'"))

    #t_user = relationship('User')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))