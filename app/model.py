# coding: utf-8
from sqlalchemy import Column, DateTime, ForeignKey, String, Text, text
from sqlalchemy.dialects.mysql import INTEGER, TINYINT
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class TRole(Base):
    __tablename__ = 't_role'

    role_id = Column(INTEGER(11), primary_key=True)
    role_name = Column(String(45))
    role_default = Column(TINYINT(4), server_default=text("'0'"))
    role_permission = Column(INTEGER(11))


class TUser(Base):
    __tablename__ = 't_user'

    user_id = Column(INTEGER(11), primary_key=True)
    user_name = Column(String(255), nullable=False)
    user_password = Column(String(128), nullable=False)
    user_available = Column(INTEGER(11), nullable=False, server_default=text("'1'"))
    user_department = Column(INTEGER(11), nullable=False)
    user_role = Column(INTEGER(11), nullable=False)
    user_regtime = Column(DateTime)
    user_lastlogtime = Column(DateTime)


class TItem(Base):
    __tablename__ = 't_item'

    item_id = Column(INTEGER(11), primary_key=True)
    item_title = Column(String(255), nullable=False)
    item_content = Column(Text, nullable=False)
    item_class = Column(INTEGER(11), nullable=False)
    item_datetime = Column(DateTime)
    item_author = Column(ForeignKey('t_user.user_id'), nullable=False, index=True)
    item_read = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    item_accept = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    item_delete = Column(TINYINT(4), nullable=False, server_default=text("'0'"))
    item_attachment = Column(String(255))

    t_user = relationship('TUser')
