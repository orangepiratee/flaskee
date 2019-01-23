# coding: utf-8
# auto generate model.py from mysql.flaskee through sqlacodegen
# sqlacodegen mysql+pymysql://debian-sys-maint:root@localhost:3306/flaskee > app/model.py

from sqlalchemy import Column, DateTime, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Item(Base):
    __tablename__ = 'items'

    item_id = Column(INTEGER(11), primary_key=True)
    item_title = Column(String(255), nullable=False)
    item_content = Column(Text, nullable=False)
    item_class = Column(INTEGER(11), nullable=False)
    item_datetime = Column(DateTime)
    item_author = Column(INTEGER(11), nullable=False)
    item_read = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    item_accept = Column(INTEGER(11), nullable=False, server_default=text("'0'"))
    item_delete = Column(INTEGER(11), nullable=False, server_default=text("'0'"))


class User(Base):
    __tablename__ = 'users'

    user_id = Column(INTEGER(11), primary_key=True)
    user_name = Column(String(255), nullable=False)
    user_password = Column(String(128), nullable=False)
    user_available = Column(INTEGER(11), nullable=False, server_default=text("'1'"))
    user_department = Column(INTEGER(11), nullable=False)
    user_role = Column(INTEGER(11), nullable=False)
    user_regtime = Column(DateTime)
    user_lastlogtime = Column(DateTime)
